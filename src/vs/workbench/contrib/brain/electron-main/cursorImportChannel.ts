/*--------------------------------------------------------------------------------------
 *  Copyright 2025 Glass Devtools, Inc. All rights reserved.
 *  Licensed under the Apache License, Version 2.0. See LICENSE.txt for more information.
 *--------------------------------------------------------------------------------------*/

// registered in app.ts
// Reads Cursor's local storage (chat database) from main process and returns it to the browser
// so chats can be imported into 404Brain fully automatically.

import { IServerChannel } from '../../../../base/parts/ipc/common/ipc.js';
import { promises as fsPromises, statSync } from 'fs';
import * as os from 'os';
import * as path from 'path';
import { CursorImportedConversation, CursorImportReadResult, CursorImportScanResult } from '../common/cursorImportServiceTypes.js';

type ChatTab = {
	tabId?: string;
	chatTitle?: string;
	lastSendTime?: number;
	bubbles?: ChatBubble[];
};

type ChatBubble = {
	type: 'user' | 'ai' | string;
	text?: string | null;
	[_: string]: unknown;
};

const CHATDATA_KEY = 'workbench.panel.aichat.view.aichat.chatdata';
const COMPOSER_DATA_KEY = 'composer.composerData';
const WORKSPACE_STORAGE_RELATIVE = path.join('User', 'workspaceStorage');

const getCursorDataDir = (): string | null => {
	let base: string | null = null;
	if (process.platform === 'win32') {
		base = process.env.APPDATA ?? path.join(os.homedir(), 'AppData', 'Roaming');
	} else if (process.platform === 'darwin') {
		base = path.join(os.homedir(), 'Library', 'Application Support');
	} else {
		base = process.env.XDG_CONFIG_HOME ?? path.join(os.homedir(), '.config');
	}
	const dir = path.join(base, 'Cursor');
	return fsExistsSync(dir) ? dir : null;
};

const fsExistsSync = (p: string): boolean => {
	try {
		statSync(p);
		return true;
	} catch {
		return false;
	}
};

const openSqliteDatabase = async (dbPath: string): Promise<any> => {
	const sqlite3 = (await import('@vscode/sqlite3')) as typeof import('@vscode/sqlite3');
	const Database = (sqlite3 as any).default?.Database ?? (sqlite3 as any).Database;
	return new Promise<any>((resolve, reject) => {
		const db = new Database(dbPath, (err: Error | null) => {
			if (err) {
				reject(err);
				return;
			}
			resolve(db);
		});
	});
};

const queryAll = (db: any, sql: string, params: any[] = []): Promise<any[]> => {
	return new Promise<any[]>((resolve, reject) => {
		db.all(sql, params, (err: Error | null, rows: any[]) => {
			if (err) {
				reject(err);
				return;
			}
			resolve(rows);
		});
	});
};

const queryGet = (db: any, sql: string, params: any[] = []): Promise<any> => {
	return new Promise<any>((resolve, reject) => {
		db.get(sql, params, (err: Error | null, row: any) => {
			if (err) {
				reject(err);
				return;
			}
			resolve(row);
		});
	});
};

const closeDatabase = (db: any): Promise<void> => {
	return new Promise<void>((resolve) => {
		db.close(() => resolve());
	});
};

