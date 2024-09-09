class TrackingNotFoundError(Exception):
    def __init__(self, tracking_code: str | None = None) -> None:
        if tracking_code is None:
            error_message = "tracking information not found!"
        else:
            error_message = (
                f"tracking information for tracking code : {tracking_code} not found!"
            )
        super().__init__(error_message)
