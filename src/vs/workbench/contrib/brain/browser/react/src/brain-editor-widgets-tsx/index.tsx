/*--------------------------------------------------------------------------------------
 *  Copyright 2025 Glass Devtools, Inc. All rights reserved.
 *  Licensed under the Apache License, Version 2.0. See LICENSE.txt for more information.
 *--------------------------------------------------------------------------------------*/

import { mountFnGenerator } from '../util/mountFnGenerator.js'
import { BrainCommandBarMain } from './BrainCommandBar.js'
import { BrainSelectionHelperMain } from './BrainSelectionHelper.js'

export const mountBrainCommandBar = mountFnGenerator(BrainCommandBarMain)

export const mountBrainSelectionHelper = mountFnGenerator(BrainSelectionHelperMain)

