# 09. SDK и инструменты разработчика

Источники: [sdk/index.md](rest-docs/sdk/index.md), [ai-tools/](rest-docs/ai-tools/mcp.md), [simulator/](rest-docs/simulator/README.md), [first-steps/](rest-docs/first-steps/index.md), [local-integrations/](rest-docs/local-integrations/index.md). Статус: *по документации*.

## 1. SDK

| SDK | Язык / среда | Авторизация | Когда выбирать (по документации) |
|---|---|---|---|
| [B24JsSDK](rest-docs/sdk/b24jssdk/index.md) | JS, браузер и Node.js | вебхук, OAuth | Внешнее веб-приложение или Node.js-сервис; `batch`, типовые объекты, логирование |
| [BX24.js](rest-docs/sdk/bx24-js-sdk/index.md) | JS, **только** фрейм приложения | OAuth (от Битрикс24) | Приложение внутри интерфейса, без своего сервера |
| [B24PhpSDK](rest-docs/sdk/b24phpsdk/index.md) | PHP | вебхук, OAuth | Сложное тиражное приложение |
| [CRest PHP SDK](rest-docs/sdk/crest-php-sdk/index.md) | PHP | вебхук, OAuth | Быстрая проверка или простая локальная интеграция |
| [B24PySDK](rest-docs/sdk/b24pysdk/index.md) | Python | вебхук, OAuth | Интеграции на Python (Django, FastAPI, Flask) |
| [B24GoSDK](rest-docs/sdk/b24gosdk/index.md) | Go | вебхук, OAuth | Фоновые сервисы с большими выгрузками |

Общее: SDK не меняют состав методов и **не отменяют лимиты** ([03-limits-and-errors.md](03-limits-and-errors.md)). Ключ вебхука и токены нельзя класть в клиентский код и репозиторий.

Язык и SDK для проекта не выбраны: решение зависит от первой практической задачи (см. `docs/state.md`). Без SDK возможны прямые HTTP-вызовы ([02-rest-requests.md](02-rest-requests.md)).

## 2. Первые шаги и практика

- [first-steps/](rest-docs/first-steps/index.md): доступ к REST, первый вызов, как пользоваться примерами.
- Генератор запросов: *Разработчикам → Другое → Генератор запросов*.
- [tutorials/](rest-docs/tutorials/index.md) — сценарии по CRM, БП, типам полей и другому.
- Что нового в API: [whats-new.md](rest-docs/whats-new.md).

## 3. Инструменты для ИИ-агентов

| Инструмент | Что делает | Страница |
|---|---|---|
| **MCP-сервер документации** (`b24-dev-mcp`) | Отдаёт ИИ-инструменту актуальную документацию REST (методы, параметры, ошибки, примеры). Данных портала не видит и методы не вызывает | [mcp.md](rest-docs/ai-tools/mcp.md) |
| **Симулятор REST API** | Проверяет вызов по схеме метода и выполняет списочные методы на тестовом датасете, без портала; секреты (вебхуки, токены) в него передавать нельзя | [simulator.md](rest-docs/ai-tools/simulator.md), [simulator/](rest-docs/simulator/README.md) |
| **Вайбкод** | Платформа создания приложений Битрикс24 с помощью ИИ-агента (ключ, описание задачи, хостинг серверной части) | [vibecode.md](rest-docs/ai-tools/vibecode.md), [vibecode-create-app.md](rest-docs/ai-tools/vibecode-create-app.md) |

Для этого проекта основной источник — **локальное зеркало документации** (`docs/knowledge/rest-docs/`): оно не требует подключения внешних сервисов. MCP-сервер и Вайбкод — внешние сервисы, подключение к ним не выполнялось и требует решения сотрудника.

## 4. Зеркало документации: как пользоваться и обновлять

- Поиск метода: `grep -i 'crm.deal' docs/knowledge/reference/methods-index.md` → путь страницы → читать `rest-docs/api-reference/<путь>`.
- Полнотекстовый поиск: `grep -ril 'application_token' docs/knowledge/rest-docs/`.
- Обновить зеркало: `bash scripts/sync-rest-docs.sh` (клонирует репозиторий, пересобирает индекс, пишет `_SOURCE.txt` с коммитом).
- Зеркало не хранится в git (`.gitignore`), воспроизводится скриптом. Подробности — [sources.md](sources.md).
