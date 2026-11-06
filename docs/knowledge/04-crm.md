# 04. CRM через REST

Источники: [api-reference/crm/index.md](rest-docs/api-reference/crm/index.md), [previous-api.md](rest-docs/api-reference/crm/previous-api.md), [migration.md](rest-docs/api-reference/crm/migration.md), [universal/index.md](rest-docs/api-reference/crm/universal/index.md), [universal/crm-item-list.md](rest-docs/api-reference/crm/universal/crm-item-list.md), [universal/category/index.md](rest-docs/api-reference/crm/universal/category/index.md). Статус: *по документации*.

## 1. Три «поколения» методов CRM — не путать

| Набор | Адрес | Имена полей | Статус |
|---|---|---|---|
| **REST 3.0** `crm.<тип>.<действие>` | `/rest/api/…` | camelCase: `title`, `stageId`, `assignedById` | Рекомендован для новой разработки |
| **Универсальные `crm.item.*`** (`entityTypeId`) | `/rest/…` | camelCase | Работают; в справочнике помечены *DEPRECATED* («развитие остановлено») |
| **Методы объектов `crm.deal.*`, `crm.lead.*`, `crm.contact.*`, `crm.company.*`, `crm.quote.*`** | `/rest/…` | ВЕРХНИЙ_РЕГИСТР: `TITLE`, `STAGE_ID` | Работают; «развитие остановлено», для поддержки существующих интеграций |

- Имя метода у сделок/лидов/контактов/компаний/предложений **одинаково** в старой и новой версиях (`crm.deal.add`), различаются адрес вызова и формат параметров/ответа. Одинаковые имена = источник путаницы: всегда смотреть, какую страницу справочника открыли.
- Методы обеих версий работают с **одними и теми же данными**; переводить интеграцию можно по частям.
- Сопоставление «старый → новый»: [migration.md](rest-docs/api-reference/crm/migration.md).
- **Нет в REST 3.0** (используются классические): создание и настройка типов смарт-процессов `crm.type.*`, таймлайн, документы, автоматизация (роботы/триггеры CRM), и др. — раздел «Разделы только в предыдущей версии» в [crm/index.md](rest-docs/api-reference/crm/index.md).
- Старые счета (`entityTypeId = 5`) не поддерживаются `crm.item.*` (`ENTITY_TYPE_NOT_SUPPORTED`); новые счета — `31` (`smartinvoice`).

### Пример: создание сделки в двух версиях

```jsonc
// классическая: POST /rest/<id>/<код>/crm.deal.add
{ "FIELDS": { "TITLE": "Заявка на закупку", "ASSIGNED_BY_ID": 1, "OPPORTUNITY": 150000, "CURRENCY_ID": "RUB" } }
// → {"result": 9021}

// REST 3.0: POST /rest/api/<id>/<код>/crm.deal.add
{ "fields": { "title": "Заявка на закупку", "assignedById": 1, "opportunity": 150000, "currencyId": "RUB" } }
// → {"result": {"id": 9023}}
```

## 2. Типы объектов и `entityTypeId`

| Объект | `entityTypeId` | Сегмент в REST 3.0 | UF `entityId` (для userfieldconfig) |
|---|---|---|---|
| Лид | 1 | `lead` | `CRM_LEAD` |
| Сделка | 2 | `deal` | `CRM_DEAL` |
| Контакт | 3 | `contact` | `CRM_CONTACT` |
| Компания | 4 | `company` | `CRM_COMPANY` |
| Предложение | 7 | `quote` | `CRM_QUOTE` |
| Реквизит | 8 | — | `CRM_REQUISITE` |
| Счёт (новый) | 31 | `smartinvoice` | `CRM_SMART_INVOICE` |
| Моя компания | — | `mycompany` | — |
| Смарт-процесс | от 128 | `smartprocess<entityTypeId>` | `CRM_{id}` (⚠ `id` из `crm.type.list`, **не** `entityTypeId`) |

