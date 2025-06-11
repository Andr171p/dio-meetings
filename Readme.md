# Сервис для создания протокола совещания

## REST API

## Meetings

Ресурс для работы с аудио записями встреч / совещаний.

### Базовый url `/api/v1/meetings`

 * ### POST `/upload`
  
   Метод для загрузки аудио записи встречи.</br></br>

   <b>Request body</b>:</br>
  
   Headers: ```multipart/form-data```</br>

   Parameters:
    - <b>name</b>: "string" - Тема/Название встречи
    - <b>speakers_count</b>: integer - количество активных спикеров
   
   Data: bytes</br></br>

   <b>Response body</b>:</br>
    - <b>Code 201 Created</br>
   Header: ```application/json```</br>
   JSON:
   ```json
   {
     "meeting_id": "1ef0141d-57a2-41d3-b1d2-3ef77290a8d8",
     "name": "Телефонный разговор",
     "audio_format": "mp3",
     "duration": 618.6,
     "speakers_count": 2,
     "file_name": "1ef0141d-57a2-41d3-b1d2-3ef77290a8d8.mp3",
     "date": "2025-06-10T16:03:25.923236",
     "created_at": "2025-06-10T11:03:28.263849"
   }
   ```
   * <b>meeting_id</b> - Уникальный ID совещания в формате uuid (генерируется при создании ресурса).
   * <b>name</b> - Название совещания.
   * <b>audio_format</b> - Формат загруженного аудио файла.
     - <b>mp3</b>
     - <b>ogg</b>
     - <b>pcm</b>
     - <b>fcal</b>
   * <b>duration</b> - Продолжительность аудио записи в секундах.
   * <b>speakers_count</b> - Количество говорящих на записи.
   * <b>file_name</b> - Имя файла в S3 в формате {meeting_id}.{audio_format}.
   * <b>date</b> - Дата проведения совещания.
   * <b>created_at</b> - Дата создания ресурса.

 * ### GET `/{meeting_id}/download`
   Метод для загрузки аудио записи встреч.</br></br>
   
   <b>Request Body</b>:</br>
   Parameters: 
     - <b>meeting_id</b>: "1ef0141d-57a2-41d3-b1d2-3ef77290a8d8" - Строка в формате UUID.</br>
   
   <b>Response Body</b>:</br>
    * <b>Code 200 OK</b></br>
       - Media-type: `"audio/mpeg"`</br>
       - Headers: ```"Content-Disposition": f"attachment; filename={}"```</br>
       - Data: bytes
    * <b>Code 404 Not found</b></br>
       JSON:
       ```json
       {"detail": "Meeting not found"}
       ```

* ### DELETE `/{meetings_id}`
  Метод для удаления совещания.</br></br>
  
  <b>Request Body</b>:</br>
  Parameters: 
    - <b>meeting_id</b>: "1ef0141d-57a2-41d3-b1d2-3ef77290a8d8"</br></br>
  
  <b>Response Body</b>:</br>
  * <b>Code 204 No content</b> - Успешное удаление</br>
  * <b>Code 404 Not found</b>
    JSON:
    ```json
    {"detail":  "Meeting not found"}
    ```

* ### GET `/{meeting_id}`
  Метод для получения метаданных совещания.
  
  <b>Request Body</b>:</br>
  Parameters:
     - <b>meeting_id</b>: "1ef0141d-57a2-41d3-b1d2-3ef77290a8d8" - Уникальный ID совещания получаемый при создании ресурса.
  
  <b>Response body</b>:</br>
  * <b>Code 200 OK</b>
    JSON
     ```json
     {
       "meeting_id": "1ef0141d-57a2-41d3-b1d2-3ef77290a8d8",
       "name": "Телефонный разговор",
       "audio_format": "mp3",
       "duration": 618.6,
       "speakers_count": 2,
       "file_name": "1ef0141d-57a2-41d3-b1d2-3ef77290a8d8.mp3",
       "date": "2025-06-10T16:03:25.923236",
       "created_at": "2025-06-10T11:03:28.263849"
     }
     ```
  * <b>Code 404 Not found</b>
    JSON
    ```json
    {"detail": "Meeting not found"}
    ```
    
 * ### GET `/`
 
    Метод для получения списка всех метаданных совещаний.
    
    <b>Response Body</b>:</br>
     -  <b>Code 200 OK</b></br>
     JSON</br>
     ```json
     [
       {
         "meeting_id": "1ef0141d-57a2-41d3-b1d2-3ef77290a8d8",
         "name": "Телефонный разговор",
         "audio_format": "mp3",
         "duration": 618.6,
         "speakers_count": 2,
         "file_name": "1ef0141d-57a2-41d3-b1d2-3ef77290a8d8.mp3",
         "date": "2025-06-10T16:03:25.923236",
         "created_at": "2025-06-10T11:03:28.263849"
       }
     ]
     ```
      - <b>Code 404 Not found</b></br>
      JSON</br>
      ```json
      {"detail":  "No meetings yet"}
      ```
       

