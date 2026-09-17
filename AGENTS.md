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

## 🔒 ВТОРОЕ ПРАВИЛО — ПОМНИТЬ И ЗАПИСЫВАТЬ

**ВСЕГДА, ДЛЯ ВСЕХ — ВСЁ ЗАПОМИНАТЬ И КЕЙСЫ ВСЕ ЗАПИСЫВАТЬ (что к чему).**

- Каждая важная механика/факт/архитектурное решение/найденный формат данных должен быть зафиксирован,
  а не жить только в голове/контексте.
- Факты про чужой софт (как хранит данные Cursor/другие приложения), форматы, найденные баги, рецепты —
  складывай в AGENTS.md (или отдельные заметки в репо). Кейсы — «что к чему». Потом это экономит часы.
- При открытии новой сессии перечитывай AGENTS.md перед правками.

---

## Суть проекта

404Brain — форк `code-oss-dev` (базовый VS Code) **1.99.3**, в который встроен ИИ-помощник «Brain»:
чат в сайдбаре, Agent mode, правка кода, FIM (autocomplete) в редакторе, поддержка многих провайдеров
(OpenAI, Anthropic, Gemini, DeepSeek и др.), MCP-серверы, `.brainrules` и `.brainskills`.

Версия продукта: `product.json` → `brainVersion` (сейчас **1.7.1**), `brainRelease` (сейчас **0050**).

---

## 📚 Документация — docs/

Подробные MD-заметки лежат в `docs/` (читай при разборе задач):
- `docs/architecture.md` — карта файлов, потоки данных, темы/иконки, импорт Cursor.
- `docs/tools-and-skills.md` — полный каталог builtin-тулзов и комбо-паттерны (умения).
- `docs/build-and-run.md` — сборка, релиз, разворот на новом ПК.

При добавлении новых тулзов/механик — актуализируй docs/.

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
  brainCommandBarService.ts     — командный бар (Ctrl+L / Ctrl/K)
  electron-main/mcpChannel.ts   — IPC-cервер MCP (main process)
  electron-main/cursorImportChannel.ts — IPC-импорт из Cursor (сканирует state.vscdb, читает чаты/rules)
  react/                       — весь UI (см. ниже)
common/                         — сервисы, но доступные и из main
  brainSettingsService.ts       — настройки и провайдеры (глобальные настройки + per-provider)
  brainSettingsTypes.ts         — типы настроек, инфа о провайдерах/фичах
  cursorImportService.ts / cursorImportServiceTypes.ts — клиентский сервис импорта из Cursor (канал brain-channel-cursorImport)
  chatThreadServiceTypes.ts     — типы сообщений (ChatMessage, BrainChatImage, ToolMessage...) + DI-токен IChatThreadService
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

