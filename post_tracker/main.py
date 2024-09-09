#!/bin/env python3

import asyncio
import os
from argparse import ArgumentParser
from pathlib import Path

# import pydymenu
from httpx import AsyncClient
from rich.console import Console
from rich.table import Table

from post_tracker.cli_utils import compat_expanduser
from post_tracker.errors import TrackingNotFoundError
from post_tracker.utils import get_tracking_post

XDG_CONFIG_HOME = os.getenv("XDG_CONFIG_HOME") or compat_expanduser("~/.config")
CODES_DIR = Path(XDG_CONFIG_HOME, "post-tracker")
CODES_FILE_PATH = Path(CODES_DIR, "tracking_codes.txt")

parser = ArgumentParser(
    prog="post-tracker",
    description="a command line tool to get tracking information from tracking.post.ir",
)
parser.add_argument(
    "-c",
    "--code",
    help="tracking code to get data from tracking.post.ir",
    required=True,
    # default=None,
)


def read_codes() -> list[str]:
    # check file exists
    if CODES_FILE_PATH.exists():
        with open(CODES_FILE_PATH) as file:
            cached_codes = file.read().strip().split("\n")
            return cached_codes
    else:
        raise FileNotFoundError()


def save_new_code(code: str) -> None:
    # check file exists
    try:
        codes = read_codes()
    except FileNotFoundError:
        codes = []
    # check not duplicate codes
    if code not in codes:
        codes.append(code)
        with open(CODES_FILE_PATH, mode="w") as file:
            file.write("\n".join(codes))


async def main() -> None:
    # check path is exists
    try:
        CODES_DIR.mkdir()
    except FileExistsError:
        pass
    # get tracking code from args
    args = parser.parse_args()
    tracking_code: str = args.code

    # TODO: remove pydemnu fzf temporarily to find a better library/approach
    # check code is passed or not
    # if tracking_code_arg is None:
    #     # load from file
    #     # read cached codes and load list of codes
    #     try:
    #         list_of_codes = read_codes()
    #         # check list is not empty
    #         if not list_of_codes:
    #             raise FileNotFoundError()
    #     except FileNotFoundError:
    #         # send error message
    #         parser.error(
    #             "code can not be empty when there is no any cached tracking code !"
    #         )
    #     choices = pydymenu.fzf(list_of_codes, prompt="Which tracking code ? ")
    #     if choices is None:
    #         return print("exit the program !")
    #     tracking_code: str = choices[0]
    # else:
    #     # save to file
    #     tracking_code = tracking_code_arg
    #     save_new_code(code=tracking_code)

    # get data from api
    table = Table(title="وضعیت مرسوله پستی", show_lines=True, header_style="white bold")
    table.add_column("وضعیت", justify="right", style="sea_green3")
    table.add_column("مکان / منطقه", justify="right", style="cyan1")
    table.add_column("زمان", justify="center", style="spring_green2")
    table.add_column("تاریخ", justify="right", style="spring_green2")
    table.add_column("ردیف", justify="center", style="white bold")
    async with AsyncClient() as client:
        try:
            data = await get_tracking_post(client=client, tracking_code=tracking_code)
            # output
        except TrackingNotFoundError as e:
            return print(e)

    for row in data.tracking_list:
        table.add_row(
            row.status,
            row.location,
            str(row.time),
            row.date,
            str(row.index),
        )
    console = Console()
    console.print(table)


if __name__ == "__main__":
    asyncio.run(main())
