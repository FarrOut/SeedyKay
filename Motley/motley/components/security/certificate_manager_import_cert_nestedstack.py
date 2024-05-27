from aws_cdk import (
    # Duration,
    NestedStack, RemovalPolicy, CfnOutput,
)
from aws_cdk.aws_acmpca import CfnCertificateAuthority, CfnCertificate
from constructs import Construct


class CertificateManagerImportCertNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)



        # self.cert = CfnCertificate(self, "MyCfnCertificate",
        #                            certificate_authority_arn=self.ca.attr_arn,
        #                            certificate_signing_request=self.ca.attr_certificate_signing_request,
        #                            signing_algorithm=self.ca.signing_algorithm,
        #                            validity=CfnCertificate.ValidityProperty(
        #                                type="MONTHS",
        #                                value=3
        #                            )
        #                            )

        # self.cert.apply_removal_policy(RemovalPolicy.DESTROY)

        # CfnOutput(self, 'CertificateArn',
        #           description='The Amazon Resource Name (ARN) for the certificate.',
        #           value=self.cert.attr_arn,
        #           )

        # CfnOutput(self, 'CertificateAuthorityArn',
        #           description='The Amazon Resource Name (ARN) for the certificate authority that issued the '
        #                       'certificate.',
        #           value=self.cert.attr_certificate_authority_arn,
        #           )
