/*--------------------------------------------------------------------------------------
 *  Copyright 2025 Glass Devtools, Inc. All rights reserved.
 *  Licensed under the Apache License, Version 2.0. See LICENSE.txt for more information.
 *--------------------------------------------------------------------------------------*/

import { endsWithAnyPrefixOf, SurroundingsRemover } from '../../common/helpers/extractCodeFromResult.js'
import { availableTools, InternalToolInfo } from '../../common/prompt/prompts.js'
import { OnFinalMessage, OnText, RawToolCallObj, RawToolParamsObj } from '../../common/sendLLMMessageTypes.js'
import { ToolName, ToolParamName } from '../../common/toolsServiceTypes.js'
import { ChatMode } from '../../common/brainSettingsTypes.js'


// =============== reasoning ===============

// could simplify this - this assumes we can never add a tag without committing it to the user's screen, but that's not true
export const extractReasoningWrapper = (
	onText: OnText, onFinalMessage: OnFinalMessage, thinkTags: [string, string]
): { newOnText: OnText, newOnFinalMessage: OnFinalMessage } => {
	let latestAddIdx = 0 // exclusive index in fullText_
	let foundTag1 = false
	let foundTag2 = false

	let fullTextSoFar = ''
	let fullReasoningSoFar = ''


	if (!thinkTags[0] || !thinkTags[1]) throw new Error(`thinkTags must not be empty if provided. Got ${JSON.stringify(thinkTags)}.`)

	let onText_ = onText
	onText = (params) => {
		onText_(params)
	}

	const newOnText: OnText = ({ fullText: fullText_, ...p }) => {

		// until found the first think tag, keep adding to fullText
		if (!foundTag1) {
			const endsWithTag1 = endsWithAnyPrefixOf(fullText_, thinkTags[0])
			if (endsWithTag1) {
				// console.log('endswith1', { fullTextSoFar, fullReasoningSoFar, fullText_ })
				// wait until we get the full tag or know more
				return
			}
			// if found the first tag
			const tag1Index = fullText_.indexOf(thinkTags[0])
			if (tag1Index !== -1) {
				// console.log('tag1Index !==1', { tag1Index, fullTextSoFar, fullReasoningSoFar, thinkTags, fullText_ })
				foundTag1 = true
				// Add text before the tag to fullTextSoFar
				fullTextSoFar += fullText_.substring(0, tag1Index)
				// Update latestAddIdx to after the first tag
				latestAddIdx = tag1Index + thinkTags[0].length
				onText({ ...p, fullText: fullTextSoFar, fullReasoning: fullReasoningSoFar })
				return
			}

			// console.log('adding to text A', { fullTextSoFar, fullReasoningSoFar })
			// add the text to fullText
			fullTextSoFar = fullText_
			latestAddIdx = fullText_.length
			onText({ ...p, fullText: fullTextSoFar, fullReasoning: fullReasoningSoFar })
			return
		}

		// at this point, we found <tag1>

		// until found the second think tag, keep adding to fullReasoning
		if (!foundTag2) {
			const endsWithTag2 = endsWithAnyPrefixOf(fullText_, thinkTags[1])
			if (endsWithTag2 && endsWithTag2 !== thinkTags[1]) { // if ends with any partial part (full is fine)
				// console.log('endsWith2', { fullTextSoFar, fullReasoningSoFar })
				// wait until we get the full tag or know more
				return
			}

			// if found the second tag
			const tag2Index = fullText_.indexOf(thinkTags[1], latestAddIdx)
			if (tag2Index !== -1) {
				// console.log('tag2Index !== -1', { fullTextSoFar, fullReasoningSoFar })
				foundTag2 = true
				// Add everything between first and second tag to reasoning
				fullReasoningSoFar += fullText_.substring(latestAddIdx, tag2Index)
				// Update latestAddIdx to after the second tag
				latestAddIdx = tag2Index + thinkTags[1].length
				onText({ ...p, fullText: fullTextSoFar, fullReasoning: fullReasoningSoFar })
				return
			}

			// add the text to fullReasoning (content after first tag but before second tag)
			// console.log('adding to text B', { fullTextSoFar, fullReasoningSoFar })

			// If we have more text than we've processed, add it to reasoning
			if (fullText_.length > latestAddIdx) {
				fullReasoningSoFar += fullText_.substring(latestAddIdx)
				latestAddIdx = fullText_.length
			}

			onText({ ...p, fullText: fullTextSoFar, fullReasoning: fullReasoningSoFar })
			return
		}

		// at this point, we found <tag2> - content after the second tag is normal text
		// console.log('adding to text C', { fullTextSoFar, fullReasoningSoFar })

		// Add any new text after the closing tag to fullTextSoFar
		if (fullText_.length > latestAddIdx) {
			fullTextSoFar += fullText_.substring(latestAddIdx)
			latestAddIdx = fullText_.length
		}

		onText({ ...p, fullText: fullTextSoFar, fullReasoning: fullReasoningSoFar })
	}


	const getOnFinalMessageParams = () => {
		const fullText_ = fullTextSoFar
		const tag1Idx = fullText_.indexOf(thinkTags[0])
		const tag2Idx = fullText_.indexOf(thinkTags[1])
		if (tag1Idx === -1) return { fullText: fullText_, fullReasoning: '' } // never started reasoning
		if (tag2Idx === -1) return { fullText: '', fullReasoning: fullText_ } // never stopped reasoning

		const fullReasoning = fullText_.substring(tag1Idx + thinkTags[0].length, tag2Idx)
		const fullText = fullText_.substring(0, tag1Idx) + fullText_.substring(tag2Idx + thinkTags[1].length, Infinity)

		return { fullText, fullReasoning }
	}

	const newOnFinalMessage: OnFinalMessage = (params) => {

		// treat like just got text before calling onFinalMessage (or else we sometimes miss the final chunk that's new to finalMessage)
		newOnText({ ...params })

		const { fullText, fullReasoning } = getOnFinalMessageParams()
		onFinalMessage({ ...params, fullText, fullReasoning })
	}

	return { newOnText, newOnFinalMessage }
}


