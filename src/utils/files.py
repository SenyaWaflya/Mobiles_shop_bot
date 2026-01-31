from aiogram.types import BufferedInputFile


async def file_bytes_to_photo(file_bytes: bytes, title: str) -> BufferedInputFile:
    photo = BufferedInputFile(
        file=file_bytes,
        filename=f'{title}.jpg',
    )
    return photo
