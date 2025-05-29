import asyncio

from src.dio_meetings.infrastructure.speech.salut_speech.api import SberDevicesAPI


async def main() -> None:
    salut_devices_api = SberDevicesAPI(api_key="<>")
    access_token = await salut_devices_api._authorize()
    print(access_token)


if __name__ == "__main__":
    asyncio.run(main())
