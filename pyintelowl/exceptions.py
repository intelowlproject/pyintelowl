import json
import typing

from requests.exceptions import RequestException


class IntelOwlClientException(RequestException):
    @property
    def error_detail(self) -> typing.Union[typing.Dict, typing.AnyStr]:
        content = None
        try:
            content = self.response.json()
            detail = content.get("detail", None)
            if detail:
                content = detail
        except json.JSONDecodeError:
            content = self.response.content
        except Exception:
            pass

        return content

    def __str__(self):
        err_msg = super().__str__()
        detail = self.error_detail
        return err_msg + f". Details: {detail}"
