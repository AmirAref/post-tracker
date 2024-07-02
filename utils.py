from httpx import AsyncClient
import asyncio
from bs4 import BeautifulSoup
import bs4
import sys
import json


async def get_viewstate(client: AsyncClient, tracking_code: str) -> tuple[str, str]:
    url = f"https://tracking.post.ir/search.aspx?id={tracking_code}"

    response = await client.get(url)

    # Ensure the request was successful
    if response.status_code != 200:
        raise Exception(f"Failed to load page: {response.status_code}")

    # Parse the __VIEWSTATE value
    soup = BeautifulSoup(response.content, "html.parser")
    viewstate_tag = soup.find("input", {"id": "__VIEWSTATE"})
    validation_tag = soup.find("input", {"id": "__EVENTVALIDATION"})
    if not (isinstance(viewstate_tag, bs4.Tag) and isinstance(validation_tag, bs4.Tag)):
        raise Exception("can't find __VIEWSTATE value in this page.")

    viewstate = viewstate_tag["value"]
    event_validation = validation_tag["value"]

    return viewstate, event_validation  # noqa


async def get_tracking_post(client: AsyncClient, tracking_code: str):
    url = f"https://tracking.post.ir/search.aspx?id={tracking_code}"

    # get view state value
    viewstate, event_validation = await get_viewstate(
        client=client, tracking_code=tracking_code
    )

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

    headers = [
        {"name": "Accept", "value": "*/*"},
        {"name": "Accept-Encoding", "value": "gzip, deflate, br, zstd"},
        {"name": "Accept-Language", "value": "en-US,en;q=0.5"},
        {"name": "Cache-Control", "value": "no-cache"},
        {"name": "Connection", "value": "keep-alive"},
        {
            "name": "Content-Type",
            "value": "application/x-www-form-urlencoded; charset=utf-8",
        },
        {"name": "Host", "value": "tracking.post.ir"},
        {"name": "Origin", "value": "https://tracking.post.ir"},
        {
            "name": "Referer",
            "value": f"https://tracking.post.ir/search.aspx?id={tracking_code}",
        },
        {"name": "Sec-Fetch-Dest", "value": "empty"},
        {"name": "Sec-Fetch-Mode", "value": "cors"},
        {"name": "Sec-Fetch-Site", "value": "same-origin"},
        {
            "name": "User-Agent",
            "value": "Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0",
        },
        {"name": "X-MicrosoftAjax", "value": "Delta=true"},
        {"name": "X-Requested-With", "value": "XMLHttpRequest"},
    ]

    headers = [(h["name"], h["value"]) for h in headers]

    response = await client.post(
        url,
        data=payload,
        headers=headers,
        follow_redirects=True,
    )

    content = response.text
    data = parse_tracking_result(content=content)

    return data


def parse_tracking_result(content: str):
    soup = BeautifulSoup(content, "html.parser")
    rows = soup.find_all("div", {"class": "row"})
    all_items = []
    for row in rows:
        row_items = row.select(".newtddata, .newtdheader")
        # row_items = row.find_all("div", {"class": "newtddata"})
        if row_items:
            row_items = [item.text for item in row_items]
            all_items.append(row_items)
    return all_items


async def main():
    tracking_code = sys.argv[1]
    async with AsyncClient() as client:
        data = await get_tracking_post(client=client, tracking_code=tracking_code)

    print(json.dumps(data, indent=3, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
