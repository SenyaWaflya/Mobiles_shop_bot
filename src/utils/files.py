from pathlib import Path

from aiogram.types import BufferedInputFile, FSInputFile


async def file_bytes_to_photo(file_bytes: bytes, title: str) -> BufferedInputFile:
    photo = BufferedInputFile(
        file=file_bytes,
        filename=f'{title}.jpg',
    )
    return photo


async def get_static_photo(filename: str) -> FSInputFile:
    src_dir = Path(__file__).parent.parent
    photo = FSInputFile(Path(f'{src_dir}/static/{filename}'))
    return photo
