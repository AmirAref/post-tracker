#!/bin/env python3

import asyncio
import os
from argparse import ArgumentParser
from pathlib import Path

from rich.console import Console
from rich.table import Table

from post_tracker import PostTracker
from post_tracker.cli_utils import compat_expanduser
from post_tracker.errors import TrackingNotFoundError

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
    # get tracking code from args
    args = parser.parse_args()
    tracking_code: str = args.code

    # TODO: remove pydemnu fzf temporarily to find a better library/approach
    # get data from api
    table = Table(title="وضعیت مرسوله پستی", show_lines=True, header_style="white bold")
    table.add_column("وضعیت", justify="right", style="sea_green3")
    table.add_column("مکان / منطقه", justify="right", style="cyan1")
    table.add_column("زمان", justify="center", style="spring_green2")
    table.add_column("تاریخ", justify="right", style="spring_green2")
    table.add_column("ردیف", justify="center", style="white bold")
    async with PostTracker() as tracker_app:
        try:
            data = await tracker_app.get_tracking_post(tracking_code=tracking_code)
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
