# AGENTS.md — руководство для агентов по проекту 404Brain

Этот файл — единственная точка входа для любого агента (LLM), работающего с репозиторием.
Читай его ПЕРЕДЛО любых правок. После каждой заметной сессии обновляй раздел «История работ».

---

## 🔒 ГЛАВНОЕ ПРАВИЛО — КЛЮЧИ

**КЛЮЧИ, ТОКЕНЫ, СЕКРЕТЫ НИКОГДА И НИГДЕ НЕ СВЕТИМ!**

- API-ключи пользователей хранятся ТОЛЬКО в settings 404Brain (идеал — SecretStorage, `ISecretStorageService`).
- НИКОГДА: не логировать ключи, не писать их в файлы, не вставлять в код/референсы/артефакты/коммиты/релизы/статьи.
- При изменении кода, где фигурируют ключи — только ссылки на имена полей/переменных, никогда реальные значения.
- Перед `git add` убедись, что в диффе нет ключей. Перед публикацией релиза/статьи — ещё раз перепроверь.
- В валидном коде проекта ключи представлены плейсхолдерами: `apiKey: ''` / `undefined`. Не ломай эту схему.

---

## Суть проекта

404Brain — форк `code-oss-dev` (базовый VS Code) **1.99.3**, в который встроен ИИ-помощник «Brain»:
чат в сайдбаре, Agent mode, правка кода, FIM (autocomplete) в редакторе, поддержка многих провайдеров
(OpenAI, Anthropic, Gemini, DeepSeek и др.), MCP-серверы, `.brainrules` и `.brainskills`.

Версия продукта: `product.json` → `brainVersion` (сейчас **1.6.1**), `brainRelease` (сейчас **0047**).

---

## ⚠️ Критично про сборку react-части

Весь React-код живёт в `src/vs/workbench/contrib/brain/browser/react/src/**` (**источник — ТОЛЬКО сюда!**).

- Правки вносятся ТОЛЬКО в `react/src/**` (папки: `sidebar-tsx/`, `brain-settings-tsx/`, `markdown/`, `util/`, `quick-edit-tsx/`, `diff/`, `brain-editor-widgets-tsx/`, `brain-onboarding/`, `brain-tooltip/`).
- `npm run buildreact`:
  1. префиксует classNames (`brain-`) и CSS из `src/` → `src2/`
  2. собирает `src2/**` в бандлы `out/**` (tsup, esm)
- `src2/` и `out/` — **генерируемые, в .gitignore, ПРАВИТЬ НАПРЯМУЮ НЕЛЬЗЯ**. Любые изменения «не применяются» пока не сделан `npm run buildreact`.
- Схема: измени `react/src/...` → запусти `npm run buildreact` → изменения попадут в бандл.

### Быстрая проверка типов (без полной сборки)
- `npm run compile` — gulp-задача, проверяет TS по всему проекту ~5 мин. Ошибки вида `tsc` вернутся в лог.
- После ЛЮБОЙ правки `.ts`/`.tsx` вне react/src (browser/common сервисы) — обязательно `npm run compile`.

### Полная сборка Windows (долгая!)
- `$env:NODE_OPTIONS='--max-old-space-size=8192'` ; `npm run gulp vscode-win32-x64`
- Занимает ~25–35 минут. Выход: `C:\Users\palapalaru\Desktop\VSCode-win32-x64`
- После сборки можно упаковывать zip из этой папки (для релиза).

---

## Архитектура Brain (карта файлов)

Все папки — относительно `src/vs/workbench/contrib/brain/`:

