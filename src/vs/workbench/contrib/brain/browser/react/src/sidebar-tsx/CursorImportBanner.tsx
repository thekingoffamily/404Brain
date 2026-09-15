/*--------------------------------------------------------------------------------------
 *  Copyright 2025 Glass Devtools, Inc. All rights reserved.
 *  Licensed under the Apache License, Version 2.0. See LICENSE.txt for more information.
 *--------------------------------------------------------------------------------------*/

import { useEffect, useState } from 'react';
import { useAccessor } from '../util/services.js';
import { IconShell1 } from '../markdown/ApplyBlockHoverButtons.js';
import { Import, LoaderCircle, X } from 'lucide-react';

// auto-detects Cursor chats on the machine and offers a one-click full import
export const CursorImportBanner = ({ className = '' }: { className?: string }) => {
	const accessor = useAccessor()
	const cursorImportService = accessor.get('ICursorImportService')
	const notificationService = accessor.get('INotificationService')

	const [found, setFound] = useState(false)
	const [count, setCount] = useState(0)
	const [currentCount, setCurrentCount] = useState(0)
	const [dismissed, setDismissed] = useState(false)
	const [busy, setBusy] = useState(false)

	useEffect(() => {
		let alive = true
		cursorImportService.scan().then((res) => {
			if (!alive) return
			if (!res.cursorFound || res.conversationCount === 0 || cursorImportService.hasImportedBefore()) {
				setFound(false)
				return
			}
			setFound(true)
			setCount(res.conversationCount)
			setCurrentCount(res.currentWorkspaceConversations)
		})
		return () => { alive = false }
	}, [cursorImportService])

	if (!found || dismissed) return null

	const onImport = async () => {
		setBusy(true)
		const result = await cursorImportService.importFromCursor()
		setBusy(false)
		if (result.imported > 0) {
			notificationService.info(`Imported ${result.imported} chats from Cursor`)
			setDismissed(true)
		} else {
			notificationService.info(`Import from Cursor finished: ${result.imported} imported, ${result.skipped} skipped.${result.error ? ' ' + result.error : ''}`)
			if (!result.error) setDismissed(true)
		}
	}

	return (
		<div className={`mb-2 px-3 py-2 rounded border border-brain-border-2 bg-brain-bg-2 text-brain-fg-1 flex items-start gap-2 select-none ${className}`}>
			<Import className='flex-shrink-0 mt-0.5' size={14} />
			<div className='min-w-0 flex-1'>
				<div className='text-sm font-medium'>Import from Cursor</div>
				<div className='text-xs text-brain-fg-3'>
					Found {count} chats{currentCount > 0 ? ` (${currentCount} in this workspace)` : ''}. Import them all into 404Brain.
				</div>
				<button
					className='mt-1.5 inline-flex items-center gap-1 text-xs rounded border border-brain-border-3 px-2 py-0.5 hover:brightness-115 cursor-pointer disabled:opacity-50'
					onClick={onImport}
					disabled={busy}
				>
					{busy ? <LoaderCircle className='animate-spin' size={11} /> : null}
					{busy ? 'Importing…' : 'Import all'}
				</button>
			</div>
			<IconShell1
				Icon={X}
				className='size-[13px]'
				onClick={() => setDismissed(true)}
				data-tooltip-id='brain-tooltip'
				data-tooltip-place='top'
				data-tooltip-content='Dismiss'
			/>
		</div>
	)
}