// =============== tools (XML) ===============



const findPartiallyWrittenToolTagAtEnd = (fullText: string, toolTags: string[]) => {
	for (const toolTag of toolTags) {
		const foundPrefix = endsWithAnyPrefixOf(fullText, toolTag)
		if (foundPrefix) {
			return [foundPrefix, toolTag] as const
		}
	}
	return false
}

const findIndexOfAny = (fullText: string, matches: string[]) => {
	for (const str of matches) {
		const idx = fullText.indexOf(str);
		if (idx !== -1) {
			return [idx, str] as const
		}
	}
	return null
}


type ToolOfToolName = { [toolName: string]: InternalToolInfo | undefined }
const parseXMLPrefixToToolCall = <T extends ToolName,>(toolName: T, toolId: string, str: string, toolOfToolName: ToolOfToolName): RawToolCallObj => {
	const paramsObj: RawToolParamsObj = {}
	const doneParams: ToolParamName<T>[] = []
	let isDone = false

	const getAnswer = (): RawToolCallObj => {
		// trim off all whitespace at and before first \n and after last \n for each param
		for (const p in paramsObj) {
			const paramName = p as ToolParamName<T>
			const orig = paramsObj[paramName]
			if (orig === undefined) continue
			paramsObj[paramName] = trimBeforeAndAfterNewLines(orig)
		}

		// return tool call
		const ans: RawToolCallObj = {
			name: toolName,
			rawParams: paramsObj,
			doneParams: doneParams,
			isDone: isDone,
			id: toolId,
		}
		return ans
	}

	// find first toolName tag
	const openToolTag = `<${toolName}>`
	let i = str.indexOf(openToolTag)
	if (i === -1) return getAnswer()
	let j = str.lastIndexOf(`</${toolName}>`)
	if (j === -1) j = Infinity
	else isDone = true


	str = str.substring(i + openToolTag.length, j)

	const pm = new SurroundingsRemover(str)

	const allowedParams = Object.keys(toolOfToolName[toolName]?.params ?? {}) as ToolParamName<T>[]
	if (allowedParams.length === 0) return getAnswer()
	let latestMatchedOpenParam: null | ToolParamName<T> = null
	let n = 0
	while (true) {
		n += 1
		if (n > 10) return getAnswer() // just for good measure as this code is early

		// find the param name opening tag
		let matchedOpenParam: null | ToolParamName<T> = null
		for (const paramName of allowedParams) {
			const removed = pm.removeFromStartUntilFullMatch(`<${paramName}>`, true)
			if (removed) {
				matchedOpenParam = paramName
				break
			}
		}
		// if did not find a new param, stop
		if (matchedOpenParam === null) {
			if (latestMatchedOpenParam !== null) {
				paramsObj[latestMatchedOpenParam] += pm.value()
			}
			return getAnswer()
		}
		else {
			latestMatchedOpenParam = matchedOpenParam
		}

		paramsObj[latestMatchedOpenParam] = ''

		// find the param name closing tag
		let matchedCloseParam: boolean = false
		let paramContents = ''
		for (const paramName of allowedParams) {
			const i = pm.i
			const closeTag = `</${paramName}>`
			const removed = pm.removeFromStartUntilFullMatch(closeTag, true)
			if (removed) {
				const i2 = pm.i
				paramContents = pm.originalS.substring(i, i2 - closeTag.length)
				matchedCloseParam = true
				break
			}
		}
		// if did not find a new close tag, stop
		if (!matchedCloseParam) {
			paramsObj[latestMatchedOpenParam] += pm.value()
			return getAnswer()
		}
		else {
			doneParams.push(latestMatchedOpenParam)
		}

		paramsObj[latestMatchedOpenParam] += paramContents
	}
}

