from splunk_hec_logger.logs_handler import SplunkHecHandler

def handler(event, context):   
    print("Initializing SplunkHecHandler...")

    splunk_handler = SplunkHecHandler(
        host='splunkfw.domain.tld',
        token='EA33046C-6FEC-4DC0-AC66-4326E58B54C3',
        port=8888,
        proto='https',
        ssl_verify=True,
        source="HEC_example"
    )

    splunk_handler.info("Hello Splunk!")
