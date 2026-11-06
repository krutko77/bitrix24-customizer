# 02. Как выполнять запросы к REST API

Источники: [settings/how-to-call-rest-api/](rest-docs/settings/how-to-call-rest-api/index.md), [rest-v3.md](rest-docs/api-reference/rest-v3.md), [settings/performance/huge-data.md](rest-docs/settings/performance/huge-data.md). Статус: *по документации*.

## 1. Структура запроса

```
https://<портал>/rest/<метод>?<параметры>                      # приложение, + auth=<TOKEN>
https://<портал>/rest/<USER_ID>/<КОД_ВЕБХУКА>/<метод>.json     # вебхук
```

- Простые вызовы допустимы через GET. Массивы и вложенные структуры — **POST + `Content-Type: application/json`** (поддерживает большинство методов). Также поддерживается `multipart/form-data`.
- Ответ по умолчанию JSON; XML — добавить `.xml` к имени метода (нужен редко).
- Рекомендуемые заголовки для POST/JSON: `Content-Type: application/json`, `Accept: application/json`, `User-Agent: имя-интеграции/версия`.
- Спецсимволы в параметрах (`& ? % [ ] #`) кодировать: [data-encoding.md](rest-docs/settings/how-to-call-rest-api/data-encoding.md). Особо проверять вложенные запросы в `batch`.
- Скачивание файлов по подписанным ссылкам (`DOWNLOAD_URL`, `urlMachine`) — отдельным GET с `User-Agent`, `Referer` (адрес портала) и `Accept-Language`; пустой/технический `User-Agent` может дать 404 от nginx.

## 2. Формат ответа

```json
{
  "result": { ... },
  "total": 73,            // только у списочных методов
  "next": 50,             // есть, если есть следующая страница
  "time": { "start":…, "finish":…, "duration":…, "processing":…, "operating":…, "operating_reset_at":… }
}
```

Ошибка: `{"error": "КОД", "error_description": "…"}` вместо `result`. Ветвиться по `error`, а не по тексту `error_description` (текст зависит от языка интерфейса). Подробно — [03-limits-and-errors.md](03-limits-and-errors.md).

## 3. Списочные методы и пагинация

- Страница — не более **50 элементов**.
- Первая страница — без `start`. Если в ответе есть `next` — передать его как `start` в следующий запрос; нет `next` → последняя страница.
- `total` считается при `start >= 0` и на больших выборках тормозит.
- Для выгрузки больших объёмов ([huge-data.md](rest-docs/settings/performance/huge-data.md)): сортировка по `id` ASC, фильтр `>id` = последний полученный id, `start = -1` (отключает подсчёт `total`), повторять, пока не вернулось меньше 50 записей. Между запросами — пауза (см. лимиты).
- В методах, которые без `select` возвращают только `id` (например, CRM REST 3.0), поля перечислять в `select`.

Пример выгрузки (идея; метод `crm.item.list`):

```json
{ "entityTypeId": 1, "order": {"id": "ASC"}, "filter": {">id": 0}, "select": ["id","title"], "start": -1 }
```

## 4. Пакетные запросы `batch`

- До **50** подзапросов за один HTTP-запрос. Вложенный `batch` запрещён (`ERROR_BATCH_METHOD_NOT_ALLOWED`); сверх 50 — `ERROR_BATCH_LENGTH_EXCEEDED`.
- Параметры: `cmd` (ключ — id подзапроса, значение — `метод?параметры` или объект), `halt` (`0` — продолжать при ошибке, `1` — остановиться; по умолчанию `false`).
- Результат предыдущего подзапроса можно подставить в следующий: `$result[id_подзапроса][поле]`.
- Ответ: `result.result` (данные по ключам), `result.result_error` (**всегда присутствует**; ошибки — записи в нём, пустой массив = успех), `result_total`, `result_next`.
- HTTP-статус `batch` может быть 200 даже при ошибках подзапросов — проверять `result_error`.
- `batch` экономит HTTP-запросы, но **не отменяет** лимит ресурсоёмкости вложенных методов.
- Для REST 3.0 есть `batch` 3.0 (`$ref`, `$refArray`): [batch-v3.md](rest-docs/settings/how-to-call-rest-api/batch-v3.md).

```json
{ "halt": 0,
  "cmd": { "get_user": "user.current", "get_departments": "department.get" } }
```

## 5. Две версии API: классическая и REST 3.0

| | Классическая (v1/v2) | REST 3.0 |
|---|---|---|
| Адрес | `/rest/…` | `/rest/api/…` |
| Вебхук | `/rest/<id>/<код>/<метод>` | `/rest/api/<id>/<код>/<метод>` |
| Параметры | GET/POST/JSON | **только POST + JSON** (в строке запроса не читаются); без параметров — GET или POST |
| Идемпотентность | нет | заголовок `Idempotency-Key` |
| Документация | страницы методов | + OpenAPI: метод `rest.documentation.openapi` (синоним `documentation`) — описание методов *именно вашего* портала |

- Обе версии работают одновременно; **не все методы переведены** на REST 3.0. В 2026 в REST 3.0 есть: задачи, CRM, База знаний 2.0, почта, торговый каталог, структура компании (`humanresources.*`), журнал событий, записи рабочего времени, follow-up звонков, форум, инфоблоки.
- Один и тот же метод может быть в обеих версиях с разными параметрами и ответом (например, `tasks.task.get`). В справочнике метод REST 3.0 помечен «v 3.0».
- В CRM для новой разработки — REST 3.0 (`crm.<тип>.<действие>`), старые `crm.lead.*`, `crm.deal.*`… «развитие остановлено, но продолжают работать». Подробно — [04-crm.md](04-crm.md).
- SDK: REST 3.0 поддерживают b24jssdk (`$b24.actions.v3`), b24pysdk (`prefer_version=3`), b24gosdk; **не** поддерживают b24phpsdk, BX24.js, CRest. См. [09-sdk-and-tools.md](09-sdk-and-tools.md).
- Ошибка `BITRIX_REST_V3_EXCEPTION_INVALIDJSONEXCEPTION` — тело не в JSON.

## 6. Первый вызов: чек-лист

1. Вебхук создан, скоупы выбраны.
2. `POST …/user.current.json` с `{}` — проверка авторизации.
3. `result` пришёл → пробуем нужный метод; `error` → [03-limits-and-errors.md](03-limits-and-errors.md).
4. В генераторе запросов в интерфейсе («Разработчикам») можно собрать вызов и скачать пример на PHP.

## 7. Смена адреса портала

Если домен портала изменился (например, сменён адрес в облаке), запросы на старый адрес редиректятся — обработка описана в [change-domen.md](rest-docs/settings/how-to-call-rest-api/change-domen.md). Хранить адрес портала в конфиге, а не в коде.