```
browser/
  chatThreadService.ts          — треды: сообщения, стриминг, инструменты, undo, checkpoint-ы
  convertToLLMMessageService.ts — конвертация чат-сообщений в формат LLM (OpenAI/Anthropic/XML/Gemini),
                                  чтение .brainrules и .brainskills, системное сообщение
  convertToLLMMessageWorkbenchContrib.ts — инициализация моделей .brainrules / .brainskills при открытии воркспейса
  toolsService.ts               — встроенные инструменты (edit_file, rewrite_file, terminal и т.д.)
  terminalToolService.ts        — постоянные терминалы
  editCodeService.ts            — правка кода inline (Ctrl+K зона)
  brainCommandBarService.ts     — командный бар (Ctrl+L / Ctrl+K)
  electron-main/mcpChannel.ts   — IPC-cервер MCP (main process)
  react/                       — весь UI (см. ниже)
common/                         — сервисы, но доступные и из main
  brainSettingsService.ts       — настройки и провайдеры (глобальные настройки + per-provider)
  brainSettingsTypes.ts         — типы настроек, инфа о провайдерах/фичах
  chatThreadServiceTypes.ts     — типы сообщений (ChatMessage, BrainChatImage, ToolMessage...)
  sendLLMMessageTypes.ts        — типы сообщений LLM (OpenAI/Anthropic/Gemini форматы)
  sendLLMMessageService.ts      — отправка и стриминг к провайдерам
  mcpService.ts / mcpServiceTypes.ts — MCP серверы (конфиг-файл, серверы, тулы)
  brainModelService.ts          — менеджер текстовых моделей (используется для чтения .brainrules/.brainskills)
  prompt/prompts.ts             — банк промптов + InternalToolInfo + system message
  refreshModelService.ts, modelCapabilities.ts, helpers/...
browser/react/src/
  sidebar-tsx/SidebarChat.tsx   — главный компонент чата (ввод, баблы, картинки, меню "Add"…)
  brain-settings-tsx/Settings.tsx — панель настроек в сайдбаре (вкладки: GPT->MCP, AI Instructions и т.д.)
  markdown/ChatMarkdownRender.tsx — рендер markdown в баблах
  util/inputs.tsx               — BrainInputBox2, кнопки, слайдеры, дропдауны
  util/services.tsx             — react-обёртки над VS Code сервисами (useAccessor и т.д.)
```

### Ключевые сервисы из React (`useAccessor`)
`IFileService`, `IWorkspaceContextService`, `ICommandService`, `INotificationService`, `IBrainModelService`,
`IMCPService`, `IChatThreadService`, `IEditorService`, `IConvertToLLMMessageService`, `IBrainSettingsService` и др.
`_registerAccessor` в `util/services.tsx` — там определяется, какие сервисы доступны.

### Добавление сообщения в тред
Единственная точка записи в `allThreads[threadId].messages` — `_addMessageToThread(threadId, msg)` в `chatThreadService.ts`
(плюс `_storeAllThreads` для персистенции). Редактирование существующего — `_editMessageInThread(threadId, idx, msg)`.

### Как подмешиваются инструкции к LLM
`convertToLLMMessageService.ts`:
- `_getCombinedAIInstructions()` объединяет: `aiInstructions` из настроек + содержимое `.brainrules` + содержимое `.brainskills/*.md`
- `_getBrainRulesFileContents()` — читает `.brainrules` в корне каждого воркспейс-фолдера
- `_getBrainSkillsFileContents()` — читает все `.md` из `.brainskills/` (модели инициализирует `convertToLLMMessageWorkbenchContrib.ts`)
- результат попадает в системное сообщение (GUIDELINES) и в FIM-префикс

### Картинки в чате (vision)
Поддерживается для OpenAI/Anthropic(полностью)/XML/Gemini. Хранятся как `BrainChatImage { dataUrl, name? }` в user-сообщении.
Конвертация: `openAIImageParts` / `anthropicImageParts` / `inlineData` (Gemini) в `convertToLLMMessageService.ts`.

---

## История работ

### [current] — сессия 1.6.1 (текущая)
Состояние: **готово к финальной сборке** (нужен `npm run gulp vscode-win32-x64`), релиз не сделан.

