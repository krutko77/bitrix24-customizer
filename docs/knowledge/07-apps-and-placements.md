# 07. Приложения, встройка в интерфейс (placement), Push&Pull

Источники: [local-integrations/](rest-docs/local-integrations/index.md), [settings/app-installation/](rest-docs/settings/app-installation/index.md), [api-reference/widgets/](rest-docs/api-reference/widgets/index.md), [placements.md](rest-docs/api-reference/widgets/placements.md), [settings/interactivity/](rest-docs/settings/interactivity/index.md). Статус: *по документации*.

## 1. Виды локальных приложений

Локальное приложение создаётся **на конкретном портале** и работает только там. Раздел: *Разработчикам → Готовые сценарии → Другое → Локальное приложение*. Права на создание приложений открывает администратор: *Настройки → Настройки Битрикс24 → Безопасность → Интеграции Битрикс24* («Кому разрешить создавать приложения»).

| Вид | Где выполняется код | Нужен свой сервер | Получает события | Подходит для |
|---|---|---|---|---|
| **Статичное** ([static-local-app.md](rest-docs/local-integrations/static-local-app.md)) | В браузере, во фрейме Битрикс24 (ZIP с `index.html`, опц. `install.html`) | Нет | **Нет** (нет серверного обработчика) | Простые экраны, виджеты, отчёты по данным текущего пользователя |
| **Серверное с интерфейсом** ([serverside-local-app-with-ui.md](rest-docs/local-integrations/serverside-local-app-with-ui.md)) | На вашем сервере + страница во фрейме | Да | Да | Интерфейс + серверная логика, секреты, события |
| **Серверное без интерфейса** ([serverside-local-app-with-no-ui.md](rest-docs/local-integrations/serverside-local-app-with-no-ui.md)) | На вашем сервере, интерфейса нет | Да | Да | Фоновая синхронизация, обработка событий, роботы |

Форма приложения: название, права (скоупы), адрес обработчика / архив, «Путь для первоначальной установки», название пункта меню. После сохранения портал показывает **код приложения (`client_id`) и секретный ключ (`client_secret`)** — положить на сервер, не в браузер.

Правила завершения установки ([installation-finish.md](rest-docs/settings/app-installation/installation-finish.md)):
- *без интерфейса*: поле «Название пункта меню» пустое, опцию «Приложение само завершает установку» не включать; на URL установки придёт POST с OAuth-данными — обработать и сохранить токены;
- *с интерфейсом*: заполнить «Название пункта меню» и включить «Приложение само завершает установку»; приложение само вызывает завершение (`BX24.installFinish()`), иначе установка «зависнет» и события/виджеты не заработают.

## 2. Клиентский JS: `BX24.js`

Подключение: `<script src="//api.bitrix24.tech/api/v1/"></script>`, затем `BX24.init(callback)`. Даёт готовую авторизацию текущего пользователя, `BX24.callMethod`, `BX24.callBatch`, диалоги, управление окном и размером фрейма, хранение настроек на стороне Битрикс24. Работает только во фрейме приложения. Документация: [sdk/bx24-js-sdk/](rest-docs/sdk/bx24-js-sdk/index.md). Для REST 3.0 `BX24.js` не подходит.

## 3. Встраивание виджетов (placement)

Виджет — интерфейс приложения в **точке встраивания**: вкладка карточки сделки, пункт меню, кнопка, боковая панель.

Как работает:
1. `placement.bind` (`PLACEMENT` = код точки, `HANDLER` = URL) — регистрирует обработчик.
2. Пользователь открывает место → Битрикс24 **POST-ом** шлёт на `HANDLER` авторизацию и контекст (например id сделки).
3. Обработчик отвечает страницей, **разрешённой к показу во фрейме**.
4. Из фрейма приложение вызывает REST от лица пользователя.

Условия:
- Скоуп **`placement`** + скоуп инструмента точки (указан в шапке страницы точки; например `crm` для `CRM_*`).
- `placement.bind` / `unbind` — администратор (в локальном приложении — ещё и сотрудник с правом создавать приложения). **Вебхуком вызвать нельзя.**
- Виджет виден только тем, кому открыт доступ к приложению (проверяется при каждом показе).
- Адрес обработчика — публичный; виджеты не показываются, пока установка не завершена, даже если `placement.bind` вернул успех.
- Фактический список мест для вашего портала: `placement.list`; зарегистрированные: `placement.get`.

