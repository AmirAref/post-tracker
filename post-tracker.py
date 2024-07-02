#!/bin/python3

import json
import asyncio
from httpx import AsyncClient
from argparse import ArgumentParser

from tracking_post.utils import get_tracking_post


parser = ArgumentParser(
    prog="post-tracker",
    description="a command line tool to get tracking information from tracking.post.ir",
)
parser.add_argument(
    "code",
    help="tracking code to get data from tracking.post.ir",
)


async def main():
    # get tracking code from args
    args = parser.parse_args()
    tracking_code: str = args.code

    # get data from api
    async with AsyncClient() as client:
        data = await get_tracking_post(client=client, tracking_code=tracking_code)

    print(json.dumps(data, indent=3, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
