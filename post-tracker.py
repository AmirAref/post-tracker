#!/bin/env python3

import asyncio
import os
from argparse import ArgumentParser
from pathlib import Path

import pydymenu
from httpx import AsyncClient

from tracking_post.cli_utils import compat_expanduser
from tracking_post.errors import TrackingNotFoundError
from tracking_post.utils import get_tracking_post

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
    required=False,
    default=None,
)


def read_codes():
    # check file exists
    if CODES_FILE_PATH.exists():
        with open(CODES_FILE_PATH) as file:
            cached_codes = file.read().strip().split("\n")
            return cached_codes
    else:
        raise FileNotFoundError()


def save_new_code(code: str):
    # check file exists
    with open(CODES_FILE_PATH, mode="a+") as file:
        file.write("\n" + code)


async def main():
    # check path is exists
    try:
        CODES_DIR.mkdir()
    except FileExistsError:
        pass
    # get tracking code from args
    args = parser.parse_args()
    tracking_code_arg: str | None = args.code

    # check code is passed or not
    if tracking_code_arg is None:
        # load from file
        # read cached codes and load list of codes
        try:
            list_of_codes = read_codes()
            # check list is not empty
            if not list_of_codes:
                raise FileNotFoundError()
        except FileNotFoundError:
            # send error message
            parser.error(
                "code can not be empry when there is no any cached tracking code !"
            )
        choices = pydymenu.fzf(list_of_codes, prompt="Which tracking code ? ")
        if choices is None:
            return print("exit the program !")
        tracking_code: str = choices[0]
    else:
        # save to file
        tracking_code = tracking_code_arg
        save_new_code(code=tracking_code)

    # get data from api
    async with AsyncClient() as client:
        try:
            data = await get_tracking_post(client=client, tracking_code=tracking_code)
            # output
            print(data.model_dump_json(indent=3))
        except TrackingNotFoundError as e:
            print(e)


if __name__ == "__main__":
    asyncio.run(main())
