import asyncio

from post_tracker.main import main as main_async


def main() -> None:
    asyncio.run(main_async())
