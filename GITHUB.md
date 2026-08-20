# GitHub: что есть и что берём

## Подключение

- MCP GitHub в Cursor: **нет**
- CLI `gh`: **не установлен, не залогинен**
- Репозитории смотрел через поиск, не через API GitHub

Подключить GitHub имеет смысл только если клонируем конкретный инструмент. Для откликов сейчас не обязательно.

## Готовые репозитории (проверка)

Не ставим (ломают ToS LinkedIn / массовый Apply без вас):

- https://github.com/akbardevop/ai-job-agent — Easy Apply автоматом
- https://github.com/AbhishekMandapmalvi/AutoApply
- https://github.com/liruihan000/claude-job-auto-apply
- https://github.com/billmal071/job-agent

Имеет смысл **позже** только как поиск объявлений (вы всё равно жмёте 1 да / 1 нет):

- https://github.com/speedyapply/JobSpy — Indeed / LinkedIn listings в таблицу, без аккаунта
- https://github.com/Jmx097/Job-Scout-public — обёртка над JobSpy, локально

Наш контур уже закрывает то же без чужого бота: пачка → Telegram → `1 да` / `2 нет` → письмо или Apply.

## Чёткий порядок работы

1. Вы смотрите резюме: открыть `resume-preview.html` в браузере (печать → PDF).
2. LinkedIn: вставить блоки из `pages-linkedin.md` (пароль мне не нужен).
3. Пишете `почта в env` — проверяю Gmail.
4. Пачка: `1 да` `2 нет` `3 да` — не коды E01.
5. JobSpy — отдельным решением, если пачек мало; не в первый день.
