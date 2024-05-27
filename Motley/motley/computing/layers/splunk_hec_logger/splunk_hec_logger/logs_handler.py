import json
import logging
import urllib3

from .log_formatter import LogFormatter
logFormatter = LogFormatter()


class SplunkHecHandler(logging.Handler):
    """
    A logging handler for sending log records to a Splunk HTTP Event Collector (HEC) listener.

    Attributes:
        - host: The hostname of the Splunk HTTP Event Collector.
        - token: The token provided by Splunk HEC for authentication.
        - port: The port number to use for the connection (default is 8888).
        - proto: The protocol to use for the connection (default is 'https').
        - ssl_verify: Whether to verify SSL certificates (default is True).
        - source: The source identifier for log records (default is 'HEC_example').

    Example Usage:
        splunk_handler = SplunkHecHandler(
            host='splunkfw.domain.tld',
            token='EA33046C-6FEC-4DC0-AC66-4326E58B54C3',
            port=8888,
            proto='https',
            ssl_verify=True,
            source="HEC_example"
        )
        logger.log("Testing Splunk HEC Info message")
    """

    URL_PATTERN = "{0}://{1}:{2}/services/collector/{3}"

    def __init__(self, host, token, **kwargs):
        """
        Init Python logging handler for sending logs to a Splunk server.

        :param host: Splunk server hostname or IP.
        :type host: str
        :param token: Splunk HTTP Event Collector (HEC) Token.
        :type token: str

        :Keyword Arguments:
            - port (int): Port number of Splunk HEC listener (0-65535).
            - proto (str): Protocol to use for the connection (http | https).
            - ssl_verify (bool | str): Whether to verify SSL certificates (True | False | <Path to cert>).
                True by default. See https://2.python-requests.org/en/master/user/advanced/#ssl-cert-verification
            - source (str): Override source value specified in Splunk HEC configuration. None by default.
            - sourcetype (str): Override sourcetype value specified in Splunk HEC configuration. None by default.
            - endpoint (str): Endpoint type (raw | event). Use 'raw' to skip field extractions.
                See http://docs.splunk.com/Documentation/Splunk/latest/RESTREF/RESTinput#services.2Fcollector.2Fraw
        """
        self.host = host
        self.token = token
        self.headers = dict()
        if kwargs is not None:
            self.port = int(kwargs.get("port", 8080))
            self.proto = kwargs.get("proto", "https")
            self.ssl_verify = (
                False
                if (kwargs.get("ssl_verify") in ["0", 0, "false", "False", False])
                else kwargs.get("ssl_verify") or True
            )
            self.source = kwargs.get("source")
            self.index = kwargs.get("index")
            self.sourcetype = kwargs.get("sourcetype", "")
            self.hostname = kwargs.get("hostname", 'aws')
            self.endpoint = kwargs.get("endpoint", "event")
            self.caller = kwargs.get("caller", "Unnamed")

        try:
            self.headers["Authorization"] = "Splunk {}".format(self.token)
            logging.Handler.__init__(self)
        except Exception as err:
            print('ERROR: ', err)
            logging.debug(
                "Failed to connect to remote Splunk server (%s:%s). Exception: %s"
                % (self.host, self.port, err)
            )
            raise err
        else:
            self.url = self.URL_PATTERN.format(
                self.proto, self.host, self.port, self.endpoint
            )

    def __log(self, record):
        """
        Send log record to Splunk HEC listener:

        :param record: The log message or dictionary to parse.
        :type record: str or object

        'record' dictionary could contain:
        :param request: Optional data related to the incoming request.
        :type request: RequestData, optional
        :param response: Optional data related to the outgoing response.
        :type response: ResponseData, optional\n
        """
        body = record

        try:
            if record.__class__ == dict and record['level'] == 'Error':
                body = logFormatter.format_error(**record, caller=self.caller)
            if record.__class__ == dict:
                body = logFormatter.format_message(**record, caller=self.caller)
        except Exception as err:
            logging.debug("Log record emit exception raised. Exception: %s " % err)

        event = dict({"host": self.hostname, "event": body, "fields": {}})

        # Splunk 7.x does not like empty fields
        if self.source is not None:
            event["source"] = self.source

        if self.sourcetype is not None:
            event["sourcetype"] = self.sourcetype

        if self.index is not None:
            event["index"] = self.index

        try:
            http = urllib3.PoolManager(timeout=20)
            http.request(
                'POST',
                url=self.url,
                body=json.dumps(event),
                headers=self.headers
            )
        except Exception as err:
            print(err)
            logging.debug(
                "Failed to emit record to Splunk server (%s:%s).  Exception raised: %s"
                % (self.host, self.port, err)
            )
            raise err

    def info(self, messageOrObj):
        """
        'messageOrObj' Represents a log entry with the specified details:

        :param messageOrObj: The log message or dictionary to parse.
        :type messageOrObj: str or object

        'messageOrObj' dictionary could contain:
        :param request: Optional data related to the incoming request.
        :type request: RequestData, optional
        :param response: Optional data related to the outgoing response.
        :type response: ResponseData, optional\n
        """
        self.__log({'message': messageOrObj, 'level': 'Info'})

    def warn(self, messageOrObj: str):
        """
        'messageOrObj' Represents a log entry with the specified details:

        :param messageOrObj: The log message or dictionary to parse.
        :type messageOrObj: str or object

        'messageOrObj' dictionary could contain:
        :param request: Optional data related to the incoming request.
        :type request: RequestData, optional
        :param response: Optional data related to the outgoing response.
        :type response: ResponseData, optional\n
        """
        self.__log({'message': messageOrObj, 'level': 'Warn'})

    def error(self, messageOrObj: str, error: Exception = ""):
        """
        'messageOrObj' Represents a log entry with the specified details:

        :param messageOrObj: The log message or dictionary to parse.
        :type messageOrObj: str or object
        :param error: Optional data related to the incoming Exception.
        :type error: Exception, optional

        'messageOrObj' dictionary could contain:
        :param request: Optional data related to the incoming request.
        :type request: RequestData, optional
        :param response: Optional data related to the outgoing response.
        :type response: ResponseData, optional\n
        """
        error_dict = ''
        if (error.__class__ == dict):
            try:
                error_dict = {
                    "An exception occurred": error,
                    "Exception arguments": error['args'] if error['args'] else "",
                    "Exception cause": error['__cause__'] if error['__cause__'] else "",
                    "Exception context": error['__context__'] if error['__context__'] else "",
                    "Exception traceback": error['__traceback__'] if error['__traceback__'] else "",
                }
            except Exception:
                error_dict = error.__dict__
        self.__log({'message': messageOrObj, 'level': 'Error', 'error': error_dict})
