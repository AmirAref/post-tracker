from httpx import AsyncClient
from bs4 import BeautifulSoup
import bs4


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
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:127.0) Gecko/20100101 Firefox/127.0",
        "X-MicrosoftAjax": "Delta=true",
        "X-Requested-With": "XMLHttpRequest",
    }

    response = await client.post(
        url,
        data=payload,
        headers=headers,
        follow_redirects=True,
    )

    # parse the content
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
