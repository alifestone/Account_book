import aiofiles
import json
import os

DB_PATH = 'data.json'

async def read_data():
    if not os.path.exists(DB_PATH):
        return {}
    async with aiofiles.open(DB_PATH, 'r', encoding='utf-8') as f:
        content = await f.read()
        if not content:
            return {}
        return json.loads(content)

async def write_data(data):
    async with aiofiles.open(DB_PATH, 'w', encoding='utf-8') as f:
        await f.write(json.dumps(data, ensure_ascii=False, indent=2))
