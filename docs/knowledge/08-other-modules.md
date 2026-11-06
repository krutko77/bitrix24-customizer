# 08. Остальные модули REST API (карта)

Источник: индекс [reference/methods-index.md](reference/methods-index.md) и разделы зеркала `rest-docs/api-reference/`. Здесь — только навигация и то, что подтверждено прочитанными страницами. Подробные справочники по этим модулям пока не написаны. Статус: *по документации*; скоупы каждого метода смотреть на его странице и в [scopes/](rest-docs/api-reference/scopes/permissions.md).

Поиск метода: `grep -i 'tasks.task' docs/knowledge/reference/methods-index.md`.

## Таблица разделов

| Область | Раздел зеркала | Ключевые методы / заметки |
|---|---|---|
| **Задачи** | [tasks/](rest-docs/api-reference/tasks/index.md) | `tasks.task.add / get / list / update / delete`, `tasks.task.getFields`, чек-листы, комментарии, учёт времени, делегирование, `approve`/`disapprove`, зависимости, потоки (`flow`), стадии. Для части методов есть версия **v 3.0** (например [tasks-task-add-rest-v3.md](rest-docs/api-reference/tasks/tasks-task-add-rest-v3.md)). События задач — [events-tasks/](rest-docs/api-reference/tasks/events-tasks/index.md). Старые `task.item.*` — устаревшая ветка (`tasks/deprecated`) |
| **Пользователи** | [user/](rest-docs/api-reference/user/index.md) | [`user.get`](rest-docs/api-reference/user/user-get.md) (по фильтру), [`user.current`](rest-docs/api-reference/user/user-current.md), [`user.add`](rest-docs/api-reference/user/user-add.md) (по документации это **приглашение** пользователя), [`user.update`](rest-docs/api-reference/user/user-update.md), `user.search`, `user.fields`, UF пользователя — [user/userfields/](rest-docs/api-reference/user/userfields/index.md) |
| **Структура компании** | [departments/](rest-docs/api-reference/departments/department-get.md) | `department.get / add / update / delete`, `department.fields`; сотрудники подразделения — `departments/employee/` |
| **Диск** | [disk/](rest-docs/api-reference/disk/index.md) | хранилища [`disk.storage.getList`](rest-docs/api-reference/disk/storage/disk-storage-get-list.md), папки, файлы [`disk.file.get`](rest-docs/api-reference/disk/file/disk-file-get.md), загрузка [`disk.folder.uploadFile`](rest-docs/api-reference/disk/folder/disk-folder-upload-file.md), версии, права, публичные ссылки. Общий разбор файлов — [files/](rest-docs/api-reference/files/index.md) (`how-to-upload-files`, `how-to-download-files`, `how-to-update-files`) |
| **Календарь** | [calendar/](rest-docs/api-reference/calendar/) | `calendar.event.add / get / getbyid / get.nearest / update / delete`, секции `calendar.section.*`, [`calendar.event.add`](rest-docs/api-reference/calendar/calendar-event/calendar-event-add.md) |
| **Универсальные списки** | [lists/](rest-docs/api-reference/lists/index.md) | списки `lists.add / get / update / delete`, поля `lists.field.*`, элементы [`lists.element.add`](rest-docs/api-reference/lists/elements/lists-element-add.md) / `get` / `update` / `delete`, разделы `lists.section.*`. Уместны для справочников и простых реестров без CRM |
| **Хранилище данных** | [entity/](rest-docs/api-reference/entity/index.md) | `entity.add`, `entity.item.add` ([пример](rest-docs/api-reference/entity/items/entity-item-add.md)): свои структуры данных приложения. Для данных, привязанных к бизнесу, обычно удобнее смарт-процесс или список |
| **Чаты, уведомления** | [chats/](rest-docs/api-reference/chats/im-chat-add.md) | `im.chat.add`, `im.notify.personal.add` и др. — [chats/notifications/](rest-docs/api-reference/chats/notifications/im-notify-personal-add.md) |
| **Чат-боты** | [chat-bots/](rest-docs/api-reference/chat-bots/index.md) | Новая бот-платформа `imbot.v2.*` (регистрация — [`imbot.v2.Bot.register`](rest-docs/api-reference/chat-bots/chat-bots-v2/imbot.v2/bots/bot-register.md)) и **устаревший** `imbot.*` в `chat-bots/outdated/` (напр. `imbot.register`). Для новых ботов смотреть v2 |
| **Открытые линии** | [imopenlines/](rest-docs/api-reference/imopenlines/index.md) | Свои каналы: `imconnector.*` ([`imconnector.register`](rest-docs/api-reference/imopenlines/imconnector/imconnector-register.md)); управление диалогами и статистика |
| **Телефония** | [telephony/](rest-docs/api-reference/telephony/index.md) | Внешние звонки `telephony.externalcall.*`, запись и расшифровка звонков, события; встроенная Voximplant (`voximplant.*`) — в том же разделе документации |
| **Рабочие группы и проекты** | [sonet-group/](rest-docs/api-reference/sonet-group/index.md) | [`socialnetwork.api.workgroup.list`](rest-docs/api-reference/sonet-group/socialnetwork-api-workgroup-list.md), участники, Скрам (бэклог, спринты) |
| **Лента новостей** | [log/](rest-docs/api-reference/log/index.md) | [`log.blogpost.add`](rest-docs/api-reference/log/log-blogpost-add.md) — сообщение в Ленту, комментарии, события |
| **Генератор документов** | [document-generator/](rest-docs/api-reference/document-generator/index.md) | Шаблоны и создание документов из данных CRM (`documentgenerator.*`); в CRM — `crm.documentgenerator.*` |
| **Торговый каталог и склад** | [catalog/](rest-docs/api-reference/catalog/index.md) | Товары `catalog.product.*` (есть v 3.0), цены, остатки, документы склада, `iblock.*` — [iblock/](rest-docs/api-reference/iblock/index.md) |
| **Интернет-магазин** | [sale/](rest-docs/api-reference/sale/index.md), [pay-system/](rest-docs/api-reference/pay-system/index.md) | Заказы `sale.order.*`, корзина, доставка, платёжные системы, кассы |
| **Рабочее время** | [timeman/](rest-docs/api-reference/timeman/index.md) | `timeman.open / close / pause / status`, графики, табели |
| **Почта и сообщения** | [mail/](rest-docs/api-reference/mail/index.md), [mailservice/](rest-docs/api-reference/mailservice/), [messageservice/](rest-docs/api-reference/messageservice/index.md) | Почтовые ящики, почтовые сервисы; свои SMS-провайдеры — [`messageservice.sender.add`](rest-docs/api-reference/messageservice/messageservice-sender-add.md) |
| **Согласия, опросы** | [user-consent/](rest-docs/api-reference/user-consent/index.md), [vote/](rest-docs/api-reference/vote/index.md) | Соглашения и согласия пользователей, голосования |
| **КЭДО** | [sign/](rest-docs/api-reference/sign/index.md) | Кадровый электронный документооборот (`sign.b2e.*`) |
| **Онлайн-запись** | [booking/](rest-docs/api-reference/booking/index.md) | `booking.v1.*` — ресурсы, бронирования, лист ожидания |
| **BI-аналитика** | [biconnector/](rest-docs/api-reference/biconnector/index.md) | Свои источники и наборы данных для BI Конструктора |
| **Журнал событий** | [event-log/](rest-docs/api-reference/event-log/index.md) | `main.eventlog.*` (REST 3.0) |
| **Сайты, магазины** | [landing/](rest-docs/api-reference/landing/index.md) | Управление сайтами, страницами, блоками (CRM-формы — в [04-crm.md](04-crm.md)) |
| **Форум, база знаний** | [forum/](rest-docs/api-reference/forum/index.md), [note/](rest-docs/api-reference/note/index.md) | В REST 3.0 |
| **AI** | [ai/](rest-docs/api-reference/ai/index.md) | `ai.engine.register / list / unregister` — подключение своего ИИ-сервиса |
| **Системные** | [common/](rest-docs/api-reference/common/), [scopes/](rest-docs/api-reference/scopes/permissions.md) | `scope`, `methods`, `app.info`, `server.time`, `user.admin`, права доступа |

## Оговорки

- Некоторые разделы помечены как REST 3.0 или имеют «v 3.0»-версии методов — перед использованием проверить, какая страница открыта ([02-rest-requests.md](02-rest-requests.md)).
- Раздел `outdated/` (и `deprecated/`) есть почти в каждом модуле — это устаревшие методы; новым интеграциям не подходят.
- Доступность отдельных модулей (Скрам, КЭДО, Онлайн-запись, телефония и т. п.) зависит от тарифа и настроек портала. Что включено на портале ЕС Транс — **не выяснено** (см. [../gaps.md](../gaps.md)).
- Полные данные о правах и полях объекта брать из страницы метода, а не из этой таблицы: здесь перечислены только главные методы.
