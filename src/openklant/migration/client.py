from io import BytesIO

import requests
import structlog
from djangorestframework_camel_case.parser import CamelCaseJSONParser, ParseError
from djangorestframework_camel_case.render import CamelCaseJSONRenderer

logger = structlog.stdlib.get_logger(__name__)


class Client:
    def _request(
        self,
        method: str,
        url: str,
        data: dict | None = None,
        params: dict | None = None,
        headers: dict | None = None,
    ) -> list | dict | None:
        if headers is None:
            headers = {}

        logger.debug("performing_http_request", method=method, url=url)

        renderer = CamelCaseJSONRenderer()
        _data = renderer.render(data) if data else None

        if method == "POST":
            logger.debug("posting_data", data=_data)
            headers.update({"Content-Type": "application/json"})

        try:
            response = requests.request(
                method, url, data=_data, params=params, headers=headers
            )

            response.raise_for_status()
        except requests.RequestException:
            logger.exception("http_request_failed", method=method, url=url)
            return
        else:
            logger.debug("response_json", data=response.json())
        logger.debug("received_response_data", url=url, content=response.content)

        parser = CamelCaseJSONParser()

        try:
            response_data = parser.parse(
                BytesIO(response.content),
                parser_context=dict(encoding=response.encoding),
            )
        except ParseError:
            logger.exception(
                "unable_to_parse_response_content", content=response.content
            )
            return

        return response_data

    def retrieve(self, url: str, params: dict | None = None) -> list | dict | None:
        return self._request("GET", url, params=params)

    def create(self, url: str, data: dict) -> dict | None:
        return self._request("POST", url, data=data)


class BaseOpenKlantClient(Client):
    token: str
    token_prefix: str
    base_url: str

    headers: dict

    def __init__(self, base_url: str, token: str) -> None:
        self.token = token
        self.base_url = base_url

        self.headers = {"Authorization": f"{self.token_prefix} {self.token}"}

    def retrieve(self, path: str, params: dict | None = None) -> list | dict | None:
        url = self.base_url + path
        return self._request("GET", url, headers=self.headers, params=params)

    def create(self, path: str, data: dict) -> dict | None:
        url = self.base_url + path
        return self._request("POST", url, data=data, headers=self.headers)