## Tasks

Ресурс для создания и работы с задачами на генерацию протоколов совещаний.

### Базовый url `/api/v1/tasks`

 * ### POST `/`

   Метод для создания задачи на генерацию протокола совещания.</br></br>

   <b>Request Body</b>:</br>
   Headers: ```application/json```</br>
   JSON:
   ```json
   {
     "meeting_id": "1ef0141d-57a2-41d3-b1d2-3ef77290a8d8"
   }
   ```
    
   <b>Response Body</b>:</br>
    - <b>Code 201 Created</b></br>
   Header: ```application/json```</br>
   JSON:
   ```json
   {
      "task_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "meeting_id": "1ef0141d-57a2-41d3-b1d2-3ef77290a8d8",
      "status": "NEW",
      "result_id": null,
      "created_at": "2025-06-09T05:16:38.409Z",
      "updated_at": "2025-06-10T11:07:35.961789"
   }
   ```
   * <b>task_id</b> - Уникальный ID задачи, создаётся при создании ресурса.
   * <b>meeting_id</b> - ID совещания для которого выполняется задача.
   * <b>status</b> - Статус выполнения задачи:
      - <b>NEW</b> - Новая задача. Этот статус можно получить только при создании ресурса.
      - <b>RUNNING</b> - Задача в процессе выполнения.
      - <b>DONE</b> - Задача успешно выполнена. В теле ответа в поле result_id будет ID протокола совещания.
      - <b>ERROR</b> - Задача завершилась с ошибкой.
   * <b>result_id</b> - ID составленного протокола, приходит только когда status DONE.
   * <b>created_at</b> - Дата и время создания задачи.
   * <b>updated_at</b> - Дата обновления статуса задачи.

 * ### GET `/{task_id}`

   Метод для получения статуса задачи.</br></br>
   
   <b>Request Body</b>:</br>
   Parameters: 
     - task_id: "3fa85f64-5717-4562-b3fc-2c963f66afa6"</br></br>
   
   <b>Response Body</b>:</br>
     - <b>Code 200 OK</b></br>
   Header: ```application/json```
   JSON:
   ```json
   {
     "task_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
     "meeting_id": "1ef0141d-57a2-41d3-b1d2-3ef77290a8d8",
     "status": "RUNNING",
     "result_id": null,
     "created_at": "2025-06-09T05:28:30.051Z",
     "updated_at": "2025-06-10T11:07:35.961789"
   }
   ```
     - <b>Code 404 Not found</b>
     ```json
     {"detail": "Task not found"}
     ```

## Results

Ресурс для получения результатов выполненных задач.

### Базовый url `/api/v1/results`

* ### GET `/{results_id}/download`
  Метод для скачивания документа с протоколом совещания.
  
  <b>Request Body</b>:</br>
  Parameters:
    - <b>result_id</b>: "3fa85f64-5717-4562-b3fc-2c963f66afa6"

  <b>Response Body</b>:</br>
     - <b>Code 200 OK</b> - Возвращает .docx файл.</br>
     Media type: `application/vnd.openxmlformats-officedocument.wordprocessingml.document`<br>
     Headers: `"Content-Disposition": f"attachment; filename={filename}"`
     - <b>Code 404 Not found</b></br>
       JSON
       ```json
       {"detail": "Result not found"}
       ```