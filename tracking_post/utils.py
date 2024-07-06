import bs4
from bs4 import BeautifulSoup
from httpx import AsyncClient
from user_agent import generate_user_agent

from tracking_post.errors import TrackingNotFoundError
from tracking_post.schemas import HourMinute, ShipmentStatus, TrackingResult


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


def parse_tracking_result(content: str) -> TrackingResult:
    soup = BeautifulSoup(content, "html.parser")
    data = TrackingResult()

    # get tracking data
    tracking_info = soup.find(attrs={"id": "pnlResult"})
    if not (tracking_info, bs4.Tag):
        raise ValueError("can't find traking info element.")
    # get all rows
    rows = tracking_info.find_all("div", {"class": "row"})
    shipment_date = None
    # get items of each row
    for row in rows:
        # get the date from header
        shipment_date_tag = row.select_one(".newtdheader")
        if shipment_date_tag:
            shipment_date = str(shipment_date_tag.text.strip())
            continue

        # get shipment status
        row_items = row.select(".newtddata")
        # check is not empty
        if row_items:
            row_items = [item.text for item in row_items]
            # create object
            shipment_time = row_items[3].strip().split(":")
            shipment_status = ShipmentStatus(
                index=row_items[0],
                status=row_items[1],
                location=row_items[2],
                time=HourMinute(hour=shipment_time[0], minute=shipment_time[1]),
                date=shipment_date,
            )
            data.tracking_list.append(shipment_status)

    # get parcel info
    parcel_info = soup.find(attrs={"id": "pParcelInfo"})
    if not isinstance(parcel_info, bs4.Tag):
        raise TrackingNotFoundError()
    # get all rows
    parcel_info_rows = parcel_info.find_all("div", {"class": "newrowdatacol"})
    # get items of each row
    for row in parcel_info_rows:
        row_headers = row.select(".newcolheader")
        row_values = row.select(".newcoldata")

        # check is not empty
        for row_header, row_value in zip(row_headers, row_values):
            row_header = row_header.text
            row_value = row_value.text
            data.parcel_info.append(
                {
                    "key": row_header,
                    "value": row_value,
                }
            )

    # reverse order of tacking
    data.tracking_list.reverse()

    return data
