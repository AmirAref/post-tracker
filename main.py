import sys
import json
import asyncio
from httpx import AsyncClient

from tracking_post.utils import get_tracking_post


async def main():
    tracking_code = sys.argv[1]
    async with AsyncClient() as client:
        data = await get_tracking_post(client=client, tracking_code=tracking_code)

    print(json.dumps(data, indent=3, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
