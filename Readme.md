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
   Code: 201</br>
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
    * <b>Code</b>: 200</br>
       - Media-type: `"audio/mpeg"`</br>
       - Headers: ```"Content-Disposition": f"attachment; filename={}"```</br>
       - Data: bytes
    * <b>Code</b>: 404</br>
       - json:
       ```json
       {"detail": "Meeting not found"}
       ```

* ### DELETE `/{meetings_id}`
  Метод для удаления совещания.</br></br>
  
  <b>Request Body</b>:</br>
  Parameters: 
    - <b>meeting_id</b>: "1ef0141d-57a2-41d3-b1d2-3ef77290a8d8"</br></br>
  
  <b>Response Body</b>:</br>
  Code: 204</br>


## Tasks

Ресурс для работы с заданиями на генерацию протокола встречи.

### Базовый url `/api/v1/tasks`

### POST `/`

   Метод для создания задачи.</br></br>

   <b>Request Body</b>:</br>
   Headers: ```application/json```</br>
   JSON:
   ```json
   {
     "meeting_key": "string"
   }
   ```
    
   <b>Response Body</b>:</br>
   Code: 201</br>
   Header: ```application/json```</br>
   JSON:
   ```json
   {
      "task_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "meeting_key": "string",
      "status": "NEW",
      "protocol_key": "string",
      "created_at": "2025-06-09T05:16:38.409Z"
   }
   ```

 * ### GET `/{task_id}`

   Метод для получения статуса задачи.</br></br>
   
   <b>Request Body</b>:</br>
   Parameters: task_id: uuid</br></br>
   
   <b>Response Body</b>:</br>
   Code: 200</br>
   Header: ```application/json```
   JSON:
   ```json
   {
     "task_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
     "meeting_key": "string",
     "status": "RUNNING",
     "protocol_key": "string",
     "created_at": "2025-06-09T05:28:30.051Z"
   }
   ```
