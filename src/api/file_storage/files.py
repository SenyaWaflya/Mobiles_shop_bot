from httpx import AsyncClient

from src.settings import settings


class FilesApi:
    @staticmethod
    async def get(file_path: str) -> bytes:
        async with AsyncClient() as client:
            resp = await client.get(f'{settings.FILE_STORAGE_API_URL}/files/{file_path}')
            resp.raise_for_status()
            file_bytes = resp.content
            return file_bytes
