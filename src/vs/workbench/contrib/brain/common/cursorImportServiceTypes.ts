/*--------------------------------------------------------------------------------------
 *  Copyright 2025 Glass Devtools, Inc. All rights reserved.
 *  Licensed under the Apache License, Version 2.0. See LICENSE.txt for more information.
 *--------------------------------------------------------------------------------------*/

// shared types between the main-process cursor import channel and the browser service

// a minimal message as parsed from Cursor's storage (bubble)
export type CursorImportedMessage = {
	role: 'user' | 'assistant';
	text: string;
};

// one conversation (Cursor "tab")
export type CursorImportedConversation = {
	id: string; // Cursor tab id / composer id
	title: string; // Cursor chat title (may be '' for untitled chats)
	createdAt: string; // ISO string
	updatedAt: string; // ISO string (preferred for lastModified sorting)
	workspaceFolder: string; // decoded local workspace folder ('' if remote/unknown)
	workspaceLabel: string; // short label to display, eg "django-project-1c" or remote URI
	messages: CursorImportedMessage[];
};

export type CursorImportScanEntry = {
	workspaceFolder: string;
	workspaceLabel: string;
	conversationCount: number;
};

// result of an automatic scan of Cursor's storage
export type CursorImportScanResult = {
	cursorFound: boolean;
	cursorDataPath: string | null;
	workspaceCount: number;
	conversationCount: number;
	// conversations that live in the currently open workspace folder (or remote workspace)
	currentWorkspaceConversations: number;
	entries: CursorImportScanEntry[];
};

export type CursorImportReadResult = {
	cursorFound: boolean;
	cursorDataPath: string | null;
	conversations: CursorImportedConversation[];
	error?: string;
};