import yadisk
import aiofiles
import asyncio
from config import app_config


async def main():
    client = yadisk.AsyncClient(token=app_config.YADISK_KEY.get_secret_value())

    async def get_count_files(client, path):
        file_count = 0
        async for i in client.listdir(path):
            if i.type == "file":
                file_count += 1
        return file_count

    async with client:
        yadisk_dir = "/Фотокамера"
        host_dir = "downloaded"
        count_files = await get_count_files(client, yadisk_dir)
        count = 0
        async for i in client.listdir(yadisk_dir):
            if i.type == "file":
                count += 1
                local_path = f"{host_dir}/{i.name}"
                async with aiofiles.open(local_path, "wb") as f:
                    await client.download(i.path, f)
                print(f"Загружен файл '{i.name}' ({count} из {count_files})")

    print("Загрузка завершена")


asyncio.run(main())