Имена методов REST 3.0 — только в нижнем регистре: `crm.smartinvoice.add`, а не `crm.smartInvoice.add`.
Идентификатор типа смарт-процесса: [crm.type.list](rest-docs/api-reference/crm/universal/user-defined-object-types/crm-type-list.md) (аналога в REST 3.0 нет — вызывать по `/rest/`).

## 3. Базовый цикл работы с элементом

1. Определить тип (`entityTypeId`) → 2. узнать поля → 3. создать/получить → 4. изменить/удалить.

| Шаг | Универсальные (`/rest/`) | REST 3.0 (`/rest/api/`) |
|---|---|---|
| Поля | [crm.item.fields](rest-docs/api-reference/crm/universal/crm-item-fields.md) | `crm.<тип>.field.list` / `field.get` |
| Создать | [crm.item.add](rest-docs/api-reference/crm/universal/crm-item-add.md) | `crm.<тип>.add` ([описание](rest-docs/api-reference/crm/rest-v3/items/crm-entity-add-rest-v3.md)) |
| Список | [crm.item.list](rest-docs/api-reference/crm/universal/crm-item-list.md) | `crm.<тип>.list` ([описание](rest-docs/api-reference/crm/rest-v3/items/crm-entity-list-rest-v3.md)) |
| Получить | crm.item.get | `crm.<тип>.get` |
| Изменить / удалить | crm.item.update / delete | `crm.<тип>.update` / `delete` |

Формы ответа:
- `crm.item.add/get/update` → объект в `result.item`; `crm.item.list` → `result.items` + `total`.
- **REST 3.0:** `get` и `list` **без `select` возвращают только `id`** — всегда перечислять нужные поля.
- В `crm.item.list` поле `fm` (телефоны, e-mail, мессенджеры) нельзя запросить через `select` явно — см. описание метода.

### Фильтр (`filter`) в `crm.item.list`
По умолчанию условия соединяются через AND; OR — ключ `logic`. Префиксы ключа: `>=`, `>`, `<=`, `<`, `=` (по умолчанию), `!=`/`!`, `@` (IN, массив), `!@` (NOT IN), `%` (LIKE, подстрока), `=%`/`%=` (LIKE, `%` указывать в значении), `!%`, `!=%`/`!%=` (NOT LIKE).
Для пользовательских полей типа `boolean` в фильтре передавать `1`/`0`. Прав «чтения» нет → элемент в выборку не попадает.

```json
{ "entityTypeId": 2, "select": ["id","title","stageId","opportunity"],
  "filter": {">=opportunity": 100000, "@stageId": ["NEW","PREPARATION"]},
  "order": {"id": "DESC"}, "start": 0 }
```

## 4. Воронки и стадии

- **Воронка** (`crm.category.*`) — отдельная ветка со своими стадиями и настройками карточки. Поддерживают: сделка (2), контакт (3), компания (4), счёт (31), смарт-процесс (≥128). У лидов воронок нет.
- **Стадии** хранятся в справочнике `crm.status.*` — у каждой воронки свой набор. В REST 3.0 стадии есть только у сделок и смарт-процессов (`crm.<тип>.category.*`, см. [rest-v3/categories](rest-docs/api-reference/crm/rest-v3/categories/index.md)).
- Привязка элемента к воронке: `categoryId` в `crm.item.add/update`.
- Порядок создания воронки: `crm.category.add` → стадии `crm.status.*` → привязка элементов → (опц.) вид карточки `crm.item.details.configuration.*`. Пошагово: [tutorials/crm/how-to-add-crm-objects/how-to-add-category-to-spa.md](rest-docs/tutorials/crm/how-to-add-crm-objects/how-to-add-category-to-spa.md).
- История смены стадий: [crm-stage-history-list.md](rest-docs/api-reference/crm/crm-stage-history-list.md).
- Особенности смарт-процессов: набор методов зависит от настроек типа (`isCategoriesEnabled` — воронки, `isStagesEnabled` — стадии, `isLinkWithProductsEnabled` — товары, `isClientEnabled` — клиент/основной контакт).

