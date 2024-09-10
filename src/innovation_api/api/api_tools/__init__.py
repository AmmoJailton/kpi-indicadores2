from fastapi import Response

from innovation_api.api.api_tools.exceptions import (
    ApiError,
    ApiInvalidAuth,
    ApiNotFoundError,
    ApiPayloadError,
    ApiTimeOut,
)


class ApiTools:
    def __init__(self) -> None:
        pass

    @staticmethod
    def check_error(response: Response, method: str) -> bool:
        if response.status_code == 404:
            raise ApiNotFoundError(f"ApiNotFoundError | method: {method} | statusCode: {response.status_code}")
        if response.status_code == 403:
            raise ApiInvalidAuth(f"ApiInvalidAuth | method: {method} | statusCode: {response.status_code}")
        if response.status_code == 400:
            raise ApiPayloadError(f"ApiPayloadError | method: {method} | statusCode: {response.status_code}")
        if response.status_code == 504:
            raise ApiTimeOut(f"ApiTimeOut | method: {method} | statusCode: {response.status_code}")
        if response.status_code < 200 or (299 < response.status_code < 600):
            raise ApiError(f"ApiError | method: {method} | statusCode: {response.status_code}")
        return True
