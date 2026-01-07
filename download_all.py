import os
import yadisk
import aiofiles
import asyncio
from config import app_config
import constants


async def main():
    async def get_count_files(client: yadisk.AsyncClient, path: str) -> int:
        file_count = 0
        async for i in client.listdir(path):
            if i.type == "file":
                file_count += 1
        return file_count

    def clean_name(name: str) -> str:
        return "".join(c for c in name if c not in r'\/:*?"<>|')

    async def download_files(client: yadisk.AsyncClient, yadisk_path: str, local_path: str):
        print(f"Загрузка файлов из {yadisk_path}...")
        os.makedirs(local_path, exist_ok=True)
        count_files = await get_count_files(client, yadisk_path)
        count = 0
        async for i in client.listdir(yadisk_path):
            safe_name = clean_name(i.name)
            if i.type == "file":
                count += 1
                local_file = os.path.join(local_path, safe_name)
                async with aiofiles.open(local_file, "wb") as f:
                    await client.download(i.path, f)
                    print(f"Загружен файл '{safe_name}' ({count} из {count_files})")
            elif i.type == "dir":
                new_local_path = os.path.join(local_path, safe_name)
                await download_files(client, i.path, new_local_path)

    print("Подключение...")
    try:
        client = yadisk.AsyncClient(token=app_config.YADISK_KEY.get_secret_value())
    except Exception as e:
        print("Ошибка подключения:", e)
        return
    print("Подключение успешно")
    # total_count = 0
    async with client:
        await download_files(client, constants.MAIN_YADISK_PATH, constants.MAIN_LOCAL_PATH)

    print("Загрузка завершена")
    # print(f"Файлов загружено: {total_count}, размер загруженных файлов: {total_mb}" МБ)


asyncio.run(main())
