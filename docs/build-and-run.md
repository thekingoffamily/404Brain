# Сборка и запуск 404Brain

## Быстрая проверка типов
```powershell
npm run compile   # gulp, проверяет весь проект (~5-8 мин). Ошибки tsc в логе.
```

## Правки React (UI сайдбар/настройки)
Источник ТОЛЬКО в `src/vs/workbench/contrib/brain/browser/react/src/**`.
Схема:
```powershell
# правим react/src/** (НЕ src2/, НЕ out/)
npm run buildreact   # префиксует classNames + собирает бандлы out/**
```
`src2/` и `out/` — генерируемые (в .gitignore), править напрямую нельзя.

## Полная сборка Windows (долгая)
```powershell
$env:NODE_OPTIONS='--max-old-space-size=8192'
npm run gulp vscode-win32-x64
```
~25-40 минут. Выход: `C:\Users\palapalaru\Desktop\VSCode-win32-x64`.

## Релиз-процедура
1. Убедиться: `buildreact` (если правился react) + `compile` прошли с 0 ошибок.
2. Обновить версии в `product.json` (`brainVersion`, `brainRelease`).
3. Полная сборка → `C:\Users\palapalaru\Desktop\VSCode-win32-x64`.
4. Упаковать zip: `404Brain-win32-x64-<v>.zip` (из папки сборки), положить на рабочий стол.
5. Коммит + `git push` (ветка `main`).
6. `gh release create v<v> <zip>` + описание.
7. **Реф-ссылка партнёрская (обязательно): `https://aitunnel.ru/?r=52512`**.
8. Статьи: черновики в `articles/vc.ru/`, шаблон `articles/_template.md`.

## Remote-сервер (SSH/REH) — сборка и «релиз»
Remote-SSH ставит сервер на удалённую машину АВТОМАТИЧЕСКИ: клиент скачивает из GitHub releases
(`DEFAULT_DOWNLOAD_URL_TEMPLATE` в `extensions/open-remote-ssh/src/serverSetup.ts`):
`https://github.com/thekingoffamily/404Brain/releases/download/<tag>/brain-reh-<os>-<arch>-<version>.tar.gz`,
где `<version>` = версия app package.json (сейчас `1.99.3`), `<tag>` = та же версия, os/arch = linux/x64|arm64|...
→ распаковка `--strip-components 1` в `~/.404brain-server/bin/<git-commit>` → запуск `bin/404brain-server`.

Чтобы remote вообще работал, **commit клиента и сервера должны совпадать** (обоих обязан быть текущий git HEAD):
на сервере при хендшейке `remoteExtensionHostAgentServer.ts` проверяет `rendererCommit !== myCommit` →
`Client refused: version mismatch`. Поэтому:
1. Собери REH из ТОЙ ЖЕ ревизии, что и desktop: `$env:NODE_OPTIONS='--max-old-space-size=8192'`; `npm run gulp vscode-reh-linux-x64` → `C:\Users\palapalaru\Desktop\vscode-reh-linux-x64` (~1.5 ч, тянет node.js для linux).
2. Упакуй содержимое папки в `brain-reh-linux-x64-<version>.tar.gz` (`tar -a -c -f ... -C <папка> .`), обнови ассет:
   `gh release upload <версия-тег> brain-reh-linux-x64-<version>.tar.gz --clobber` (сегодня тег `1.99.3`).
3. На уже подключавшихся серверах лишние старые папки `~/.404brain-server/bin/<старый-commit>` можно удалить;
   при следующем подключении клиент сам поставит свежий сервер под свой commit (свежих серверов это касается автоматически).

Кейс: mangler (minify классов) может упасть на `.d.ts` из node_modules (`OVERLAPPING edit`,
например `google-auth-library/.../impersonated.d.ts`) — node_modules исключён из переименований
(см. `build/lib/mangle/index.js`, guard `/node_modules/`). Если менять до-коммитную ревизию —
сначала закоммить, иначе `product.json.commit` останется от старого HEAD и remote не совпадёт.

## Разворот на новом ПК
1. `git clone` репозитория 404Brain.
2. `npm install` (окружение VS Code 1.99.3).
3. Собрать как выше. (см. также статью `articles/` про быстрый разворот).

## Замечания по теме/иконкам
- Чтобы сборка не пыталась ставить зависимости для тематических расширений
  (`extensions/beardedtheme`, `extensions/beardedicons`), в их `package.json` удалены
  scripts/dependencies/devDependencies/sponsor-ключи.
- Скачанные с Marketplace `.vsix` распаковываются копированием файла в `.zip` + `ZipFile::ExtractToDirectory`
  (PowerShell `Expand-Archive` не принимает расширение `.vsix`).
- НЕ сохранять package.json расширений из PowerShell в UTF-8 с BOM: этап `bundle-non-native-extensions-build`
  падает с `Error parsing 'package.json' manifest file: not a valid JSON file` (vsce не понимает BOM).
  Поведение `-Encoding UTF8` в Windows PowerShell 5.1 пишет BOM; править JSON лучше так, чтобы оставался UTF-8 без BOM.

## Диагностика запуска (серый экран / краш при старте)
- Разбор приложения: `<сборка>\\resources\\app\\out\\vs\\workbench\\workbench.desktop.main.js`.
- Логи сессии: `%APPDATA%\\404Brain\\logs\\<session>\\window1\\renderer.log` и `...\\main.log`.
  Краши/дампы: `%APPDATA%\\404Brain\\Crashpad\\`.
- **`TypeError: decorator is not a function`** = цикл common↔browser (см. правило в AGENTS.md):
  DI-токен `createDecorator(...)` оказался в бандле ПОСЛЕ `X = __decorate([__param(N, токен)])` → токен `undefined`.
  Грепни `workbench.desktop.main.js` по имени токена: номер строки `var X = createDecorator(...)` ДОЛЖЕН быть
  меньше номера строки `X = __decorate`. Класть токены в common, browser ре-экспортирует. Устранить цикл — пересобрать.
- **`ReferenceError: process is not defined`** — `process.*` на уровне модуля common/browser: sandbox-рендерер
  не имеет глобального `process`. Заменять на платформенные хелперы (`isWindows` из `base/common/platform.js` и т.п.).
- **`Connection error: ... version mismatch`** при старте = восстанавливается ssh-remote окно, а сервер на
  удалённой машине собран из другого коммита/версии. Локальный клиент и удалённый REH-сервер
  должны собираться из одного коммита — иначе remote окно не отрисуется (НЕ баг клиента, лог чистый).
- Изолированная проверка сборки без профиля: `404Brain.exe --user-data-dir=<новая пустая папка>` — если стартует
  стабильно, проблема в старых данных/remote-восстановлении, а не в билде.