class ApiError(Exception):
    pass


class ApiTimeOut(ApiError):
    pass


class ApiNotFoundError(ApiError):
    pass


class ApiInvalidAuth(ApiError):
    pass


class ApiPayloadError(ApiError):
    pass
