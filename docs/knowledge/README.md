# База знаний по Битрикс24 (облако, тариф «Профессиональный»)

Для кого: проект настройки корпоративного портала компании **ЕС Транс**.
Собрано 2026-11-06 из официальных источников (список — в [sources.md](sources.md)).

## С чего начать

| Задача | Читать |
|---|---|
| Понять, что вообще можно кастомизировать в облаке и чем | [00-cloud-customization-overview.md](00-cloud-customization-overview.md) |
| Получить доступ к API, создать вебхук/приложение, выбрать скоупы | [01-access-auth-webhooks.md](01-access-auth-webhooks.md) |
| Собрать запрос, batch, пагинация, REST 3.0 | [02-rest-requests.md](02-rest-requests.md) |
| Лимиты и коды ошибок | [03-limits-and-errors.md](03-limits-and-errors.md) |
| CRM: сделки, лиды, смарт-процессы, воронки, товары | [04-crm.md](04-crm.md) |
| Пользовательские поля | [05-user-fields.md](05-user-fields.md) |
| Роботы, бизнес-процессы, события, исходящие вебхуки | [06-automation-events.md](06-automation-events.md) |
| Приложения, встройка в интерфейс (placement), Push&Pull | [07-apps-and-placements.md](07-apps-and-placements.md) |
| Задачи, пользователи, структура, диск, чаты, телефония и др. | [08-other-modules.md](08-other-modules.md) |
| SDK, MCP-сервер документации, инструменты | [09-sdk-and-tools.md](09-sdk-and-tools.md) |
| D7 и Bitrix Framework — что это и применимо ли в облаке | [10-d7-and-bitrix-framework.md](10-d7-and-bitrix-framework.md) |
| Найти конкретный метод REST | [reference/methods-index.md](reference/methods-index.md) + grep по зеркалу |

## Как устроена папка

```
docs/knowledge/
├── README.md                     ← этот файл
├── 00…10-*.md                    ← тематические справочники (написаны вручную, на русском)
├── sources.md                    ← источники, даты, лицензии, ограничения
├── reference/methods-index.md    ← индекс всех 2819 страниц справочника REST (генерируется)
└── rest-docs/                    ← локальное зеркало официальной REST-документации (в git НЕ входит)
```

## Как искать по зеркалу

```bash
# где описан метод
grep -i 'crm.deal.add' docs/knowledge/reference/methods-index.md
# полнотекстовый поиск по всей документации
grep -rIl 'OPERATION_TIME_LIMIT' docs/knowledge/rest-docs/
```

Страница метода содержит параметры, пример ответа, коды ошибок и примеры на curl/PHP/JS/Python.

## Зеркало отсутствует или устарело

Зеркало ~50 МБ и не коммитится (см. `.gitignore`). Восстановить/обновить:

```bash
bash scripts/sync-rest-docs.sh
```

Скрипт также пересобирает `reference/methods-index.md`. Актуальность зеркала — в `rest-docs/_SOURCE.txt`.

## Правила пользования базой

1. **Метод не выдумывать.** Перед использованием метода убедиться, что он есть в `methods-index.md` или в зеркале.
2. **Версия API.** Часть методов есть в двух версиях (классической `/rest/` и REST 3.0 `/rest/api/`) с разными параметрами — см. [02-rest-requests.md](02-rest-requests.md).
3. **Пометки достоверности** в справочниках: *«по документации»* — прочитано в официальном источнике; *«не проверено на портале»* — реальное поведение на портале ЕС Транс не сверялось.
4. Вопросы, на которые база не отвечает (специфика портала ЕС Транс), — в [../gaps.md](../gaps.md).
