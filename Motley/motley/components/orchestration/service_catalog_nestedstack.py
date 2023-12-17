from aws_cdk import CfnOutput, NestedStack, RemovalPolicy, RemovalPolicyOptions, Tags
from aws_cdk import aws_ec2 as ec2  # Duration,
from aws_cdk import aws_eks as eks
from aws_cdk import aws_servicecatalog as servicecatalog
from aws_cdk.aws_eks import (ClusterLoggingTypes, KubernetesVersion,
                             LaunchTemplateSpec)
from aws_cdk.aws_iam import (AccountPrincipal, ManagedPolicy, PolicyDocument, AccountRootPrincipal,
                             PolicyStatement, Role, ServicePrincipal)
from aws_cdk.lambda_layer_kubectl_v24 import KubectlV24Layer
from constructs import Construct

from aws_cdk import aws_s3 as s3

from motley.components.machine_learning.sage_maker.sagemaker_domain_nestedstack import SageMakerDomainNestedStack


class SageMakerProduct(servicecatalog.ProductStack):
    def __init__(self, scope, id, *, asset_bucket: s3.IBucket = None,):
        super().__init__(scope, id, asset_bucket=asset_bucket,)

        SageMakerDomainNestedStack(self, 'SageMakerDomainNestedStack',
                                   removal_policy=RemovalPolicy.DESTROY,
                                   )


class ServiceCatalogNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,  asset_bucket: s3.IBucket = None, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        portfolio = servicecatalog.Portfolio(self, "Portfolio",
                                             display_name="MyPortfolio",
                                             provider_name="MyTeam"
                                             )

        role = Role(self, "Role",
                    assumed_by=AccountRootPrincipal()
                    )
        portfolio.give_access_to_role(role)

        product = servicecatalog.CloudFormationProduct(self, "Product",
                                                       product_name="My SageMaker Product",
                                                       owner="Product Owner",
                                                       product_versions=[servicecatalog.CloudFormationProductVersion(
                                                           product_version_name="v1",
                                                           cloud_formation_template=servicecatalog.CloudFormationTemplate.from_product_stack(
                                                               SageMakerProduct(self, "SageMakerProduct", asset_bucket=asset_bucket))
                                                       )
                                                       ]
                                                       )