export const extractXMLToolsWrapper = (
	onText: OnText,
	onFinalMessage: OnFinalMessage,
	chatMode: ChatMode | null,
	mcpTools: InternalToolInfo[] | undefined,
): { newOnText: OnText, newOnFinalMessage: OnFinalMessage } => {

	if (!chatMode) return { newOnText: onText, newOnFinalMessage: onFinalMessage }
	const tools = availableTools(chatMode, mcpTools)
	if (!tools) return { newOnText: onText, newOnFinalMessage: onFinalMessage }

	const toolOfToolName: ToolOfToolName = {}
	const toolOpenTags = tools.map(t => `<${t.name}>`)
	for (const t of tools) { toolOfToolName[t.name] = t }
	const toolNames = tools.map(t => t.name)

	// normalize sloppy model output so tool calls are recognized:
	// 1) strip wrapper tags some models put around a call (<tool_call>, <invoke>, ...)
	// 2) fix a missing '<' on the opening tag: `read_file>` -> `<read_file>` (only for known tool names)
	const sanitizeToolStream = (s: string): string => {
		let out = s.replace(/<\/?(?:tool_call|tool_use|function_call|invoke|result)\b[^>]*>/gi, '')
		for (const name of toolNames) {
			out = out.replace(new RegExp(`(^|\\n)${name}>`, 'g'), `$1<${name}>`)
		}
		return out
	}

	// detect <availableTools[0]></availableTools[0]>, etc.
	// Multiple tool calls are supported: the model may batch several consecutive calls in ONE response
	// (<read_file>...</read_file><read_file>...</read_file>...). They all get parsed here and returned as `toolCalls`.
	let fullText = '';
	let trueFullText = ''
	let latestToolCall: RawToolCallObj | undefined = undefined // the currently-streaming (or most recent) tool call, for live UI
	let completedToolCalls: RawToolCallObj[] = [] // every fully-closed tool call seen so far

	let foundOpenTag: { idx: number, toolName: ToolName, id: string } | null = null
	let openToolTagBuffer = '' // the characters we've seen so far that come after a < with no space afterwards, not yet added to fullText

	let prevFullTextLen = 0

	// feed raw text into the visible buffer. Halfway-written <tags> are withheld until they resolve.
	// Each tool call gets a unique id derived from its position (stable across chunks AND across rescans).
	const consumeVisibleChunk = (chunk: string): { open: { idx: number, toolName: ToolName, id: string } | null } => {
		const combined = openToolTagBuffer + chunk
		const isPartial = findPartiallyWrittenToolTagAtEnd(combined, toolOpenTags)
		if (isPartial) {
			openToolTagBuffer = combined
			return { open: null }
		}
		// not a partial tag, so commit the whole chunk as visible text, then check for a tool tag
		fullText += combined
		openToolTagBuffer = ''
		const i = findIndexOfAny(fullText, toolOpenTags)
		if (i !== null) {
			const [idx, toolTag] = i
			const toolName = toolTag.substring(1, toolTag.length - 1) as ToolName
			// do not count anything at or after i in fullText
			fullText = fullText.substring(0, idx)
			return { open: { idx, toolName, id: `call_${toolName}_${idx}` } }
		}
		return { open: null }
	}

	const newOnText: OnText = (params) => {
		const sanitizedFullText = sanitizeToolStream(params.fullText)
		const newText = sanitizedFullText.substring(prevFullTextLen)
		prevFullTextLen = sanitizedFullText.length
		trueFullText = sanitizedFullText

		// if we're not inside a tool call, absorb the new text and look for an opening tag
		if (foundOpenTag === null) {
			const { open } = consumeVisibleChunk(newText)
			if (open) foundOpenTag = open
		}

		// process (possibly several) complete tool calls the model batched consecutively
		let guard = 0
		while (foundOpenTag) {
			if (guard++ > 50) break // safety net

			// parse ONLY up to this call's own closing tag, so consecutive same-name calls don't pollute each other
			const closeTag = `</${foundOpenTag.toolName}>`
			const block = trueFullText.substring(foundOpenTag.idx)
			const closeIdx = block.indexOf(closeTag)
			const blockText = closeIdx === -1 ? block : block.substring(0, closeIdx + closeTag.length)
			const call = parseXMLPrefixToToolCall(foundOpenTag.toolName, foundOpenTag.id, blockText, toolOfToolName)
			latestToolCall = call
			if (!call.isDone) break // still streaming this call

			// this call is fully closed - park it and re-scan what follows it
			completedToolCalls.push(call)
			const closeEndIdx = foundOpenTag.idx + (closeIdx === -1 ? block.length : closeIdx + closeTag.length)
			foundOpenTag = null

			const { open } = consumeVisibleChunk(trueFullText.substring(closeEndIdx))
			if (open) foundOpenTag = open
			else latestToolCall = undefined
		}

		onText({
			...params,
			fullText,
			toolCall: latestToolCall,
			toolCalls: completedToolCalls.length ? [...completedToolCalls] : undefined,
		});
	};


	// deterministic re-scan of the final stream: recomputes every complete call and the (possible) trailing open call,
	// regardless of how the incremental parser buffered partial tags along the way.
	const rescanAllToolCalls = () => {
		fullText = ''
		completedToolCalls = []
		latestToolCall = undefined
		let inProgress = false
		const s = trueFullText
		const n = s.length
		let pos = 0
		while (pos < n) {
			// find the next opening tag after pos
			let bestIdx = -1
			let bestName = ''
			for (const name of toolNames) {
				const tag = `<${name}>`
				const idx = s.indexOf(tag, pos)
				if (idx !== -1 && (bestIdx === -1 || idx < bestIdx)) { bestIdx = idx; bestName = name }
			}
			if (bestIdx === -1) {
				fullText += s.substring(pos)
				break
			}
			// visible text before the tool call
			fullText += s.substring(pos, bestIdx)
			const name = bestName as ToolName
			const id = `call_${name}_${bestIdx}`
			const closeIdx = s.indexOf(`</${name}>`, bestIdx + name.length + 2)
			if (closeIdx === -1) {
				// unfinished call at the very end - keep it (matches prior behavior)
				inProgress = true
				latestToolCall = parseXMLPrefixToToolCall(name, id, s.substring(bestIdx), toolOfToolName)
				break
			}
			const closeEndIdx = closeIdx + name.length + 3
			completedToolCalls.push(parseXMLPrefixToToolCall(name, id, s.substring(bestIdx, closeEndIdx), toolOfToolName))
			pos = closeEndIdx
		}
		// withhold a half-written tool tag at the very end of the visible text
		const partial = findPartiallyWrittenToolTagAtEnd(fullText, toolOpenTags)
		if (partial) fullText = fullText.substring(0, fullText.length - partial[0].length)
		if (!inProgress) latestToolCall = undefined
	}


	const newOnFinalMessage: OnFinalMessage = (params) => {
		// treat like just got text before calling onFinalMessage (or else we sometimes miss the final chunk that's new to finalMessage)
		newOnText({ ...params })

		// exact pass over the whole stream; this is what we return to the agent loop
		rescanAllToolCalls()

		fullText = fullText.trimEnd()
		const additional = latestToolCall ? [latestToolCall] : []
		const toolCalls = (completedToolCalls.length || additional.length) ? [...completedToolCalls, ...additional] : undefined
		const toolCall = toolCalls?.[toolCalls.length - 1]

		onFinalMessage({ ...params, fullText, toolCall, toolCalls })
	}
	return { newOnText, newOnFinalMessage };
}



// trim all whitespace up until the first newline, and all whitespace up until the last newline
const trimBeforeAndAfterNewLines = (s: string) => {
	if (!s) return s;

	const firstNewLineIndex = s.indexOf('\n');

	if (firstNewLineIndex !== -1 && s.substring(0, firstNewLineIndex).trim() === '') {
		s = s.substring(firstNewLineIndex + 1, Infinity)
	}

	const lastNewLineIndex = s.lastIndexOf('\n');
	if (lastNewLineIndex !== -1 && s.substring(lastNewLineIndex + 1, Infinity).trim() === '') {
		s = s.substring(0, lastNewLineIndex)
	}

	return s
}
