/*--------------------------------------------------------------------------------------
 *  Copyright 2025 Glass Devtools, Inc. All rights reserved.
 *  Licensed under the Apache License, Version 2.0. See LICENSE.txt for more information.
 *--------------------------------------------------------------------------------------*/

import { Disposable } from '../../../../base/common/lifecycle.js';
import { registerSingleton, InstantiationType } from '../../../../platform/instantiation/common/extensions.js';
import { createDecorator } from '../../../../platform/instantiation/common/instantiation.js';
import { IMainProcessService } from '../../../../platform/ipc/common/mainProcessService.js';
import { IChannel } from '../../../../base/parts/ipc/common/ipc.js';
import { IStorageService, StorageScope, StorageTarget } from '../../../../platform/storage/common/storage.js';
import { IWorkspaceContextService, IWorkspaceFolder } from '../../../../platform/workspace/common/workspace.js';
import { generateUuid } from '../../../../base/common/uuid.js';
import { IChatThreadService, ThreadType } from '../browser/chatThreadService.js';
import { ChatMessage } from './chatThreadServiceTypes.js';
import { CursorImportReadResult, CursorImportScanResult, CursorImportedConversation } from './cursorImportServiceTypes.js';

const SEEN_IDS_STORAGE_KEY = 'brain.cursorImport.seenIds';

export interface ICursorImportService {
	readonly _serviceBrand: undefined;

	// auto-detects Cursor's storage and counts conversations (fast, no message bodies)
	scan(): Promise<CursorImportScanResult>;

	// reads everything from Cursor and imports as 404Brain threads (idempotent: already-seen chats are skipped)
	importFromCursor(): Promise<{ imported: number; skipped: number; error?: string }>;

	// true if a previous import has already run (used to hide/keep the banner)
	hasImportedBefore(): boolean;

	// import .cursorrules / .cursor/rules/*.mdc into .brainrules for the current workspace
	importCursorRulesToBrainrules(): Promise<{ created: boolean; error?: string }>;
}

export const ICursorImportService = createDecorator<ICursorImportService>('cursorImportService');

class CursorImportService extends Disposable implements ICursorImportService {
	_serviceBrand: undefined;

	private readonly channel: IChannel; // CursorImportChannel
	private _cachedScanResult: CursorImportScanResult | null = null;

	constructor(
		@IMainProcessService private readonly mainProcessService: IMainProcessService,
		@IWorkspaceContextService private readonly workspaceContextService: IWorkspaceContextService,
		@IStorageService private readonly storageService: IStorageService,
		@IChatThreadService private readonly chatThreadService: IChatThreadService,
	) {
		super();
		this.channel = this.mainProcessService.getChannel('brain-channel-cursorImport');
	}

	private _getCurrentWorkspaceFolders(): string[] {
		const normalize = (p: string) => p.replace(/[\\/]/g, pathSep).toLowerCase();
		const folders = this.workspaceContextService.getWorkspace().folders ?? [];
		return folders.map((f: IWorkspaceFolder) => normalize(f.uri.fsPath));
	}

	private _normalizedFoldersList(): string[] | null {
		const folders = this._getCurrentWorkspaceFolders();
		return folders.length > 0 ? folders : null;
	}

	async scan(): Promise<CursorImportScanResult> {
		if (this._cachedScanResult) return this._cachedScanResult;
		const scanResult: CursorImportScanResult = await this.channel.call('scan', {});
		if (!scanResult?.cursorFound) {
			const empty: CursorImportScanResult = { cursorFound: false, cursorDataPath: null, workspaceCount: 0, conversationCount: 0, currentWorkspaceConversations: 0, entries: [] };
			this._cachedScanResult = empty;
			return empty;
		}

		const currentFolders = this._normalizedFoldersList();
		let currentWorkspaceConversations = 0;
		if (currentFolders) {
			for (const entry of scanResult.entries ?? []) {
				const folder = entry.workspaceFolder.replace(/[\\/]/g, pathSep).toLowerCase();
				if (currentFolders.includes(folder)) {
					currentWorkspaceConversations += entry.conversationCount;
				}
			}
		}

		const result: CursorImportScanResult = { ...scanResult, currentWorkspaceConversations };
		this._cachedScanResult = result;
		return result;
	}

