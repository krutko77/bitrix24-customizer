# Журнал изменений

Новые записи — сверху.

## 2026-11-06 — подключён GitHub-репозиторий

- `git init -b main`, `origin` → https://github.com/krutko77/bitrix24-customizer.git (публичный, пустой; доступность проверена `git ls-remote`).
- Коммиты и push не выполнялись.
- Перед первым снимком: из `docs/gaps.md` убран IP сервера, `.claude/settings.local.json` добавлен в `.gitignore`.

## 2026-11-06 — удалены остатки FZ-87

- По просьбе сотрудника удалены: `src/` (дашборд Node/Express), `package.json`, `deploy-vps.sh`, `.env.example`, `.portal-meta.json`.
- Оставлены `CLAUDE.md`, `.claude/`, `scripts/snapshot.sh`, `README.md` (рабочая инфраструктура, упоминаний FZ-87 нет).
- Исправлены ссылки на удалённое в `state.md`, `gaps.md`, `knowledge/01`, `07`, `09`. Данные VPS из удалённого шаблона деплоя сохранены как вопрос в `gaps.md` (п. 10).

## 2026-11-06 — база знаний по Битрикс24

- Создана база знаний `docs/knowledge/`: `README.md`, справочники `00`–`10` (обзор облачной кастомизации, доступ и вебхуки, запросы, лимиты и ошибки, CRM, пользовательские поля, автоматизация и события, приложения и placement, карта остальных модулей, SDK и инструменты, D7/Bitrix Framework), `sources.md`.
- Загружено локальное зеркало официальной REST-документации (репозиторий `bitrix-tools/b24-rest-docs`, MIT, коммит `806cf55`) в `docs/knowledge/rest-docs/`; сгенерирован индекс `docs/knowledge/reference/methods-index.md` (2819 страниц).
- Добавлены скрипты `scripts/sync-rest-docs.sh` и `scripts/build-methods-index.py`; в `.gitignore` добавлено `docs/knowledge/rest-docs/`.
- Проверено: имена методов сверены с индексом, все относительные ссылки в `docs/knowledge/*.md` существуют (0 битых), спорные утверждения про UF исправлены по документации (`05`).
- Удалён временный клон репозитория документации `/home/my_workspace/_untrusted/b24-rest-docs`.
- Заполнены `docs/state.md`, `docs/gaps.md`.
- Не делалось: проверка на портале ЕС Транс, чтение содержимого D7/Framework, подключение MCP-сервера и Вайбкода, снимок в git.
