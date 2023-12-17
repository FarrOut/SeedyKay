from aws_cdk import (
    # Duration,
    Stack, RemovalPolicy,
)
from constructs import Construct
from motley.components.machine_learning.sage_maker.sagemaker_domain_nestedstack import SageMakerDomainNestedStack
from motley.components.machine_learning.sage_maker.sagemaker_single_model_nestedstack import \
    SageMakerSingleModelNestedStack


class MachineLearningStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # sage_maker = SageMakerSingleModelNestedStack(self, "SageMakerSingleModelNestedStack",
        #                                              repo_name='tensorflow-training',
        #                                              image_tag='2.13.0-cpu-py310-ubuntu20.04-ec2',
        #                                              account_id='',
        #                                              removal_policy=removal_policy,
        #                                              )

        sage_maker = SageMakerDomainNestedStack(self, 'SageMakerDomainNestedStack',
                                                removal_policy=removal_policy,
                                                )
