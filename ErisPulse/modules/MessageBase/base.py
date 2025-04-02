import io
import mimetypes
import requests
import filetype


class MessageBase:
    def __init__(self, sdk, logger) -> None:
        self.yhToken = sdk.env.YUNHU_TOKEN

    def NetJsonGet(self, url) -> dict[str, any]:
        return requests.get(url=url).json()

    def NetJsonPost(self, url, data) -> dict[str, any]:
        return requests.post(
            url=url, headers={"Content-Type": "application/json"}, json=data
        ).json()

    def NetFileUpload(self, url, field_name, file_bytes) -> dict[str, any]:
        file_name = "file.{}".format(filetype.guess(file_bytes).extension)
        return requests.post(
            url=url,
            files=[
                (
                    field_name,
                    (
                        file_name,
                        io.BufferedReader(io.BytesIO(file_bytes)),
                        mimetypes.guess_type(file_name),
                    ),
                )
            ],
        ).json()
