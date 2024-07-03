#!/bin/env python3

import asyncio
from argparse import ArgumentParser

from httpx import AsyncClient

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

    print(data.model_dump_json(indent=3))


if __name__ == "__main__":
    asyncio.run(main())
