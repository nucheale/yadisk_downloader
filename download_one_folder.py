import os
import yadisk
import aiofiles
import asyncio

import constants
from config import app_config


async def main():
    async def get_count_files(client: yadisk.AsyncClient, path: str) -> int:
        file_count = 0
        async for i in client.listdir(path):
            if i.type == "file":
                file_count += 1
        return file_count

    print("Подключение...")
    try:
        client = yadisk.AsyncClient(token=app_config.YADISK_KEY.get_secret_value())
    except Exception as e:
        print("Ошибка подключения:", e)
        return
    print("Подключение успешно")
    async with client:
        yadisk_path = constants.ONE_FOLDER_YADISK_PATH
        local_path = os.path.join(constants.MAIN_LOCAL_PATH, yadisk_path)
        count_files = await get_count_files(client, yadisk_path)
        count = 0
        os.makedirs(local_path, exist_ok=True)
        async for i in client.listdir(yadisk_path):
            if i.type == "file":
                count += 1
                local_file = os.path.join(local_path, i.name)
                async with aiofiles.open(local_file, "wb") as f:
                    await client.download(i.path, f)
                print(f"Загружен файл '{i.name}' ({count} из {count_files})")

    print("Загрузка завершена")


asyncio.run(main())
