import boto3
import logging
import cfnresponse

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

lambda_ = boto3.client('lambda')

def handler(event, context) -> str:
  layer_name = str(event['ResourceProperties']['LayerName'])

  try:
    latest_version_arn = get_latest_layer_version(layer_name)

    responseData = {}
    responseData['Data'] = latest_version_arn
    cfnresponse.send(event, context, cfnresponse.SUCCESS, responseData, "LatestLayerVersionArn")
  except Exception:
    logger.exception('Signaling failure to CloudFormation.')
    cfnresponse.send(event, context, cfnresponse.FAILED, {})

def get_latest_layer_version(layer_name) -> str:
    logger.info('Fetching layer versions of function: {}'.format(layer_name))

    response = lambda_.list_layer_versions(
    LayerName=layer_name,
    MaxItems=3,
    )

    versions = response['LayerVersions']
    logger.debug('Found {} layer versions'.format(len(versions)))
    first_version = versions[0]

    latest_version_arn = first_version['LayerVersionArn']
    logger.info('Latest layer version found: {}'.format(latest_version_arn))

    return latest_version_arn
