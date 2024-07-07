import asyncio

from post_tracker.main import main as main_async


def main():
    asyncio.run(main_async())
