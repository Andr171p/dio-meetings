# Сервис для создания протокола совещания

## REST API

## Основные сущности

 * ### <b>FileMetadata</b>

Метаданные файла загруженного или сформированного файла.

```json
{
  "id": "1ef0141d-57a2-41d3-b1d2-3ef77290a8d8",
  "file_name": "string",
  "key": "string",
  "bucket": "string",
  "size": 0.00,
  "format": "string",
  "type": "string",
  "uploaded_date": "2025-06-10T11:03:28.263849"
}
```
 * <b>id</b> - Уникальный ID файла в формате UUID4, присваивается при создании.
 * <b>file_name</b> - Имя файла.
 * <b>key</b> - Ключ / имя файла в S3 хранилище.
 * <b>bucket</b> - 'Бакет' (коллекция) в S3 хранилище.
 * <b>size</b> - Размер файла в МБ.
 * <b>format</b> - Формат / расширение файла.
 * <b>type</b> - Тип файла. Разрешённые типы файлов:
    - AUDIO (.mp3, .ogg, .pcm, .wav)
    - DOCUMENT (.docx, .pdf, .doc)
 * <b>uploaded_date</b> - Дата загрузки файла.


 * ### <b>Task</b>

Задача на генерацию протокола совещания.

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "file_id": "1ef0141d-57a2-41d3-b1d2-3ef77290a8d8",
  "status": "string",
  "result_id": null,
  "created_at": "2025-06-10T11:03:28.263849",
  "updated_at": "2025-06-10T11:03:28.263849"
}
```

 * <b>id</b> - Уникальный ID задачи в формате UUID4, присваивается при создании.
 * <b>file_id</b> - ID аудио записи совещания.
 * <b>status</b> - Статус выполнения задачи:
   - NEW - Новая задача (после создания задачи).
   - RUNNING - Задача выполняется.
   - DONE - Задача успешно завершена.
   - ERROR - Задача остановилась из-за ошибки.
 * <b>result_id</b> - ID сформированного протокола совещания в формате UUID4 (Приходит вместе с статусом DONE).
 * <b>created_at</b> - Дата и время создания задачи.
 * <b>updated_at</b>-  Дата обновления статуса задачи.

## Ресурсы

 * ### `/api/v1/audio`
   Работа с аудио записями совещания.
 * ### `/api/v1/tasks`
   Создание и получения статусов задач
 * ### `/api/v1/documents`
   Работа со сформированными протоколами совещаний

## Методы `/api/v1/audio`

 * ### <b>POST</b> `/upload`

Загружает аудио запись совещания.

<b>Request</b><sup>required</sup>

 * Content-type: `multipart/form-data`
 * Body:
   -  audio_file: Аудио файл для загрузки.

<b>Responses</b>

| Статус код | Описание                        |
|------------|---------------------------------|
 | 201        | Успешная загрузка аудио файла   |
| 500        | Ошибка при загрузке аудио файла |

 * Body (201 CREATED):
```json
{
  "id": "1ef0141d-57a2-41d3-b1d2-3ef77290a8d8",
  "file_name": "string",
  "key": "string",
  "bucket": "string",
  "size": 0.00,
  "format": "mp3",
  "type": "AUDIO",
  "uploaded_date": "2025-06-10T11:03:28.263849"
}
```
 * Body (500 INTERNAL SERVER ERROR)

```json
{"detail": "UPLOADING_ERROR"}
```

<b>Пример запроса</b>

```bash
curl -X POST "http://your-api-domain.com/api/v1/audio/upload" \
  -H "Content-type: multipart/form-data" \
  -F "audio_file=@meeting_recording.mp3"