Частые точки (полный каталог — [placements.md](rest-docs/api-reference/widgets/placements.md)):

| Нужно | Код |
|---|---|
| Вкладка в карточке CRM | `CRM_DEAL_DETAIL_TAB`, `CRM_LEAD_DETAIL_TAB`, `CRM_CONTACT_DETAIL_TAB`, `CRM_COMPANY_DETAIL_TAB`, для смарт-процесса `CRM_DYNAMIC_<id>_DETAIL_TAB` |
| Кнопка/меню в карточке | `CRM_XXX_DETAIL_TOOLBAR`, `CRM_XXX_DETAIL_ACTIVITY` |
| Действие в списке | `CRM_XXX_LIST_MENU` (элемент), `CRM_XXX_LIST_TOOLBAR` (весь список) |
| Вкладка/панель в задаче | `TASK_VIEW_TAB`, `TASK_VIEW_SIDEBAR`, `TASK_VIEW_TOP_PANEL`, `TASK_LIST_CONTEXT_MENU` |
| Свой раздел на всю область | `LEFT_MENU`, `CRM_ANALYTICS_MENU`, `BI_ANALYTICS_MENU` |
| Чат | `IM_TEXTAREA`, `IM_SIDEBAR`, `IM_CONTEXT_MENU` |
| Кнопка в дизайнере роботов | `CRM_XXX_ROBOT_DESIGNER_TOOLBAR` |
| Подстановка данных (поиск клиента, автозаполнение реквизитов) | `CRM_DETAIL_SEARCH`, `CRM_REQUISITE_AUTOCOMPLETE`, `CRM_BANK_DETAIL_AUTOCOMPLETE` |
| Фоновый код на всех страницах | `PAGE_BACKGROUND_WORKER` |
| Открытие приложения по ссылке | `REST_APP_URI` |

(`XXX` = `LEAD`, `DEAL`, `CONTACT`, `COMPANY`, `QUOTE`, `SMART_INVOICE`, `ORDER`, `ACTIVITY` или `DYNAMIC_<id>` для смарт-процесса — набор зависит от точки.)

Не через `placement.bind`: пункт главного меню приложения (настройки приложения), страница настройки коннектора (`imconnector.register`), **пользовательский тип поля** (`userfieldtype.add`).

## 4. Пользовательские типы полей

`userfieldtype.add` регистрирует **тип** UF со своим интерфейсом просмотра/редактирования в карточке CRM (не само поле). Группа [widgets/user-field/](rest-docs/api-reference/widgets/user-field/index.md); о типах — [05-user-fields.md](05-user-fields.md).

## 5. Системные события приложения

`ONAPPINSTALL`, `ONAPPUPDATE`, `ONAPPUNINSTALL`, `ONAPPPAYMENT`, `ONAPPMETHODCONFIRM`, `ONAPPUSERREADY`… — [api-reference/common/events/](rest-docs/api-reference/common/events/index.md). Проверка `application_token` — [06-automation-events.md](06-automation-events.md).

## 6. Push&Pull (обновление интерфейса без перезагрузки)

Только в контексте приложения, скоуп `pull`. Доставляет **собственные события приложения** (не события Битрикс24 о сделках — для них `event.bind`).
- Каналы: `shared` (общий), `private` (для одного пользователя).
- Клиент в браузере — `BX.PullClient`; собственный клиент — [custom-push-and-pull-client.md](rest-docs/settings/interactivity/custom-push-and-pull-client.md).
- REST: `pull.application.config.get`, `pull.application.event.add`, `pull.application.push.add`.

## 7. Хостинг серверных приложений

Серверному приложению нужен публичный HTTPS-адрес (обработчик, страница фрейма, события). Есть ли у ЕС Транс подходящий сервер, не выяснено (см. `docs/gaps.md`). Кода приложения в проекте пока нет. Также у Битрикс24 есть сервис **Вайбкод** (генерация и хостинг приложения по описанию) — [ai-tools/vibecode.md](rest-docs/ai-tools/vibecode.md); применимость для ЕС Транс не оценивалась.

## 8. Тиражные приложения (Маркетплейс)

Для распространения на разные порталы: кабинет разработчика, технологическое партнёрство, модерация — [market/](rest-docs/market/index.md). Для задач внутри одной компании не нужны.