Сделано в этой сессии:
1. **Markdown-фикс** (`react/src/markdown/ChatMarkdownRender.tsx`): убран латекс-препроцессинг, добавлен `InlineTokens` (вложенные strong/em/del/blockquote/link/code), параметр `text/escape`.
2. **Картинки в чат**: типы `BrainChatImage`, `OpenAIUserContentPart`, `AnthropicImagePart/Source/MediaType`;
   `convertToLLMMessageService.ts` (`parseDataUrl`, `openAIImageParts`, `anthropicImageParts`, `mergeContent`);
   `chatThreadService.ts` (поле `images` у user-сообщения, проброс в `addUserMessageAndStreamResponse` и edit);
   `SidebarChat.tsx` (`StagingImages`, `AttachImagesButton`, Ctrl+V паста, `readFileAsDataUrl` + даунскейл до 1280px, макс 4 шт).
3. **Фикс очередности сообщений**: `_runToolCall` НЕ вставляет «running»-плейсхолдер в чат до выполнения;
   `_swapOutLatestStreamingToolWithResult` ищет последний tool-месседж с конца (пропуская checkpoint-ы);
   `SidebarChat.tsx`: стриминг-бабл только при `isRunning === 'LLM'`, лоадер и при `isRunning === 'tool'`.
4. **MCP/правила/скилы из чата**: компонент `AddStuffMenu` в `SidebarChat.tsx` (кнопка `+` у поля ввода):
   Attach image / Add MCP server (открывает mcp.json) / Create `.brainrules` / Create a skill (шаблон `.brainskills/example.md`).
   Создание файлов — через `IFileService` + `brainOpenFileFn`. После создания скила — `brainModelService.initializeModel` для мгновенного подхвата.
5. **Скилы реализованы**: `.brainskills/*.md` читаются и подмешиваются в системное сообщение.
   `brainModelService.ts`: добавлен `getModelFSPaths()`. `convertToLLMMessageWorkbenchContrib.ts`: инициализация моделей `.brainskills/*.md` (через `fileService.resolve`).
6. `Settings.tsx`: в раздел AI Instructions добавлено упоминание `.brainskills` папки.

Проверено: `npm run buildreact` ✅, `npm run compile` ✅ (0 ошибок).
**Ещё не сделано**: полная сборка win32-x64, zip, коммит/пуш, релиз `v1.6.1`, статьи.

### Прошлые сессии (кратко)
- **v1.6.0**: добавлены SSH/WSL extension API proposals, bump версия; бонусные фиксы markdown/UI. Релиз `v1.6.0` сделан.
- Более ранние: базовая система Brain (чат, agent, FIM, инструменты, MCP, настройки провайдеров).

---

## Релиз-процедура (подтверждённый рантайм)

1. Убедиться: `buildreact` + `compile` прошли.
2. Полная сборка: `$env:NODE_OPTIONS='--max-old-space-size=8192'`; `npm run gulp vscode-win32-x64` → `C:\Users\palapalaru\Desktop\VSCode-win32-x64`.
3. Выпустить zip (например `404Brain-win32-x64-1.6.1.zip`) из папки сборки.
4. Коммит с осмысленным сообщением, затем `git push` в `origin/main` (ветка `main`).
5. Релиз на GitHub: `gh release create v1.6.1 <zip>` + описание.
6. **Реф-ссылка партнёрская (обязательно в релизах\README\статьях): `https://aitunnel.ru/?r=52512`**
7. Статьи (vc.ru и Reddit) — черновики лежат в `articles/vc.ru/`, шаблон `_template.md`.

---

## Вкусы и стиль (чтобы было КРАСОТЬ)

- Хвост-классы: используются утилиты Tailwind-стиля с префиксом `brain-` (см. `styles.css`), например `bg-brain-bg-1`, `text-brain-fg-3`, `border-brain-border-3`. Смотри, как сделано рядом, и повторяй паттерн.
- Интерфейс на русском/английском смешанно; текст, обращённый к пользователю — по контексту.
- Логи на русском и английском допускаются, но БЕЗ секретов.
- Кода не комментируй лишнего; если нужен комментарий — короткий, по делу. (Правило из системного прома кода — не добавлять комментарии, если не просят — НЕ применимо к файлу AGENTS.md, он сам по себе документация.)