# Каталог тулзов и умений (Brain, v1.7.0)

Каждое «умение» агента — это один или несколько вызовов builtin-тулзов. Способность агента решать задачи
определяется комбинацией тулзов. Полный машинный список — `builtinTools` в `common/prompt/prompts.ts`.

## Builtin-тулзы

### Контекст и чтение
| Тулз | Что делает | Параметры |
|---|---|---|
| `read_file` | Полное содержимое файла (с пагинацией) | uri, start_line?, end_line?, page_number? |
| `ls_dir` | Список файлов/папок в каталоге | uri?, page_number? |
| `get_dir_tree` | Дерево каталога (эффективно для ориентации) | uri |
| `search_pathnames_only` | Поиск по именам файлов | query, include_pattern?, page_number? |
| `search_for_files` | Поиск по содержимому (подстрока/regex) | query, search_in_folder?, is_regex?, page_number? |
| `search_in_file` | Номера строк, где встречается pattern в файле | uri, query, is_regex? |
| `read_lint_errors` | Lint-ошибки/предупреждения файла | uri |

### Контекст редактора (read-only, v1.7.0)
| Тулз | Что делает | Параметры |
|---|---|---|
| `get_selection` | Выделенный текст + файл + диапазон строк | — |
| `get_active_file` | Полный путь активного (фокусируемого) файла | — |
| `get_open_tabs` | Список всех открытых вкладок | — |
| `get_workspace_info` | Список корневых папок воркспейса | — |
| `get_git_status` | `git status --short --branch` (требует одобрения «terminal») | cwd? |

### Редактирование
| Тулз | Что делает | Параметры |
|---|---|---|
| `create_file_or_folder` | Создание файла/папки (папка — с `uri` на `/`) | uri |
| `delete_file_or_folder` | Удаление | uri, is_recursive? |
| `rewrite_file` | Перезапись файла целиком | uri, new_content |
| `edit_file` | Точечная правка search/replace блоками | uri, search_replace_blocks |

### Терминал
| Тулз | Что делает | Параметры |
|---|---|---|
| `run_command` | Разовый запуск с таймаутом `MAX_TERMINAL_INACTIVE_TIME`s | command, cwd?, terminal_id? |
| `open_persistent_terminal` | Открыть фоновый терминал (dev-сервер и т.п.) | cwd? |
| `run_persistent_command` | Команда в постоянном терминале | command, persistent_terminal_id |
| `kill_persistent_terminal` | Закрыть постоянный терминал | persistent_terminal_id |

Дополнительно в agent-режиме доступны MCP-тулзы (из `mcpService`).

## Умения (комбо-паттерны)

Промпт агента содержит блок `<skills>` с рекомендациями по комбинациям:

1. **Ориентация в коде**: `get_workspace_info` → `get_dir_tree`/`ls_dir` → `read_file` ключевых файлов.
2. **Точная правка**: `read_file` (или `get_selection`, если юзер выделил) → `edit_file` → `read_lint_errors` для проверки.
3. **Полная перезапись**: `read_file` для стиля/контекста → `rewrite_file`.
4. **Поиск**: `search_pathnames_only` (по именам) или `search_for_files` (по содержимому) → `read_file` результатов.
5. **Проверка состояния**: `get_selection` (что выделил юзер), `get_git_status` до/после изменений,
   `read_lint_errors` после каждой правки.
6. **Терминальная работа**: `open_persistent_terminal` для долгих процессов, `run_command` для разовых,
   `run_persistent_command` в уже открытом терминале.
7. **Ошибки тулзов**: не сдаваться — диагностировать вывод и повторить с исправленными параметрами.

## Правила работы агента (в системном промпте)

- **Всегда анализировать** (`<always_analyze>`): думать до ответа/действия, проверять факты тулзами,
  перечитывать изменённый код, валидировать результат (lint), не предполагать содержимое файлов.
- **Агент-регламенты** (`agentSpecs`): статус-апдейты до батчей тулзов, резюме в конце,
  один тулз за раз, чтение файлов целиком перед большими правками, верификация после правок,
  цитирование кода в формате `startLine:endLine:/full/absolute/path`.
- **Язык** (`<language>`): отвечать на языке пользователя; код/термины — английский.
- **Рассуждения (reasoning)**: для Chat (и агента через Chat) reasoning включён по умолчанию;
  у провайдеров извлекается из `reasoning_content` → `reasoning` → `reasoning_summary` → `thinking`
  (OpenAI-совместимые) и thought-партов Gemini.