from datetime import datetime
from dataclasses import dataclass
from enum import Enum
import pytz
import json


class LogLevel(Enum):
    Info = 'Info'
    Warn = 'Warn'
    Error = 'Error'


@dataclass
class RequestData:
    resource: str
    path: str
    httpMethod: str
    requestContext: dict
    headers: dict
    multiValueHeaders: dict
    queryStringParameters: dict
    multiValueQueryStringParameters: dict
    pathParameters: dict
    stageVariables: dict
    body: str
    isBase64Encoded: bool


@dataclass
class ResponseData:
    resource: str
    path: str
    httpMethod: str
    requestContext: dict
    headers: dict
    multiValueHeaders: dict
    queryStringParameters: dict
    multiValueQueryStringParameters: dict
    pathParameters: dict
    stageVariables: dict
    body: str
    isBase64Encoded: bool


class LogFormatter:
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
    TIME_ZONE = 'UTC'

    def format_request(self, request: RequestData) -> str:
        if not request:
            return ''

        request_log = ''
        request_log += f", Url: \"{request.url}\"" if request.url else ""
        request_log += f", RequestHeaders: \"{request.headers}\"" if request.headers else ""
        request_log += f", Body: \"{request.body}\"" if request.body else ""

        return request_log

    def format_response(self, response: ResponseData) -> str:
        if not response:
            return ''

        response_log = ''
        response_log += f", Url: \"{response.url}\"" if response.url else ""
        response_log += f", ResponseHeaders: \"{response.headers}\"" if response.headers else ""
        response_log += f", Body: \"{response.body}\"" if response.body else ""
        response_log += f", Status: \"{response.status_code}\"" if response.status_code else ""

        return response_log

    def format_message(self, level: LogLevel, caller: str, message: str, request: RequestData = None,
                       response: ResponseData = None
                       ) -> str:
        try:
            timestamp = datetime.now(pytz.timezone(self.TIME_ZONE)).strftime(self.DATE_FORMAT)
            msg_resp = 'APIResponse' if response else None
            msg_req = 'APIRequest' if request else None
            msg = message or msg_resp or msg_req or ''

            return f"[{timestamp}] Level=\"{level}\", Category=\"AIS.{caller}\"" \
                   f", Message=\"{msg}\"{self.format_request(request)}{self.format_response(response)}"
        except Exception as e:
            raise e

    def format_error(self, level: LogLevel, message: str, caller: str, error: Exception):
        timestamp = datetime.now(pytz.timezone(self.TIME_ZONE)).strftime(self.DATE_FORMAT)
        try:
            return f"[{timestamp}] Level=\"Error\", Category=\"AIS.{caller}\", Message=\"{message}\",'Error':" \
                "{" \
                   f"\"An exception occurred\": {error},"\
                   f"\"Exception arguments\": {error['args'] if error['args'] else ''},"\
                   f"\"Exception cause\": {error['__cause__'] if error['__cause__'] else ''},"\
                   f"\"Exception context\": {error['__context__'] if error['__context__'] else ''},"\
                   f"\"Exception traceback\": {error['__traceback__'] if error['__traceback__'] else ''}"\
                "}"
        except Exception:
            return f"[{timestamp}] Level=\"Error\", Category=\"AIS.{caller}\", Message=\"{message}\"," \
                   f"'Error': {json.dumps(error)}"