const decodeWorkspaceFolder = (folderRaw: string | undefined): { folder: string; label: string } => {
	if (!folderRaw) {
		return { folder: '', label: '(unknown workspace)' };
	}
	const isFile = /^file:\/\//i.test(folderRaw);
	let decoded = folderRaw;
	try {
		if (isFile) {
			decoded = decodeURIComponent(folderRaw.replace(/^file:\/\//i, ''));
		}
	} catch {
		// keep raw on decode error
	}

	if (isFile) {
		// on windows convert /h:/Users/... to h:\Users\...
		const driveMatch = decoded.match(/^\/([a-zA-Z]:)\/(.*)$/);
		if (process.platform === 'win32' && driveMatch) {
			const normalized = `${driveMatch[1]}\\${driveMatch[2].replace(/\//g, '\\')}`;
			return { folder: normalized, label: path.basename(normalized) || normalized };
		}
		return { folder: decoded, label: path.basename(decoded) || decoded };
	}

	// remote or other scheme: keep as label
	const short = folderRaw.length > 70 ? folderRaw.slice(0, 70) + '…' : folderRaw;
	return { folder: '', label: short };
};

const normalizeMessageText = (b: ChatBubble): string => {
	const t = b.text;
	if (typeof t === 'string') return t;
	if (t === null || t === undefined) return '';
	return String(t);
};

// parse a chatdata / composer JSON value into a list of conversations
const parseChatJson = (rawValue: unknown, workspaceFolderRaw: string): CursorImportedConversation[] => {
	let valueBuffer = rawValue;
	if (valueBuffer && typeof valueBuffer === 'object' && (valueBuffer as any).type === 'Buffer') {
		valueBuffer = Buffer.from((valueBuffer as any).data);
	}
	if (Buffer.isBuffer(valueBuffer)) {
		valueBuffer = valueBuffer.toString('utf8');
	}
	if (typeof valueBuffer !== 'string') return [];

	let json: any;
	try {
		json = JSON.parse(valueBuffer);
	} catch {
		return [];
	}
	if (!json || typeof json !== 'object') return [];

	const { folder, label } = decodeWorkspaceFolder(workspaceFolderRaw);

	// modern format: { tabs: [...] }
	const tabs: ChatTab[] = Array.isArray(json.tabs) ? json.tabs : [];
	// legacy format: { composers: [...] } -> best effort
	const composers = Array.isArray(json.composers) ? json.composers : [];

	const conversations: CursorImportedConversation[] = [];
	const seenTabIds = new Set<string>();

	for (const tab of tabs) {
		if (!tab || typeof tab !== 'object') continue;
		const bubbles = Array.isArray(tab.bubbles) ? tab.bubbles : [];
		const messages = bubbles
			.filter(b => b && b.type === 'user' || b && b.type === 'ai')
			.map(b => {
				const text = normalizeMessageText(b);
				const role = b.type === 'user' ? 'user' as const : 'assistant' as const;
				return { role, text };
			})
			.filter(m => m.text.length > 0);

		if (messages.length === 0) continue;

		const id = tab.tabId || (tab as any).composerId || '';
		if (id) {
			if (seenTabIds.has(id)) continue;
			seenTabIds.add(id);
		}

		const ts = typeof tab.lastSendTime === 'number' && tab.lastSendTime > 0 ? tab.lastSendTime : Date.now();
		conversations.push({
			id,
			title: typeof tab.chatTitle === 'string' ? tab.chatTitle : '',
			createdAt: new Date(ts).toISOString(),
			updatedAt: new Date(ts).toISOString(),
			workspaceFolder: folder,
			workspaceLabel: label,
			messages,
		});
	}

	// legacy composers (if any real content)
	for (const c of composers) {
		if (!c || typeof c !== 'object') continue;
		const messages: CursorImportedConversation['messages'] = [];
		// no reliable message mapping — skip
		if (messages.length === 0) continue;
		// (kept intentionally minimal: modern chatdata is the source of truth)
		conversations.push({
			id: String((c as any).composerId ?? ''),
			title: (c as any).title ?? '',
			createdAt: new Date().toISOString(),
			updatedAt: new Date().toISOString(),
			workspaceFolder: folder,
			workspaceLabel: label,
			messages,
		});
	}

	return conversations;
};

export class CursorImportChannel implements IServerChannel {

	// events are not used by this channel
	listen(_: unknown, event: string): any {
		throw new Error(`CursorImportChannel: Event not found: ${event}`);
	}

	async call(_: unknown, command: string, params: any): Promise<any> {
		try {
			if (command === 'scan') {
				return await this._scan();
			}
			else if (command === 'read') {
				return await this._read();
			}
			else if (command === 'importRules') {
				return await this._importRules(params.workspaceFolders ?? []);
			}
			else {
				throw new Error(`CursorImportChannel: command "${command}" not recognized.`)
			}
		}
		catch (e) {
			console.error('cursorImport channel: Call Error:', e);
			return { cursorFound: false, cursorDataPath: null, conversations: [], error: String(e) } satisfies CursorImportReadResult;
		}
	}

	private async _scan(): Promise<CursorImportScanResult> {
		const cursorDataPath = getCursorDataDir();
		if (!cursorDataPath) {
			return { cursorFound: false, cursorDataPath: null, workspaceCount: 0, conversationCount: 0, currentWorkspaceConversations: 0, entries: [] };
		}
		const wsRoot = path.join(cursorDataPath, WORKSPACE_STORAGE_RELATIVE);
		const result = await this._readWorkspaceDb(wsRoot);
		return {
			cursorFound: true,
			cursorDataPath,
			workspaceCount: result.workspaceCount,
			conversationCount: result.conversations.length,
			currentWorkspaceConversations: 0, // computed browser-side against the current workspace
			entries: result.conversations.map(c => ({ workspaceFolder: c.workspaceFolder, workspaceLabel: c.workspaceLabel, conversationCount: 1 })),
		};
	}

	private async _read(): Promise<CursorImportReadResult> {
		const cursorDataPath = getCursorDataDir();
		if (!cursorDataPath) {
			return { cursorFound: false, cursorDataPath: null, conversations: [] };
		}
		const wsRoot = path.join(cursorDataPath, WORKSPACE_STORAGE_RELATIVE);
		const result = await this._readWorkspaceDb(wsRoot);
		return { cursorFound: true, cursorDataPath, conversations: result.conversations };
	}

	// convert .cursorrules + .cursor/rules/*.mdc (+ global ~/.cursor/rules) into a .brainrules file
	// only creates the file if it does not exist yet. returns created = true when at least one rules file was written.
	private async _importRules(workspaceFolders: string[]): Promise<{ created: boolean; error?: string }> {
		try {
			// global rules (apply to every workspace)
			const globalRulesDir = path.join(os.homedir(), '.cursor', 'rules');
			const globalParts: string[] = [];
			if (fsExistsSync(globalRulesDir)) {
				for (const file of await fsPromises.readdir(globalRulesDir)) {
					if (file.endsWith('.mdc')) {
						globalParts.push(await fsPromises.readFile(path.join(globalRulesDir, file), 'utf8'));
					}
				}
			}

			let created = false;
			for (const folder of workspaceFolders) {
				if (!folder || !fsExistsSync(folder)) continue;
				const brainrulesPath = path.join(folder, '.brainrules');
				if (fsExistsSync(brainrulesPath)) continue; // never overwrite existing rules

				const parts: string[] = [...globalParts];

				// legacy .cursorrules file
				const cursorrulesPath = path.join(folder, '.cursorrules');
				if (fsExistsSync(cursorrulesPath)) {
					parts.push(await fsPromises.readFile(cursorrulesPath, 'utf8'));
				}

				// modern .cursor/rules/*.mdc (project-scoped)
				const projectRulesDir = path.join(folder, '.cursor', 'rules');
				if (fsExistsSync(projectRulesDir)) {
					const files = (await fsPromises.readdir(projectRulesDir)).filter(f => f.endsWith('.mdc')).sort();
					for (const file of files) {
						parts.push(await fsPromises.readFile(path.join(projectRulesDir, file), 'utf8'));
					}
				}

				const content = parts.filter(p => (p || '').trim().length > 0).join('\n\n---\n\n');
				if (!content.trim()) continue;

				const header = '// Imported from Cursor (.cursorrules / rules/*.mdc) by 404Brain\n// You can edit this file freely — it is read by 404Brain on every message.\n\n';
				await fsPromises.writeFile(brainrulesPath, header + content, 'utf8');
				created = true;
			}

			return { created };
		} catch (e) {
			return { created: false, error: String(e) };
		}
	}

	private async _readWorkspaceDb(wsRoot: string): Promise<{ conversations: CursorImportedConversation[]; workspaceCount: number }> {
		let workspaceDirs: string[] = [];
		try {
			workspaceDirs = (await fsPromises.readdir(wsRoot, { withFileTypes: true }))
				.filter(e => e.isDirectory())
				.map(e => path.join(wsRoot, e.name));
		} catch {
			return { conversations: [], workspaceCount: 0 };
		}

		const conversations: CursorImportedConversation[] = [];
		let workspaceCount = 0;

		for (const dir of workspaceDirs) {
			const wsJsonPath = path.join(dir, 'workspace.json');
			const dbPath = path.join(dir, 'state.vscdb');
			if (!fsExistsSync(dbPath)) continue;
			workspaceCount++;

			let folderRaw: string | undefined;
			try {
				const wsJson = JSON.parse(await fsPromises.readFile(wsJsonPath, 'utf8'));
				folderRaw = wsJson?.folder;
			} catch {
				folderRaw = undefined;
			}

			let db: any = null;
			try {
				db = await openSqliteDatabase(dbPath);
				// do not ever modify Cursor's database
				await queryGet(db, `PRAGMA query_only = ON`, []);
				const rows = await queryAll(db, `SELECT key FROM ItemTable WHERE key = ? OR key = ?`, [CHATDATA_KEY, COMPOSER_DATA_KEY]);

				for (const row of rows) {
					const key = row?.key;
					if (!key) continue;
					const found = await queryGet(db, `SELECT value FROM ItemTable WHERE key = ?`, [key]);
					if (!found) continue;
					// BLOB -> Buffer
					const val = found.value;
					if (!val) continue;
					const jsonStr = Buffer.isBuffer(val) ? val.toString('utf8') : String(val);
					const convos = parseChatJson(jsonStr, folderRaw || dir);
					conversations.push(...convos);
				}
			} catch (err) {
				// a single broken/old state.vscdb should not abort the whole scan
				console.error(`cursorImport: failed to read ${dbPath}:`, err);
			} finally {
				if (db) {
					try { await closeDatabase(db); } catch { /* ignore */ }
				}
			}
		}

		// keep conversations sorted by recency (most recent first)
		conversations.sort((a, b) => new Date(b.updatedAt).getTime() - new Date(a.updatedAt).getTime());

		return { conversations, workspaceCount };
	}
}