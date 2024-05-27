from aws_synthetics.selenium import synthetics_webdriver as syn_webdriver
from aws_synthetics.common import synthetics_logger as logger
import os, ssl

def main():

    # url = "https://www.gandalfsax.com/"
    # url = 'http://filplumb.uk/'
    url = 'https://i.kym-cdn.com/entries/icons/original/000/000/007/bd6.jpg'

    # Set screenshot option
    takeScreenshot = True

    browser = syn_webdriver.Chrome()
    browser.get(url)

    if takeScreenshot:
        browser.save_screenshot("loaded.png")

    #  Workaround for SSL CERTIFICATE_VERIFY_FAILED
    # https://moreless.medium.com/how-to-fix-python-ssl-certificate-verify-failed-97772d9dd14c
    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
    getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context

    response_code = syn_webdriver.get_http_response(url)
    if not response_code or response_code < 200 or response_code > 299:
        raise Exception("Failed to load page!")
    logger.info("Canary successfully executed")

def handler(event, context):
    # user defined log statements using synthetics_logger
    logger.info("Selenium Python heartbeat canary")
    return main()
