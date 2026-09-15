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