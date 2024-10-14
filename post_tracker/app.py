from contextlib import AbstractAsyncContextManager
from typing import Self

import httpx
from user_agent import generate_user_agent

from post_tracker.custom_types import TrackingResult
from post_tracker.logger import get_logger
from post_tracker.utils import get_viewstate, parse_tracking_result

logger = get_logger(name=__name__)


class PostTracker(AbstractAsyncContextManager):
    """
    PostTracker is the main class that will be used get tracking info.

    Example:
        ```python
        import asyncio
        from post_tracker import PostTracker
        from post_tracker.errors import TrackingNotFoundError

        async def main():
            code = "12345"
            async with PostTracker() as tracker_app:
                try:
                    result = await tracker_app.get_tracking_post(tracking_code=code)
                    print(result)
                    # output
                except TrackingNotFoundError as e:
                    return print(e)


        asyncio.run(main())
        ```

    """

    def __init__(self) -> None:
        """initializing the PostTracker application."""

        self._httpx_client = httpx.AsyncClient()

        logger.debug("PostTracker app Initialized !")

    async def __aenter__(self) -> Self:
        logger.debug("async client opened.")
        return self

    async def __aexit__(self, __exc_type, __exc_value, __traceback) -> None:  # noqa: ANN001
        await self.close()

    async def close(self) -> None:
        """
        close the applocation
        """
        # http client
        if not self._httpx_client.is_closed:
            await self._httpx_client.aclose()
        logger.debug("PostTracker application closed.")

    async def get_tracking_post(self, tracking_code: str) -> TrackingResult:
        url = f"https://tracking.post.ir/search.aspx?id={tracking_code}"

        # get view state value
        viewstate, event_validation = await get_viewstate(
            client=self._httpx_client, tracking_code=tracking_code
        )
        # get random user agent
        user_agent = generate_user_agent()

        payload = {
            "scripmanager1": "pnlMain|btnSearch",
            "__LASTFOCUS": "",
            "txtbSearch": tracking_code,
            "txtVoteReason": "",
            "txtVoteTel": "",
            "__EVENTTARGET": "btnSearch",
            "__EVENTARGUMENT": "",
            "__VIEWSTATE": viewstate,
            "__VIEWSTATEGENERATOR": "BBBC20B8",
            "__VIEWSTATEENCRYPTED": "",
            "__EVENTVALIDATION": event_validation,
            "__ASYNCPOST": "true",
            "": "",
        }

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en-US,en;q=0.5",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
            "Host": "tracking.post.ir",
            "Origin": "https://tracking.post.ir",
            "Referer": f"https://tracking.post.ir/search.aspx?id={tracking_code}",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": user_agent,
            "X-MicrosoftAjax": "Delta=true",
            "X-Requested-With": "XMLHttpRequest",
        }

        response = await self._httpx_client.post(
            url,
            data=payload,
            headers=headers,
            follow_redirects=True,
        )

        # parse the content
        content = response.text
        data = parse_tracking_result(content=content)

        return data
