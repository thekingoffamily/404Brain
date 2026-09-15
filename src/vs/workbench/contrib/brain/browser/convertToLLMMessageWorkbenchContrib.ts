/*--------------------------------------------------------------------------------------
 *  Copyright 2025 Glass Devtools, Inc. All rights reserved.
 *  Licensed under the Apache License, Version 2.0. See LICENSE.txt for more information.
 *--------------------------------------------------------------------------------------*/

import { Disposable } from '../../../../base/common/lifecycle.js';
import { URI } from '../../../../base/common/uri.js';
import { IWorkspaceContextService } from '../../../../platform/workspace/common/workspace.js';
import { IFileService } from '../../../../platform/files/common/files.js';
import { IWorkbenchContribution, registerWorkbenchContribution2, WorkbenchPhase } from '../../../common/contributions.js';
import { IBrainModelService } from '../common/brainModelService.js';

class ConvertContribWorkbenchContribution extends Disposable implements IWorkbenchContribution {
	static readonly ID = 'workbench.contrib.brain.convertcontrib'
	_serviceBrand: undefined;

	constructor(
		@IBrainModelService private readonly brainModelService: IBrainModelService,
		@IWorkspaceContextService private readonly workspaceContext: IWorkspaceContextService,
		@IFileService private readonly fileService: IFileService,
	) {
		super()

		const initializeURI = async (uri: URI) => {
			this.workspaceContext.getWorkspace()
			const brainRulesURI = URI.joinPath(uri, '.brainrules')
			this.brainModelService.initializeModel(brainRulesURI)

			// initialize all .md files in .brainskills folder as well
			const brainSkillsFolderURI = URI.joinPath(uri, '.brainskills')
			try {
				const folderStat = await this.fileService.resolve(brainSkillsFolderURI)
				for (const child of folderStat.children ?? []) {
					if (child.isFile && child.name.endsWith('.md')) {
						this.brainModelService.initializeModel(child.resource)
					}
				}
			} catch (e) {
				// .brainskills folder doesn't exist yet, that's fine
			}
		}

		// call
		this._register(this.workspaceContext.onDidChangeWorkspaceFolders((e) => {
			[...e.changed, ...e.added].forEach(w => { initializeURI(w.uri) })
		}))
		this.workspaceContext.getWorkspace().folders.forEach(w => { initializeURI(w.uri) })
	}
}


registerWorkbenchContribution2(ConvertContribWorkbenchContribution.ID, ConvertContribWorkbenchContribution, WorkbenchPhase.BlockRestore);
