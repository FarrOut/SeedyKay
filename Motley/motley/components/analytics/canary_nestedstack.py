from aws_cdk import (
    # Duration,
    aws_synthetics_alpha as synthetics, aws_lambda as lambda_,
    NestedStack, RemovalPolicy, Duration, )
from aws_cdk.aws_synthetics_alpha import Code, RuntimeFamily
from constructs import Construct


class CanaryNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Relative to project root (The same level as app.py)
        asset_path = "./assets/canaries"

        canary_code = synthetics.Code.from_asset(asset_path=asset_path)

        canary_code = synthetics.Code.from_asset(asset_path=asset_path,
                                                 bundling={
                                                     "image": lambda_.Runtime.PYTHON_3_9.bundling_image,
                                                     "command": ["bash", "-c",
                                                                 f"pip install -r python/canary/requirements.txt -t "
                                                                 f"/asset-output/python/lib/python3.9/site-packages "
                                                                 f"&& cp -r * /asset-output &&ls /asset-output"],
                                                     "user": "root",
                                                 }
                                                 )

        canary = synthetics.Canary(self, "MyCanary",
                                   schedule=synthetics.Schedule.rate(Duration.minutes(5)),
                                   test=synthetics.Test.custom(
                                       code=canary_code,
                                       handler="pageLoadBlueprint.handler",
                                   ),
                                   cleanup=synthetics.Cleanup.LAMBDA,
                                   runtime=synthetics.Runtime(name='syn-python-selenium-2.0',
                                                              family=RuntimeFamily.PYTHON),
                                   )
