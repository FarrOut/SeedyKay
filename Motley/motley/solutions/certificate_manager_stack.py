from aws_cdk import (
    # Duration,
    Stack, RemovalPolicy,
)
from constructs import Construct

from motley.components.analytics.canary_nestedstack import CanaryNestedStack
from motley.components.analytics.forecast_stack import ForecastStack
from motley.components.security.certificate_manager_import_cert_nestedstack import CertificateManagerImportCertNestedStack


class CertificateManagerStack(Stack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cert_stack = CertificateManagerImportCertNestedStack(self, 'CertificateManagerImportCertNestedStack',
                                                             removal_policy=removal_policy,
                                                             )
