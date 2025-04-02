class SendMessage:
    def __init__(self, sdk, logger):
        self.yhToken = sdk.MessageBase.yhToken
        self.apiUrl = (
            "https://chat-go.jwzhd.com/open-apis/v1/bot/send?token=" + self.yhToken
        )
        self.NetJsonPost = sdk.MessageBase.NetJsonPost
        self.NetFileUpload = sdk.MessageBase.NetFileUpload

    def _gen_body(
        self,
        recvId: str,
        recvType: str,
        contentType: str,
        content: dict[str, any],
        parentId: str,
    ) -> dict[str, any]:
        return {
            "recvId": recvId,
            "recvType": recvType,
            "contentType": contentType,
            "content": content,
            "parentId": parentId,
        }

    def Text(
        self,
        recvId: str,
        recvType: str,
        content: str,
        buttons: list[list[dict[str, any]]] = [],
        parentId: str = "",
    ) -> dict[str, any]:
        return self.NetJsonPost(
            self.apiUrl,
            self._gen_body(
                recvId,
                recvType,
                "text",
                {"text": content, "buttons": buttons},
                parentId,
            ),
        )

    def Markdown(
        self,
        recvId: str,
        recvType: str,
        content: str,
        buttons: list[list[dict[str, any]]] = [],
        parentId: str = "",
    ) -> dict[str, any]:
        return self.NetJsonPost(
            self.apiUrl,
            self._gen_body(
                recvId,
                recvType,
                "markdown",
                {"text": content, "buttons": buttons},
                parentId,
            ),
        )

    def Html(
        self,
        recvId: str,
        recvType: str,
        content: str,
        buttons: list[list[dict[str, any]]] = [],
        parentId: str = "",
    ) -> dict[str, any]:
        return self.NetJsonPost(
            self.apiUrl,
            self._gen_body(
                recvId,
                recvType,
                "html",
                {"text": content, "buttons": buttons},
                parentId,
            ),
        )

    def Image(
        self,
        recvId: str,
        recvType: str,
        content: bytes,
        buttons: list[list[dict[str, any]]] = [],
        parentId: str = "",
    ) -> dict[str, any]:
        return self.NetJsonPost(
            self.apiUrl,
            self._gen_body(
                recvId,
                recvType,
                "image",
                {
                    "imageKey": self.NetFileUpload(
                        "https://chat-go.jwzhd.com/open-apis/v1/image/upload?token="
                        + self.yhToken,
                        "image",
                        content,
                    )["data"]["imageKey"],
                    "buttons": buttons,
                },
                parentId,
            ),
        )

    def Video(
        self,
        recvId: str,
        recvType: str,
        content: bytes,
        buttons: list[list[dict[str, any]]] = [],
        parentId: str = "",
    ) -> dict[str, any]:
        return self.NetJsonPost(
            self.apiUrl,
            self._gen_body(
                recvId,
                recvType,
                "video",
                {
                    "videoKey": self.NetFileUpload(
                        "https://chat-go.jwzhd.com/open-apis/v1/video/upload?token="
                        + self.yhToken,
                        "video",
                        content,
                    )["data"]["videoKey"],
                    "buttons": buttons,
                },
                parentId,
            ),
        )

    def File(
        self,
        recvId: str,
        recvType: str,
        content: bytes,
        buttons: list[list[dict[str, any]]] = [],
        parentId: str = "",
    ) -> dict[str, any]:
        return self.NetJsonPost(
            self.apiUrl,
            self._gen_body(
                recvId,
                recvType,
                "file",
                {
                    "fileKey": self.NetFileUpload(
                        "https://chat-go.jwzhd.com/open-apis/v1/file/upload?token="
                        + self.yhToken,
                        "file",
                        content,
                    )["data"]["fileKey"],
                    "buttons": buttons,
                },
                parentId,
            ),
        )