### ⚠️ Правило слоёв common ↔ browser (иначе серый экран при старте!)
- **common модули НЕ могут runtime-импортировать НИЧЕГО из browser/** (разрешён только `import type`).
  Иначе esbuild (бандл `workbench.desktop.main.js`) получает цикл common↔browser и кладёт модуль
  browser ПОСЛЕ его использования → токен = `undefined` → `TypeError: decorator is not a function`
  при загрузке workbench (серое окно).
- DI-токены (createDecorator) клади в `common/` (например `IChatThreadService` — в `chatThreadServiceTypes.ts`),
  browser-реализация делает `export const IChatThreadService = IChatThreadServiceToken` (ре-экспорт).
- Диагностика краша: grep в `workbench.desktop.main.js` — если `createDecorator("...")` объявлен строкой ПОЗЖЕ,
  чем `__param(N, ...)` его использует — это тот самый цикл.
- Второй сценарий серого экрана: `process.platform/env/...` в common/browser-модуле — sandbox-рендерер
  НЕ имеет `process` (ReferenceError). Используй `isWindows` из `base/common/platform.js` и т.п.

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

### [current] — сессия 2.1.0 (завершена)
Состояние: **релиз v1.7.4 выпущен** (404Brain-win32-x64-1.7.4.zip, tag v1.7.4, product 1.7.4/0053, commit `64092b2c`).

Сделано в этой сессии:
1. **Починены тулзы в чате (агент «умирал» и не читал файлы)**. Симптом: агент писал тул-вызовы как
   `<tool_call>read_file> <uri>…</uri></read_file>` (обёртка `<tool_call>` + открывающий тег БЕЗ `<`, `read_file>`
   вместо `<read_file>`) — парсер `extractGrammar.ts` искал строго `<read_file>`, не находил, тул никогда не исполнялся.
   - **Парсер (толерантность)** `extractGrammar.ts` `extractXMLToolsWrapper`: добавлена `sanitizeToolStream()` —
     выкидывает обёртки `<tool_call>`/`<tool_use>`/`<function_call>`/`<invoke>`/`<result>` и конвертирует `read_file>`
     → `<read_file>` ТОЛЬКО для известных имён тулов на старте строки (ложных срабатываний нет — проверено на строке из чата).
   - **Промпт** `prompts.ts` `<tool_calling>`: жёсткая EXACT-спека формата с примером (`<read_file>` … `</read_file>`),
     запрет `<tool_call>`-обёртки и лишнего `>` после имени, только перечисленные имена параметров.
2. **compile** ✅ (0 ошибок), desktop-сборка ✅ (14 мин), проверено в бандле: `sanitizeToolStream` (main.js),
   «EXACT tool call format» (workbench.desktop.main.js), product 1.7.4/0053.

### Постфикс сессии 2.1.0 — REH-тар перепатчен на `64092b2c`
- Новый desktop собран из HEAD `64092b2c` (строки BKB до коммита) — в exe запечён `64092b2c`, а релиз-тар `1.99.3`
  был на `8dcfd2bc` → для Remote-SSH клиент↔сервер разъедутся. Патч без пересборки REH: в
  `~/.404brain-server/bin/<commit>/product.json` и в `brain-reh-linux-x64-1.99.3.tar.gz` (WSL, ext4) строка `commit`
  заменена на `64092b2c…`; тар залит clobber в release `1.99.3`.

### сессия 2.0.0 (завершена)
Состояние: **релиз v1.7.3 выпущен** (404Brain-win32-x64-1.7.3.zip, tag v1.7.3, product 1.7.3/0052).

Сделано в этой сессии (сборка из HEAD `8dcfd2bc`, без нового REH — клиент↔сервер commit совпадают):
1. **Скорость ответов**:
   - Reasoning по умолчанию ВЫКЛ для Chat (`modelCapabilities.ts` → `defaultEnabledVal = !canTurnOffReasoning`); в UI можно включить обратно.
   - Дерево воркспейса в системном сообщении урезано: `MAX_DIRSTR_CHARS_TOTAL_BEGINNING` 20k→8k, стартовый `START_MAX_DEPTH` ∞→6 (`directoryStrService.ts`) — меньше токенов и быстрее генерация system message (важно для огромных папок типа `~`).
   - Язык ответов по Unicode-алфавиту (`detectHumanLanguage`), блок `<language_override>` в system message; `<formatting>` — без `**`/`#` в прозе, короткие ответы; запрет tool-call/XML/JSON-синтаксиса в видимом тексте.
2. **«Привет» больше НЕ запускает tools (движковый гард!)**: `_isSimpleOpenerMessage()` в `chatThreadService.ts` — если это первое сообщение треда и оно короткий одиночный привет, `_runChatAgent` вызывается с `chatModeOverride: 'normal'` (тулзов в 'normal' нет вообще → ни `pm2 list`, ни поиска). Промпт-подкрепление: HARD RULE (minimum tool use on greeting).
3. **Aide-style проактивность**: `_getActiveFileDiagnosticsStr()` в `convertToLLMMessageService.ts` — lint-ошибки активного файла (`IMarkerService.read({resource})`) подмешиваются в system message для agent/gather (`<current_lint_errors>`), меньше round-trips.
4. **Apply-фикс**: если блок хочет примениться в 'current' файл, а файла нет — открывается новый untitled-файл и Apply идёт туда (`ApplyBlockHoverButtons.tsx` + `IEditorService` в accessor map). Больше не показывает «We couldn't run Apply here».
5. **compile** ✅ (0 ошибок), **buildreact** ✅, desktop-сборка ✅ (13 мин), все фиксы проверены в бандле (`rg` по workbench.desktop.main.js).

### Постфикс сессии 2.0.0 — REH `.144` (раньше сборки): сервер/клиент version mismatch + битый rg
- `version mismatch`: клиент собран из `8dcfd2bc`, сервер был с `3efe08f1`. Фикс БЕЗ пересборки REH: в
  `~/.404brain-server/bin/<commit>/product.json` (лежит В КОРНЕ папки сервера, не `resources/app/`) строка
  `commit` заменена на `8dcfd2bc`; тар `brain-reh-linux-x64-1.99.3.tar.gz` пересобран в WSL с этим же commit
  (ext4 сохраняет exec-биты) и залит clobber в release `1.99.3` (52.5 МБ). Если клиент позже пересоберут
  с новым коммитом — повторить патч.
- `spawn .../rg ENOENT` на сервере: в `node_modules/@vscode/ripgrep/bin/` был ТОЛЬКО `rg.exe` (Windows-PE).
  Установлен Linux `rg` (ripgrep 13.0.0) из официального server 1.99.3
  (`https://update.code.visualstudio.com/commit:17baf841131aa23349f217ca7c570c76ee87b957/server-linux-x64/stable`,
  НЕ `commit/`), `chmod +x`, `rg.exe` удалён; заодно убраны Windows-аддоны (`msalruntime.dll`, `conpty*`,
  `winpty*`, `OpenConsole.exe`) — `find *.exe|*.dll` = 0. Сервер стартует («404Brain 1.99.3»).
- Кейс на будущее: системный тест терминала/поиска на новой машине удаляется со старым таром (1559 файлов,
  отсутствие `+x` на `bin/*`): пересобирать тар в WSL.

### сессия 1.9.0 (завершена)
Состояние: **релиз v1.7.2 выпущен** (404Brain-win32-x64-1.7.2.zip, tag v1.7.2; REH-сервер обновлён в release `1.99.3`).

Итоги сессии (план внизу — исполнен полностью):
- Релиз `v1.7.2` (коммит `3efe08f1`): desktop win32-x64 + REH linux-x64 собраны из ОДНОГО HEAD
  (desktop `13 мин`, REH `1.6 ч` — второй сборочный процесс мешал в старте фазы compile-src).
- REH-тар `brain-reh-linux-x64-1.99.3.tar.gz` (57.9 МБ, commit `3efe08f1`) залит clobber в release `1.99.3`.
- В релиз добавлена партнёрская реф-ссылка `https://aitunnel.ru/?r=52512` в описание.

Сделано в этой сессии:
1. **aiTunnel-каталог (~130 моделей)** в настройках провайдеров (шинный список моделей вместо жёстко зашитых).
2. **Фикс 'auto'**: вместо кашицы `[object Object]` в выпадашке моделей теперь корректный выбор; дефолтные
   дешёвые китайские модели (DeepSeek-серия) для нового юзера.
3. `brainVersion` → 1.7.2, `brainRelease` → 0051.
4. **Сборка и релиз**: desktop + REH из одного HEAD `3efe08f1`, всё проверено (commit, версии, расширения:
   beardedtheme/beardedicons/brain-uikit в desktop; в REH кита нет — ожидаемо).
5. Кейс: два параллельных gulp-сборщика (`vscode-reh-linux-x64` + случайно запущенный второй)
   конкурируют за `out-build` и растягивают compile-src с ~10 мин до 90+ мин — запускать сборки строго по одной.

### Постфикс сессии 1.9.0 — фикс REH-тара (клиент не подключался по SSH)
Симптом: после релиза 1.7.2 Remote-SSH на `.144` падал с `Couldn't install vscode server on remote server,
install script returned non-zero exit status`, в логе сервера `bin/404brain-server: Permission denied`.

Кейс (ВАЖНО): **Windows `tar -czf` НЕ сохраняет exec-биты** (всё кладёт `-rw-rw-rw-`). Первую заливку
REH-тара в release 1.99.3 сделали через системный tar → на удалённом сервере и `bin/404brain-server`,
и бинарь `node` распаковались без `+x` → сервер не запускается. В старом таре (1.7.1) биты были
(`-rwxr-xr-x`, 1559 файлов) — он собирался иначе (через WSL).
Рецепт правильного тара под Windows: `wsl -e bash -lc "cp -r <folder> ~/ && chmod +x bin/* bin/remote-cli/* bin/helpers/*.sh; tar -czf ..."` —
на ext4 биты сохраняются. Проверка: `tar -tvf | grep 404brain-server` должен показать `-rwxr-xr-x`.
Фикс уже залит clobber в release 1.99.3 (58.0 МБ, commit `3efe08f1`); на `.144` переразвернуто вручную и проверено (`--help` → «404Brain 1.99.3»).

### Постфикс сессии 1.9.0 — фикс REH-тара (нативные аддоны Windows в Linux-таре → зависал терминал)
Симптом: терминал на remote (`.144`) висел при открытии; в логе сервера:
`@parcel/watcher/build/Release/watcher.node: invalid ELF header` (это Windows PE32, а не Linux ELF).

Кейс (ВАЖНО): `npm run gulp vscode-reh-linux-x64` на **Windows** кладёт в REH `node_modules/**`
нативные `.node` аддоны, скомпилированные под Windows (PE32+): `@parcel/watcher`, `node-pty`,
`@vscode/spdlog`, `native-watchdog`, `kerberos`, `@vscode/deviceid`, `vsda` и Windows-only
(`crypt32`, `windows_process_tree`, `winregistry`, `conpty*`, `msal-node-runtime`). Для Linux-REH
они бесполезны и роняют ptyHost (терминал), файл-watcher и т.д.

Рецепт фикса (пересобрать нативный слой из официального VS Code той же версии):
1. Скачать официальный сервер той же версии (1.99.3):
   `curl "https://update.code.visualstudio.com/commit:<MS_COMMIT>/server-linux-x64/stable" -o vs-server.tar.gz`
   (commit берём из `https://api.github.com/repos/microsoft/vscode/git/refs/tags/<version>`).
2. Распаковать оба тара внутри WSL (на ext4, чтобы сохранить exec-биты):
   `tar xzf our.tar.gz` + `mkdir of && tar xzf vs-server.tar.gz -C of`.
3. Скопировать Linux ELF `.node` из официального в наш REH (пути совпадают):
   `@parcel/watcher/build/Release/watcher.node`, `node-pty/build/Release/pty.node`,
   `@vscode/spdlog/build/Release/spdlog.node`, `native-watchdog/build/Release/watchdog.node`,
   `kerberos/build/Release/kerberos.node`, `@vscode/deviceid/build/Release/windows.node`,
   `vsda/build/Release/vsda.node` (vsda может отсутствовать — создать папку и положить).
4. Удалить Windows-only аддоны (их в Linux-таре быть не должно):
   `node-pty/build/Release/{conpty,conpty_console_list}.node`,
   `@vscode/windows-ca-certs/.../crypt32.node`, `@vscode/windows-process-tree/.../windows_process_tree.node`,
   `@vscode/windows-registry/.../winregistry.node`, `extensions/microsoft-authentication/dist/msal-node-runtime.node`.
5. Проверка: `find ... -name '*.node' -exec file {} +` → все `ELF 64-bit` (7 шт. остаётся).
6. Пересобрать тар в WSL: `tar -czf brain-reh-linux-x64-1.99.3.tar.gz vscode-reh-linux-x64`.
7. `gh release upload 1.99.3 <tar> --clobber`, дальше переустановить сервер на `.144` из нового тара.
   Проверка терминала напрямую: `./node ptest.cjs` с `require('node-pty')` + `pty.spawn('bash', ...)` →
   должен вывести `TERMINAL_OK`. Примечание: при `process.exit` без закрытия подписки watcher возможен
   `free(): double free` — это артефакт теста, в проде сервер закрывает подписки корректно.

### сессия 1.8.0 (завершена)
Состояние: **релиз v1.7.1 выпущен** (404Brain-win32-x64-1.7.1.zip, tag v1.7.1; REH-сервер обновлён в release `1.99.3`).

Итоги сессии (план внизу — исполнен полностью, кроме ручной проверки `.144`):
- Релиз `v1.7.1` (коммит `5cad6560`, сборка `20515a28`): desktop win32-x64 + REH linux-x64 собраны из ОДНОГО HEAD.
- REH-тар `brain-reh-linux-x64-1.99.3.tar.gz` (57.9 МБ, commit `20515a28`) залит clobber в release `1.99.3` — SSH-клиент теперь ставит корректный сервер под свой commit.
- Умения ui_design/ux-ui-kit + ReAct-цикл в системном промпте; кит brain-uikit в desktop-билде (проверено);
  кейс: в REH кит НЕ уходит (массив extensionKind → UI; для агента чтение идёт из клиентского appRoot).

Сделано в этой сессии (планируется):
1. **Фикс boot-краша (серый экран)** после релиза v1.7.0 (коммит `238607b3`):
   - Краш 1: `TypeError: decorator is not a function` — цикл common↔browser: `common/cursorImportService.ts`
     импортировал токен `IChatThreadService` из `browser/chatThreadService.ts`; esbuild клал браузерный модуль
     ПОСЛЕ использования → токен `undefined` в `__param(3, ...)`. Фикс: токен перенесён в
     `common/chatThreadServiceTypes.ts` (`createDecorator('brainChatThreadService')`), browser ре-экспортирует.
   - Краш 2: `ReferenceError: process is not defined` — `const pathSep = process.platform === 'win32'` в том же
     файле; sandbox-рендерер без `process`. Фикс: `isWindows` из `base/common/platform.js`.
   - Проверка: токен в бандле объявлен ДО `CursorImportService = __decorate([...])`; изолированная сессия
     (`--user-data-dir=новый`) стабильна 4+ мин, лог чист.
2. **Remote-сервер (SSH/REH) — версии и автоустановка** (замена битого REH в release `1.99.3`, кейс `.144`):
   - Механизм: `extensions/open-remote-ssh/src/serverSetup.ts` — `DEFAULT_DOWNLOAD_URL_TEMPLATE`
     `releases/download/<version>/brain-reh-<os>-<arch>-<version>.tar.gz`; сервер ставится автоматически
     в `~/.404brain-server/bin/<git-commit>` при подключении.
   - `Client refused: version mismatch` — серверная проверка `remoteExtensionHostAgentServer.ts:384`:
     `rendererCommit !== myCommit`. Совпадение commit'ов клиент↔сервер ОБЯЗАТЕЛЬНО: desktop и REH собирать
     из одной ревизии (HEAD). Битый ассет был собран раньше → на `.144` после обновления tar перепроверить.
   - Кейс: mangler может упасть на `.d.ts` из node_modules (`OVERLAPPING edit`,
     `google-auth-library/.../impersonated.d.ts`) → в `build/lib/mangle/index.js` node_modules исключён из моглинга.
   - Кейс: алиас `144` в `~/.ssh/config` был битый (`Host 144<мусор>!`) — поправлен.
3. **Дефолтные умения (Agent Skills)**: блок `<default_skills>` в `prompts.ts` (code-review, debugging,
   test-writing, refactoring, git-workflow, codebase-onboarding, security-review, performance-analysis,
   api-integration, documentation-writing, ui_design, ux-ui-kit). Формат agentskills.io (name + when + how).
   В `<always_analyze>` добавлен ReAct-цикл (analyze→plan→act→observe→correct→answer) с честностью про
   непроверенные числа/факты.
4. **UI/UX-кит (plugin87/ux-ui-agent-skills, v2.8.0)**: пакуется как локальное расширение
   `extensions/brain-uikit/` (extensionKind `["workspace","ui"]`), содержимое — trimmed копия кита в `ux-ui/`
   (~2.1 МБ: `.claude/skills` 19 шт + `rules/`, `design-systems/` 138 шт, `tokens/`, `components/`,
   `accessibility/`, `workflows/`, `CLAUDE.md` и т.д.; исключены `examples/` ~3.6 МБ, `tests/`, `evals/`,
   `.github/`, `scripts/`).
   Кит попадает в desktop-продукт (проверено в билде: commit 20515a28, desktop 1.7.1).
   ⚠️ Кейс: в REH-сборку НЕ попадает — `gulpfile.reh.js` (`isUIExtension`, switch по `extensionKind`,
   массив `["workspace","ui"]` уходит в default → considered UI → отфильтрован). Для агента не критично:
   агент живёт в клиентском рендерере и читает файлы кита из локального `<appRoot>/extensions/brain-uikit/ux-ui/`
   (`read_file` ходит в `brainModelService`, работает с любым абсолютным путём вне воркспейса).
   Если когда-то понадобится кит на сервере — поставить `"extensionKind": "workspace"` (строкой).
5. `brainVersion` → 1.7.1, `brainRelease` → 0050.

### Прошлые сессии

### сессия 1.7.0 (завершена)
Состояние: **релиз v1.7.0 выпущен** (404Brain-win32-x64-1.7.0.zip, tag v1.7.0)

Сделано в этой сессии:
1. **Дефолтные тема и иконки (Bearded)**:
   - В репо добавлены локальные расширения `extensions/beardedtheme` (BeardedBear 10.1.0) и
     `extensions/beardedicons` (BeardedBear 1.22.0); package.json очищены от dev-мусора (шкрипты/deps).
     Скачаны VSIX с Marketplace, распакованы (обход: `.vsix` → копия `.zip` + `ZipFile::ExtractToDirectory`,
     PowerShell `Expand-Archive` VSIX не принимает).
   - `src/vs/workbench/services/themes/common/workbenchThemeService.ts` → `ThemeSettingDefaults`:
     `COLOR_THEME_DARK = 'Bearded Theme Coffee'`, `FILE_ICON_THEME = 'bearded-icons'`,
     `COLOR_THEME_DARK_OLD = 'Default Dark+'` (миграция). Механика: `settingsId = theme.id || label`
     (`colorThemeData.ts`), для иконок `settingsId = iconTheme.id`.
   - Extensions в продукт попадают из `extensions/*/package.json` автоматически
     (`build/lib/extensions.js` → `packageNonNativeLocalExtensionsStream`); excludedExtensions их не трогает.
   - Кейс: package.json расширений, сохранённые PowerShell с UTF-8 BOM, роняют этап
     `bundle-non-native-extensions-build` (`Error parsing 'package.json' manifest file: not a valid JSON file`)
     — сохраняем JSON без BOM.
2. **Новые builtin-тулзы (умения=тулзы)**:
   - `toolsServiceTypes.ts`: `get_selection`, `get_active_file`, `get_open_tabs`, `get_workspace_info` (read-only,
     без одобрения) и `get_git_status` (с `approvalTypeOfBuiltinToolName: 'terminal'`).
   - `toolsService.ts`: реализация через `ICodeEditorService` (getActiveCodeEditor) и `IEditorService` (editors),
     `get_git_status` → `terminalToolService.runCommand('git status --short --branch')`.
   - `prompts.ts` → `builtinTools`: описания всех новых тулзов (иначе `satisfies` не соберётся).
3. **Промпты**: блок `<always_analyze>` для всех режимов (всегда думать→проверять→валидировать, не предполагать
   содержимое файлов) + блок `<skills>` в agentSpecs (каталог умений/комбо-паттернов).
   Reasoning для Chat включён по умолчанию и раньше (агент работает через `'Chat'`).
4. **docs/**: `docs/readme.md`, `docs/architecture.md`, `docs/tools-and-skills.md`, `docs/build-and-run.md`.
5. **product.json**: `brainVersion` → 1.7.0, `brainRelease` → 0049.
6. **compile** ✅ (0 ошибок).
7. **Сборка и релиз**: полная сборка `vscode-win32-x64` успешна (~25 мин), продукт проверен
   (extensions beardedtheme/beardedicons в билде, product.json 1.7.0/0049); выпущен
   `404Brain-win32-x64-1.7.0.zip`. Кейс: package.json расширений с UTF-8 BOM роняет этап
   `bundle-non-native-extensions-build` — сохранённые PowerShell JSON пишем без BOM (см. docs/build-and-run.md).
8. Релиз `v1.7.0` (коммит `cac33bf1`).
9. **Фикс boot-краша (серый экран)** после релиза (коммит `238607b3`):
   - Краш 1: `TypeError: decorator is not a function` — цикл common↔browser: `common/cursorImportService.ts`
     импортировал токен `IChatThreadService` из `browser/chatThreadService.ts`; esbuild клал браузерный модуль
     ПОСЛЕ использования → токен `undefined` в `__param(3, ...)`. Фикс: токен перенесён в
     `common/chatThreadServiceTypes.ts` (`createDecorator('brainChatThreadService')`), browser ре-экспортирует.
   - Краш 2: `ReferenceError: process is not defined` — `const pathSep = process.platform === 'win32'` в том же
     файле; sandbox-рендерер без `process`. Фикс: `isWindows` из `base/common/platform.js`.
   - Проверка: `decode`: токен в бандле объявлен ДО `CursorImportService = __decorate([...])`; изолированная
     сессия (`--user-data-dir=новый`) стабильна 4+ мин, лог чист.
   - Кейс remote: если последняя сессия была ssh-remote, при старте клиент 404Brain восстанавливает remote-окно и
     получает `version mismatch` (сервер на удалённой машине должен быть такой же сборки/commit). Это НЕ баг
     клиента — отрендерить remote нельзя, пока сервер не обновлён. Урок: локальный клиент и удалённый сервер
     (REH) должны собираться из одного коммита.

### сессия 1.6.2 (завершена)
Состояние: **релиз v1.6.2 выпущен** (404Brain-win32-x64-1.6.2.zip, tag v1.6.2)

Сделано в этой сессии:
1. **Регламент Cursor в системный промпт агента** (`common/prompt/prompts.ts`): добавлен блок `agentSpecs` для `mode === 'agent'` —
   `<communication>`, `<status_update>`, `<summary>`, `<tool_calling>` (ONE tool call at a time — сохранено), `<flow>`,
   `<looking_before_leaping>`, `<code_style>`, `<citing_code>` (формат `startLine:endLine:/full/absolute/path`).
2. **Язык ответов** (`common/prompt/prompts.ts`): новый блок `<language>` во всех режимах чата —
   отвечать на языке пользователя (Привет → по-русски), код/термины остаются на английском, запрет самовольно переключаться на другой язык.
3. **Reasoning «как у Cursor» — извлечение думалки у провайдеров**:
   - `electron-main/llmMessage/sendLLMMessage.impl.ts`: OpenAI-совместимый парсер толерантен — конфигурируемое поле,
     а если пусто: `reasoning_content` → `reasoning` → `reasoning_summary` → `thinking` (раньше openAI/xAI вообще не отдавали думалку,
     aiTunnel/OpenRouter ловили только `reasoning`, а pass-through апстримы шлют `reasoning_content`).
   - Gemini: извлекаются thought-парты (`part.thought === true`) в `fullReasoning` (было «do not handle reasoning yet», думалка текла в displayContent).
   - `common/modelCapabilities.ts`: добавлен `output` для openAI (`reasoning_content`) и xAI (`reasoning`).
   - Рендер блока рассуждений (`ReasoningWrapper` в `SidebarChat.tsx`) уже существовал — теперь данные доходят до него у всех провайдеров.
4. **compile** ✅ (0 ошибок).
5. **Импорт из Cursor (автомат)** — фича сессии 1.6.2:
   - Формат Cursor (что где лежит): `%APPDATA%\Cursor\User\workspaceStorage\<hash>\state.vscdb` (SQLite).
     Чаты — ключ `workbench.panel.aichat.view.aichat.chatdata` (JSON, `tabs[]` → `bubbles[]` user/ai c `text`),
     композеры — `composer.composerData` (в основном служебные/короткие). Папка воркспейса — `workspace.json` → `folder` (`file:///h%3A/...`).
     `conversation-search.db` (FTS) НЕ используем; таблицы `composerHeaders/cursorDiskKV` пусты. 218 воркспейсов с чатами.
   - Выбор чтения: `@vscode/sqlite3` (уже в проекте, `import('@vscode/sqlite3')`), БД открываем ТОЛЬКО с `PRAGMA query_only=ON` (Cursor не трогаем).
   - Архитектура: main-процесс `electron-main/cursorImportChannel.ts` (IServerChannel, команды scan/read/importRules) +
     renderer-сервис `common/cursorImportService.ts` (канал `brain-channel-cursorImport`, dedupe по `brain.cursorImport.seenIds`,
     конвертация chatdata → треды 404Brain, `currentWorkspaceConversations` считается на клиенте).
   - Rules: `.cursorrules` + `.cursor/rules/*.mdc` + глобальные `~/.cursor/rules` → `.brainrules` (только если файла ещё нет).
   - UI: авто-баннер `sidebar-tsx/CursorImportBanner.tsx` на лендинге чата (сам находит чаты, кнопка «Import all»),
     в Settings.tsx секция «Import from Cursor» (Import All Chats / Import Rules).
   - `chatThreadService.ts`: `ThreadType` получил `title?: string`, добавлен `importThreads(threads)`.
6. Релиз `v1.6.2`.

### Прошлые сессии (кратко)
- **v1.6.1**: markdown-фикс (InlineTokens), картинки в чат (vision OpenAI/Anthropic/Gemini), фикс очередности сообщений,
  меню «+» в чате (Attach image / MCP / .brainrules / skill), скилы `.brainskills/*.md`, AGENTS.md-документация. Релиз `v1.6.1`.
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