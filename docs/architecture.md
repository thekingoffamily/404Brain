# Архитектура Brain (v1.7.0)

## Обзор

404Brain — форк `code-oss-dev` (VS Code) **1.99.3** со встроенным ИИ-помощником «Brain»:
чат в сайдбаре (Chat / Agent / Gather режимы), FIM-автодополнение (Ctrl+K зона), правка кода через тулзы,
MCP-серверы, `.brainrules` / `.brainskills`, импорт из Cursor.

Версии: `product.json` → `brainVersion` (сейчас **1.7.0**), `brainRelease` (сейчас **0049**).

## Ключевые папки

Относительно `src/vs/workbench/contrib/brain/`:

```
browser/
  chatThreadService.ts          — треды: сообщения, стриминг, инструменты, undo, checkpoint-ы, importThreads
  convertToLLMMessageService.ts — конвертация чат-сообщений в формат LLM, чтение .brainrules/.brainskills, системное сообщение
  toolsService.ts               — исполнение builtin-тулзов (read/ls/search/edit/terminal/editor-context)
  terminalToolService.ts        — постоянные и временные терминалы
  editCodeService.ts            — inline-правка (Ctrl+K зона), search/replace blocks
  brainCommandBarService.ts     — командный бар (Ctrl+L / Ctrl+K), стриминг
  autocompleteService.ts        — FIM/автодополнение
  electron-main/mcpChannel.ts   — IPC-сервер MCP
  electron-main/cursorImportChannel.ts — импорт из Cursor (scan/read/importRules)
common/
  brainSettingsService.ts       — настройки и провайдеры (глобальные + per-provider)
  brainSettingsTypes.ts         — типы настроек, FeatureName, провайдеры
  sendLLMMessageService.ts      — отправка и стриминг к провайдерам
  sendLLMMessageTypes.ts        — типы сообщений LLM (OpenAI/Anthropic/Gemini/XML)
  mcpService.ts                 — MCP серверы
  modelCapabilities.ts          — возможности моделей (reasoning, context, output)
  chatThreadServiceTypes.ts     — типы чата (ChatMessage, ToolMessage…)
  toolsServiceTypes.ts          — типы тулзов (BuiltinToolCallParams / BuiltinToolResultType)
  cursorImportService.ts        — клиентский сервис импорта Cursor
  prompt/prompts.ts             — банк промптов, builtinTools, system message, агент-регламенты
browser/react/src/
  sidebar-tsx/SidebarChat.tsx   — главный компонент чата
  brain-settings-tsx/Settings.tsx — панель настроек (вкладки GPT..MCP, AI Instructions)
  markdown/                     — рендер markdown
  util/inputs.tsx, services.tsx — react-обёртки
```

## Поток данных

### Добавление сообщения в тред
Единственная точка записи `allThreads[threadId].messages` — `_addMessageToThread(threadId, msg)`
в `chatThreadService.ts` (+ `_storeAllThreads` для персистенции). Редактирование — `_editMessageInThread`.

### Как подмешиваются инструкции к LLM
`convertToLLMMessageService.ts`:
- `_getCombinedAIInstructions()` = `aiInstructions` из настроек + `.brainrules` + `.brainskills/*.md`;
- результат попадает в системное сообщение (GUIDELINES) и FIM-префикс.

### Тулзы
`toolsService.ts` (`IToolsService`):
- `validateParams` — преобразование сырых params от LLM (snake_case) в безопасные типы;
- `callTool` — исполнение; возвращает `{ result, interruptTool }`;
- `stringOfResult` — сериализация результата в текст для LLM.

Новые тулзы добавляются в 4 местах:
1. `toolsServiceTypes.ts` → `BuiltinToolCallParams` / `BuiltinToolResultType` (+ `approvalTypeOfBuiltinToolName`, если тулз требует одобрения, напр. `get_git_status` → `terminal`);
2. `browser/toolsService.ts` → `validateParams`, `callTool`, `stringOfResult`;
3. `common/prompt/prompts.ts` → `builtinTools` (описание + параметры). Без этого шага TS-проверка `satisfies` не соберётся;
4. `docs/tools-and-skills.md` → актуализировать каталог.

## Темы и иконки (v1.7.0)

- Дефолты задаются константами `ThemeSettingDefaults` в
  `src/vs/workbench/services/themes/common/workbenchThemeService.ts`:
  `COLOR_THEME_DARK = 'Bearded Theme Coffee'`, `FILE_ICON_THEME = 'bearded-icons'`,
  `COLOR_THEME_DARK_OLD = 'Default Dark+'` (для миграции старых профилей).
- `settingsId` темы = `theme.id || label` (`colorThemeData.ts` → `fromExtensionTheme`).
  У пакета темы нет `id`, поэтому важен точный `label` из `extensions/beardedtheme/package.json` → `"Bearded Theme Coffee"`.
- Иконки: `extensions/beardedicons/package.json` → `contributes.iconThemes[].id = "bearded-icons"`.
- Локальные темы лежат в `extensions/beardedtheme` и `extensions/beardedicons` и автоматически пакуются в продукт
  из `extensions/*/package.json` (`build/lib/extensions.js` → `packageNonNativeLocalExtensionsStream`).
- При сборке тематических расширений из package.json убираются scripts/dependencies/devDependencies
  (иначе сборщик пробует устанавливать npm-зависимости); сами темы — статический JSON без кода.

## Импорт из Cursor (v1.6.2)

- Локация чатов Cursor: `%APPDATA%\Cursor\User\workspaceStorage\<hash>\state.vscdb` (SQLite).
  Ключ `workbench.panel.aichat.view.aichat.chatdata` → JSON `tabs[]` → `bubbles[]` (user/ai с `text`).
  Папка воркспейса — `workspace.json` → `folder` (`file:///...`).
- Читаем через `@vscode/sqlite3` с `PRAGMA query_only=ON`.
- Архитектура: main-процесс `electron-main/cursorImportChannel.ts` (команды scan/read/importRules) +
  renderer `common/cursorImportService.ts` (канал `brain-channel-cursorImport`, dedupe по `brain.cursorImport.seenIds`).
- Rules: `.cursorrules` + `.cursor/rules/*.mdc` + глобальные `~/.cursor/rules` → `.brainrules`.
- UI: баннер `sidebar-tsx/CursorImportBanner.tsx` + секция в Settings.tsx.