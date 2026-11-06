# 05. Пользовательские поля (UF)

Источники: [tutorials/field-types/index.md](rest-docs/tutorials/field-types/index.md), [userfieldconfig/index.md](rest-docs/api-reference/crm/universal/userfieldconfig/index.md), [userfieldconfig-add.md](rest-docs/api-reference/crm/universal/userfieldconfig/userfieldconfig-add.md), [crm-userfield-types.md](rest-docs/api-reference/crm/universal/user-defined-fields/crm-userfield-types.md). Статус: *по документации*.

## 1. Какие методы существуют

| Семейство | Методы | Регистр параметров | Где применять |
|---|---|---|---|
| **`userfieldconfig.*`** (скоуп `userfieldconfig` + скоуп модуля, например `crm`) | `getTypes`, `add`, `get`, `list`, `update`, `delete` | camelCase: `userTypeId`, `multiple`, `settings` | Единый способ для CRM, RPA и других модулей, где есть UF. Предпочтителен для новых задач |
| **`crm.<объект>.userfield.*`** (классика) | `add`, `get`, `list`, `update`, `delete` у `crm.deal`, `crm.lead`, `crm.contact`, `crm.company`… | ВЕРХНИЙ: `USER_TYPE_ID`, `MULTIPLE`, `SETTINGS` | Существующие интеграции |
| **REST 3.0 `crm.<тип>.field.custom.*`** | `add`, `get`, `list`, `update`, `delete` | camelCase | Новая версия CRM |
| Поля задач / пользователей | `tasks.task.*` (UF), [user/userfields/](rest-docs/api-reference/user/userfields/index.md) (`user.userfield.*`) | — | Задачи, сотрудники |

Права: для CRM — право «Разрешить изменять настройки» на объект.

## 2. Идентификаторы `entityId` (для userfieldconfig)

`CRM_LEAD`, `CRM_CONTACT`, `CRM_COMPANY`, `CRM_DEAL`, `CRM_QUOTE`, `CRM_INVOICE`, `CRM_SMART_INVOICE`, `CRM_REQUISITE`, `CRM_SMART_DOCUMENT`, `CRM_SMART_B2E_DOC`;
смарт-процесс — `CRM_{id}` (⚠ `id` из `crm.type.list`, это не `entityTypeId`); RPA — `RPA_{id}`.

## 3. Код (имя) поля

- **`userfieldconfig.add`:** `fieldName` в формате `UF_{ИДЕНТИФИКАТОР_ОБЪЕКТА}_{POSTFIX}` — например `UF_CRM_7_NEW_REST_LIST_2026` для смарт-процесса. Символы `A-Z`, `0-9`, `_`; максимум 50 символов; уникален в рамках объекта.
- **Классические `crm.<объект>.userfield.add`:** к переданному коду система **сама добавляет префикс** `UF_CRM_` (`MANAGER_NOTE` → `UF_CRM_MANAGER_NOTE`; `UF_MANAGER_NOTE` → `UF_CRM_MANAGER_NOTE`; `UF_CRM_MANAGER_NOTE` без изменений). Лимит 50 символов считается вместе с префиксом, то есть на сам код остаётся 43. Длиннее — ошибка `ERROR_CORE` («Имя поля слишком длинное»).
- **Формат имени в ответах:** в классических методах объектов — `UF_CRM_…`; в универсальных `crm.item.*` и REST 3.0 те же поля приходят в camelCase (`ufCrm10Digit`, `ufCrm2_1639669411830`, `ufCrmBindOne` — примеры из документации). Точное имя после создания читать через `crm.item.fields` / `*.userfield.list` / `userfieldconfig.list`, а не собирать вручную.

## 4. Типы полей

Список возвращает `crm.userfield.types` / `userfieldconfig.getTypes`. Стандартные:
`string`, `integer`, `double`, `boolean`, `datetime`, `enumeration` (список), `iblock_section`, `iblock_element`, `employee`, `crm_status`, `crm`, `address`, `money`, `url`, `file`; в выдаче `userfieldconfig.getTypes` встречается также `date`. Набор зависит от метода и портала — актуальный список запрашивать `crm.userfield.types` / `userfieldconfig.getTypes`. Плюс **пользовательские типы** приложения (`userfieldtype.add`, см. [07-apps-and-placements.md](07-apps-and-placements.md)).

Параметры создания (`userfieldconfig.add`): `moduleId`, `field` { `entityId`, `fieldName`, `userTypeId`, `multiple` (`Y`/`N`), `mandatory`, `showFilter`, `editInList`, `isSearchable`, `sort`, `xmlId`, `settings`, `editFormLabel`, `helpMessage`, `enum` }. Неподдерживаемые ключи (`showInList`, `listColumnLabel`, `listFilterLabel`, `errorMessage`, `label`) **игнорируются без ошибки**. `settings` зависят от типа (длина, регулярка, точность и т. д.).

```json
{
  "moduleId": "crm",
  "field": {
    "entityId": "CRM_DEAL",
    "fieldName": "UF_CRM_TRIP_NUMBER",
    "userTypeId": "string",
    "editFormLabel": { "ru": "Номер рейса" },
    "mandatory": "N", "showFilter": "Y"
  }
}
```
*(пример собран по описанию параметров; на портале не запускался)*

## 5. Что хранит значение (важно для записи и чтения)

В API значение — не то, что видно в карточке:

| Тип | В значении лежит |
|---|---|
| `enumeration` | **id** варианта списка (не текст) |
| `crm` | Ссылка на элемент CRM `{PREFIX}_{ID}`: лид `L_4`, сделка `D_1`, контакт `C_2`, компания `CO_3`, новый счёт `SI_7`, смарт-процесс `T80_6`. Множественное — массив (`["CO_1","CO_2"]`). Источник: [crm/data-types.md](rest-docs/api-reference/crm/data-types.md) |
| `crm_status` | Строковый `STATUS_ID` из справочника CRM (`IT`) |
| `iblock_element` | id элементов инфоблока (списка/каталога) |
| `iblock_section` | id разделов (вложенные в значение не входят) |
| Множественное (`MULTIPLE=Y`) | Всегда **массив**, даже при одном значении |

`enumeration` — список принадлежит полю; `crm_status` — общий справочник CRM.

## 6. Молчаливые отказы (ошибки НЕ будет)

По документации метод не вернёт ошибку, если:
- в `enumeration`, `iblock_element`, `iblock_section` передан **текст** вместо id — поле обнулится (в ответе `0`), а отбор по тексту вернёт посторонние записи;
- в `crm` / `crm_status` передан текст, несуществующий код или произвольный префикс (`XX_1`) — сохранится дословно;
- `crm.deal.userfield.update` не принимает `USER_TYPE_ID` и `MULTIPLE` и молча игнорирует их — **тип и множественность после создания не меняются**;
- в `field` переданы неподдерживаемые ключи.

**Вывод:** результат записи UF проверять **чтением** (`get`/`list`), а не кодом ответа. Тип поля продумывать до создания (изменить нельзя — создавать новое поле и переносить данные).

## 7. Отдельные сценарии

В зеркале: [tutorials/field-types/](rest-docs/tutorials/field-types/index.md) — UF в смарт-процессе, точность числового поля, автозаполнение зависимого поля, поля привязки к CRM / справочнику CRM / инфоблокам, `enumeration`.

## 8. Ограничения

Длина стандартных полей и способ узнать лимиты UF: [crm/field-length-limits.md](rest-docs/api-reference/crm/field-length-limits.md).