```

 * ### GET `/{file_id}/download`

Скачивает аудио запись совещания.

<b>Parameters</b>

| Имя     | Тип  | Описание       |
|---------|------|----------------|
| file_id | UUID | ID аудио файла |

<b>Responses</b>

| Статус код | Описание                          |
|------------|-----------------------------------|
| 200        | Успешное скачивание аудио файла   |
| 404        | Аудио файл не найден              |
| 500        | Ошибка при скачивании аудио файла |

<b>Пример запроса</b>

```bash
curl -X GET "http://your-api-domain.com/api/v1/audio/123e4567-e89b-12d3-a456-426614174000/download" \
  --output meeting_recording.mp3
```

 * ### DELETE `/{file_id}`

Удаляет аудио запись совещания.

<b>Parameters</b><sup>required</sup>

| Имя     | Тип  | Описание       |
|---------|------|----------------|
| file_id | UUID | ID аудио файла |

<b>Responses</b>

| Статус код | Описание                        |
|------------|---------------------------------|
| 204        | Успешное удаление аудио файла   |
| 404        | Аудио файл не найден            |
| 500        | Ошибка при удалении аудио файла |

<b>Пример запроса</b>

```bash
curl -X DELETE "http://your-api-domain.com/api/v1/audio/123e4567-e89b-12d3-a456-426614174000"
```


 * ### GET `/{file_id}`

Получает метаданные аудио файла.

<b>Parameters</b><sup>required</sup>

| Имя     | Тип  | Описание       |
|---------|------|----------------|
| file_id | UUID | ID аудио файла |

<b>Responses</b>

| Статус код | Описание                                  |
|------------|-------------------------------------------|
| 200        | Успешное получение метаданных аудио файла |
| 404        | Аудио файл не найден                      |
| 500        | Ошибка при получении метаданных           |

 * Body (200 OK)

```json
{
  "id": "1ef0141d-57a2-41d3-b1d2-3ef77290a8d8",
  "file_name": "string",
  "key": "string",
  "bucket": "string",
  "size": 0.00,
  "format": "mp3",
  "type": "AUDIO",
  "uploaded_date": "2025-06-10T11:03:28.263849"
}
```

 * Body (404 NOT FOUND)

```json
{"detail": "NOT_FOUND"}
```

 * Body (500 INTERNAL SERVER ERROR)

```json
{"detail": "RECEIVING_ERROR"}
```

 * ### GET `/filter?start={date}&end={date}`

Фильтрует загруженные аудио файлы по заданному промежутку дат.

<b>Query Parameters</b><sup>required</sup>

| Имя   | Тип      | Описание                               |
|-------|----------|----------------------------------------|
| start | datetime | Стартовая дата в формате (YYYY-MM-DD). |
| end   | datetime | Конечная дата  в формате (YYYY-MM-DD)  |

<b>Responses</b>

| Статус код | Описание                          |
|------------|-----------------------------------|
| 200        | Аудио файлы успешно отфильтрованы |
| 500        | Ошибка при фильтрации             |

* Body (200 OK)

```json
[
  {
    "id": "1ef0141d-57a2-41d3-b1d2-3ef77290a8d8",
    "file_name": "string",
    "key": "string",
    "bucket": "string",
    "size": 0.00,
    "format": "mp3",
    "type": "AUDIO",
    "uploaded_date": "2025-06-10T11:03:28.263849"
  }
]
```

 * Body (500 INTERNAL SERVER ERROR)

```json
{"detail": "RECEIVING_ERROR"}
```

<b>Пример запроса</b>

```bash
curl -X GET "http://your-api-domain.com/api/v1/audio/?date=2023-01-01&mode=after"
```


 * ### GET `/today`

Возвращает все сегодняшние аудиозаписи.

<b>Responses</b>
 
| Статус код | Описание                    |
|------------|-----------------------------|
 | 200        | Успешное получение данных   |
| 500        | Ошибка при получении данных |

 * Body (200 OK)

```json
[
  {
    "id": "1ef0141d-57a2-41d3-b1d2-3ef77290a8d8",
    "file_name": "string",
    "key": "string",
    "bucket": "string",
    "size": 0.00,
    "format": "mp3",
    "type": "AUDIO",
    "uploaded_date": "2025-06-10T11:03:28.263849"
  }
]
```

 * Body (500 INTERNAL SERVER ERROR)

```json
{"detail": "RECEIVING_ERROR"}
```


 * ### GET `/{file_id}/document`

Получает метаданные сформированного протокола совещания.

<b>Parameters</b><sup>required</sup>

| Имя     | Тип  | Описание       |
|---------|------|----------------|
| file_id | UUID | ID аудио файла |

<b>Responses</b>

| Статус код | Описание                                     |
|------------|----------------------------------------------|
 | 200        | Успешное получение метаданных                |
 | 404        | Для этого аудиофайла не сформирован протокол |
| 500        | Ошибка при получении метаданных              |

 * Body (200 OK)

```json
{
    "id": "1ef0141d-57a2-41d3-b1d2-3ef77290a8d8",
    "file_name": "string",
    "key": "string",
    "bucket": "string",
    "size": 0.00,
    "format": "DOCX",
    "type": "DOCUMENT",
    "uploaded_date": "2025-06-10T11:03:28.263849"
  }
