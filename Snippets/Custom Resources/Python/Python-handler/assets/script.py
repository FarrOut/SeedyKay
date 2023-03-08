import json
import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def handler(event, context):
    try:
        logger.debug('Event:{}\n', event)
        response_data = {}
        if event['RequestType'] == 'Delete':
            logger.info('Delete request received.')
            logger.debug('Sending SUCCESS signal for delete request...')
            # cfnresponse.send(event, context, cfnresponse.SUCCESS, response_data)
            response = {'Data': response_data, 'isComplete': 'true'}
            logger.debug('Sending SUCCESS response.\n{}', response)
            return response

        response_data['Message'] = 'Hello World'
        response = {'Data': response_data, 'isComplete': 'true'}
        logger.debug('Sending SUCCESS response.\n{}', response)
        return response
        # cfnresponse.send(event, context, cfnresponse.SUCCESS, response_data)
    except Exception as e:
        logger.error(e, exc_info=True)
        response_data = {'Reason': e}
        # cfnresponse.send(event, context, cfnresponse.FAILED, response_data)

# TODO
# def is_complete(event, context):
#     try:
#         logger.debug('Checking if complete\n', event)
#
#     except Exception as e:
#         logger.error(e, exc_info=True)