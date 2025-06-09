# Сервис для создания протокола совещания

## REST API

## Meetings

Ресурс для работы с аудио записями встреч / совещаний.

### Базовый url `/api/v1/meetings`

 * ### POST `/upload`
  
   Метод для загрузки аудио записи встречи.</br></br>

   <b>Request body</b>:</br>
   Headers: ```multipart/form-data```</br>
   Data: bytes</br></br>

   <b>Response body</b>:</br>
   Code: 201</br>
   Header: ```application/json```</br>
   JSON:
   ```json
   {
     "meeting_key": "string",
     "created_at": "2025-06-09T04:47:31.863Z"
   }
   ```

 * ### GET `/{meeting_key}/download`
   Метод для загрузки аудио записи встреч.</br></br>
   
   <b>Request Body</b>:</br>
   Parameters: meeting_key: "string"</br></br>

   <b>Response Body</b>:</br>
   Code: 200</br>
   Header: ```"Content-Disposition": f"attachment; filename={meeting_key}"```</br>
   Data: bytes

* ### DELETE `/{meetings_key}`
  Метод для удаления аудио записи совещания.</br></br>
  
  <b>Request Body</b>:</br>
  Parameters: meeting_key: "string"</br></br>
  
  <b>Response Body</b>:</br>
  Code: 204</br>
