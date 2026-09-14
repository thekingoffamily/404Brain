// Normally you'd want to put these exports in the files that register them, but if you do that you'll get an import order error if you import them in certain cases.
// (importing them runs the whole file to get the ID, causing an import error). I guess it's best practice to separate out IDs, pretty annoying...

export const BRAIN_CTRL_L_ACTION_ID = 'brain.ctrlLAction'

export const BRAIN_CTRL_K_ACTION_ID = 'brain.ctrlKAction'

export const BRAIN_ACCEPT_DIFF_ACTION_ID = 'brain.acceptDiff'

export const BRAIN_REJECT_DIFF_ACTION_ID = 'brain.rejectDiff'

export const BRAIN_GOTO_NEXT_DIFF_ACTION_ID = 'brain.goToNextDiff'

export const BRAIN_GOTO_PREV_DIFF_ACTION_ID = 'brain.goToPrevDiff'

export const BRAIN_GOTO_NEXT_URI_ACTION_ID = 'brain.goToNextUri'

export const BRAIN_GOTO_PREV_URI_ACTION_ID = 'brain.goToPrevUri'

export const BRAIN_ACCEPT_FILE_ACTION_ID = 'brain.acceptFile'

export const BRAIN_REJECT_FILE_ACTION_ID = 'brain.rejectFile'

export const BRAIN_ACCEPT_ALL_DIFFS_ACTION_ID = 'brain.acceptAllDiffs'

export const BRAIN_REJECT_ALL_DIFFS_ACTION_ID = 'brain.rejectAllDiffs'