	async importFromCursor(): Promise<{ imported: number; skipped: number; error?: string }> {
		try {
			const readResult: CursorImportReadResult = await this.channel.call('read', {});
			if (!readResult?.cursorFound) {
				return { imported: 0, skipped: 0, error: 'Cursor data not found. Install/run Cursor once first.' };
			}
			if (!readResult.conversations?.length) {
				return { imported: 0, skipped: 0, error: 'No chats found in Cursor.' };
			}

			const seenIds = new Set<string>(this._getSeenIds());

			const toImport: CursorImportedConversation[] = [];
			let skipped = 0;
			for (const conversation of readResult.conversations) {
				const dedupeKey = this._dedupeKeyOf(conversation);
				if (seenIds.has(dedupeKey)) {
					skipped++;
					continue;
				}
				if (conversation.messages.length === 0) {
					skipped++;
					continue;
				}
				toImport.push(conversation);
			}

			const threads = toImport.map(c => this._conversationToThread(c));
			const { imported } = this.chatThreadService.importThreads(threads);

			// remember the ids that have been handled (both imported and skipped-by-dedupe get marked as seen)
			const newSeen = new Set(seenIds);
			for (const conversation of readResult.conversations) {
				newSeen.add(this._dedupeKeyOf(conversation));
			}
			this._storeSeenIds(Array.from(newSeen));

			return { imported, skipped, error: undefined };
		} catch (e) {
			return { imported: 0, skipped: 0, error: String(e) };
		}
	}

	hasImportedBefore(): boolean {
		return this._getSeenIds().length > 0;
	}

	async importCursorRulesToBrainrules(): Promise<{ created: boolean; error?: string }> {
		try {
			const workspaceFolders = this.workspaceContextService.getWorkspace().folders ?? [];
			if (workspaceFolders.length === 0) {
				return { created: false, error: 'No workspace folder opened.' };
			}
			// handled from renderer via IFileService? main channel would be needed for fs read of .cursorrules.
			const result: { created: boolean; error?: string } = await this.channel.call('importRules', { workspaceFolders });
			return result;
		} catch (e) {
			return { created: false, error: String(e) };
		}
	}

	private _dedupeKeyOf(conversation: CursorImportedConversation): string {
		return `${conversation.workspaceFolder.toLowerCase()}||${conversation.id}`;
	}

	private _getSeenIds(): string[] {
		const raw = this.storageService.get(SEEN_IDS_STORAGE_KEY, StorageScope.APPLICATION);
		if (!raw) return [];
		try {
			const parsed = JSON.parse(raw);
			return Array.isArray(parsed) ? parsed.filter((x): x is string => typeof x === 'string') : [];
		} catch {
			return [];
		}
	}

	private _storeSeenIds(ids: string[]) {
		this.storageService.store(SEEN_IDS_STORAGE_KEY, JSON.stringify(ids), StorageScope.APPLICATION, StorageTarget.USER);
	}

	private _conversationToThread(conversation: CursorImportedConversation): ThreadType {
		const messages: ChatMessage[] = conversation.messages.map(m => {
			if (m.role === 'user') {
				return {
					role: 'user',
					content: m.text,
					displayContent: m.text,
					selections: null,
					images: null,
					state: { stagingSelections: [], isBeingEdited: false },
				} satisfies ChatMessage;
			}
			return {
				role: 'assistant',
				displayContent: m.text,
				reasoning: '',
				anthropicReasoning: null,
			} satisfies ChatMessage;
		});

		const firstUserText = conversation.messages.find(m => m.role === 'user')?.text ?? '';

		return {
			id: generateUuid(),
			title: conversation.title || (firstUserText.length > 60 ? firstUserText.slice(0, 60) + '…' : firstUserText),
			createdAt: conversation.createdAt,
			lastModified: conversation.updatedAt,
			messages,
			filesWithUserChanges: new Set(),
			state: {
				currCheckpointIdx: null,
				stagingSelections: [],
				focusedMessageIdx: undefined,
				linksOfMessageIdx: {},
			},
		};
	}
}

const pathSep = process.platform === 'win32' ? '\\' : '/';

registerSingleton(ICursorImportService, CursorImportService, InstantiationType.Eager);