## 5. Связанные сущности

| Что | Где |
|---|---|
| Товарные позиции | `crm.item.productrow.*` ([set](rest-docs/api-reference/crm/universal/product-rows/crm-item-productrow-set.md)), REST 3.0 — `crm.<тип>.productrow.list / replace` |
| Контакты ↔ сделки/компании | REST 3.0: поля `contactsId`, `contactId` (основной), `companiesId`, `companyId` + `addfieldvalue` / `deletefieldvalue` / `setprimarycontact`; классика: `crm.deal.contact.*` и т.п. |
| Реквизиты и банк. реквизиты | [crm/requisites/](rest-docs/api-reference/crm/requisites/index.md), REST 3.0 — [rest-v3/requisites](rest-docs/api-reference/crm/rest-v3/requisites/index.md) |
| Дела (звонок, встреча, универсальное дело) | [crm.activity.todo.add](rest-docs/api-reference/crm/timeline/activities/todo/crm-activity-todo-add.md) и группы `crm.activity.*` ([timeline/](rest-docs/api-reference/crm/timeline/index.md)) |
| Комментарии в таймлайне | [crm.timeline.comment.add](rest-docs/api-reference/crm/timeline/comments/crm-timeline-comment-add.md) |
| Дубликаты | [crm/duplicates/](rest-docs/api-reference/crm/duplicates/index.md) |
| CRM-формы | [crm/form/](rest-docs/api-reference/crm/form/index.md) (`crm.form.*`) — приём заявок с сайта |
| Генератор документов | `crm.documentgenerator.*` ([crm/document-generator/](rest-docs/api-reference/crm/document-generator/index.md)) |
| Справочники и валюты | `crm.status.*`, `crm.currency.*`; REST 3.0 — `crm.dictionary.<справочник>.*` |
| Вид карточки | `crm.item.details.configuration.*`; REST 3.0 — `crm.<тип>.detailpagelayout.*` |
| Режим лидов (вкл/выкл) | `crm.lead.isenabled / enable / disable` (REST 3.0), [crm-settings-mode-get.md](rest-docs/api-reference/crm/crm-settings-mode-get.md) |
| Автоматизация CRM (роботы, триггеры) | см. [06-automation-events.md](06-automation-events.md) |

Типы и структура объектов: [crm/data-types.md](rest-docs/api-reference/crm/data-types.md), поля основных объектов: [crm/main-entities-fields.md](rest-docs/api-reference/crm/main-entities-fields.md), ограничения длины полей: [crm/field-length-limits.md](rest-docs/api-reference/crm/field-length-limits.md).

## 6. Типичные сценарии (туториалы в зеркале)

Папка [tutorials/crm/](rest-docs/tutorials/crm/index.md): добавление сделки/компании/контакта/реквизитов/дел, редактирование, выборки (в т.ч. по названию стадии, поставщики), виджеты CRM, аналитика. Типы полей — [tutorials/field-types/](rest-docs/tutorials/field-types/index.md), см. [05-user-fields.md](05-user-fields.md).

## 7. Ловушки

- Новую интеграцию начинать с REST 3.0 там, где метод в нём есть; иначе — классический `/rest/`, и в одном проекте чётко разделять оба вида.
- Регистр полей: `TITLE` (классика объектов) vs `title` (универсальные и REST 3.0). Смешивание → поле молча не применится.
- Права проверяются на каждый элемент: список «обрезается» по правам пользователя, от имени которого идёт запрос (вебхука).
- Обязательные поля и значения по умолчанию зависят от настроек портала (воронка, обязательные поля стадий). Проверять на тестовых данных до боевого запуска. *Не проверено на портале ЕС Транс.*
