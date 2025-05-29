import os
import asyncio
from uuid import UUID
from pprint import pprint
from dotenv import load_dotenv

from src.dio_meetings.infrastructure.ai.salute_speech.api import SaluteSpeechAPI


load_dotenv(".env")


async def main() -> None:
    # response_file_id = "d8aee9ca-88e8-40a7-9da6-d8d3145f9cd6"
    file_path = "847y7aiqteg40hi6gu7ok7t7lrolqprb.mp3"
    salute_speech_api = SaluteSpeechAPI(api_key=os.getenv("SALUTE_SPEECH_API_KEY"))
    '''request_file_id = await salute_speech_api.upload_file(file_path)
    task_result = await salute_speech_api.async_recognize(
        request_file_id=request_file_id,
        file_extension="mp3"
    )
    print(task_result)
    while task_result.status != "DONE":
        await asyncio.sleep(1)
        task_result = await salute_speech_api.get_task_status(task_result.id)
        if task_result.status == "DONE":
            res = await salute_speech_api.download_file(task_result.response_file_id)
            print(res)'''
    res = await salute_speech_api.download_file(UUID("982c1d33-3bda-4281-a896-2e6bf8d63096"))
    print(res)
    text = "\n\n".join(res)
    print(text)


if __name__ == "__main__":
    asyncio.run(main())