```

 * Body (404 NOT FOUND)

```json
{"detail": "NOT_FOUND"}
```

 * Body (500 INTERNAL SERVER ERROR)

```json
{"detail":  "RECEIVING_ERROR"}
```


## Методы `/api/v1/tasks`

 * ### POST ``

Создаёт задачу на генерацию протокола совещания.

<b>Request</b><sup>required</sup>

 * Content-type: `application/json`
 * Body:

```json
{"file_id": "1ef0141d-57a2-41d3-b1d2-3ef77290a8d8"}
```

<b>file_id</b> - ID аудио файла для которого нужно сделать протокол совещания.

<b>Responses</b>

| Статус код | Описание                   |
|------------|----------------------------|
| 200        | Успешное создание задачи   |
| 500        | Ошибка при создании задачи |

 * Body (200 OK)

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "file_id": "1ef0141d-57a2-41d3-b1d2-3ef77290a8d8",
  "status": "NEW",
  "result_id": null,
  "created_at": "2025-06-10T11:03:28.263849",
  "updated_at": "2025-06-10T11:03:28.263849"
}
```

 * Body (500 INTERNAL SERVER ERROR)

```json
{"detail": "NOR_CREATED"}
```

 * ### GET `/{task_id}`

Получает статус текущей задачи.

<b>Parameters</b>

| Имя     | Тип  | Описание                                   |
|---------|------|--------------------------------------------|
| task_id | UUID | ID задачи, присваивается после её создания |


<b>Responses</b>

| Статус код | Описание                          |
|------------|-----------------------------------|
| 200        | Успешное получение статуса задачи |
| 404        | Задача не найдена                 |

 * Body (200 OK)

```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "file_id": "1ef0141d-57a2-41d3-b1d2-3ef77290a8d8",
  "status": "RUNNING",
  "result_id": null,
  "created_at": "2025-06-10T11:03:28.263849",
  "updated_at": "2025-06-10T11:03:28.263849"
}
```

 * Body (404)

```json
{"detail": "NOT_FOUND"}
```


## Методы `/api/v1/documents`

 * ### GET  `/{result_id}/download`

Скачивает сформированный протокол совещания.

<b>Parameters</b>

| Имя       | Тип  | Описание                     |
|-----------|------|------------------------------|
| result_id | UUID | ID сформированного протокола |

<b>Responses</b>

| Статус код | Описание                      |
|------------|-------------------------------|
| 200        | Успешное скачивание документа |
| 404        | Документ не найден            |

<b>Headers</b>

 * Content-Type: `application/vnd.openxmlformats-officedocument.wordprocessingml.document`
 * Content-Disposition: `attachment; filename*=UTF-8''{Имя файла}`
 * Content-Length: Длина контента файла.

<b>Пример запроса</b>

```bash
curl -X GET "http://your-api-domain.com/api/v1/documents/123e4567-e89b-12d3-a456-426614174000/download" \
  - OJ
```
