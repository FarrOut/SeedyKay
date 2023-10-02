from aws_cdk import (
    # Duration,
    NestedStack, RemovalPolicy, CfnOutput,
)
from aws_cdk.aws_acmpca import CfnCertificateAuthority, CfnCertificate
from constructs import Construct


class AcmStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.ca = CfnCertificateAuthority(self, "CA",
                                          type="ROOT",
                                          key_algorithm="RSA_2048",
                                          signing_algorithm="SHA256WITHRSA",
                                          subject=CfnCertificateAuthority.SubjectProperty(
                                              country="US",
                                              organization="Amazon Web Services",
                                              organizational_unit="Premium Support",
                                          )
                                          )
        self.ca.apply_removal_policy(RemovalPolicy.DESTROY)

        CfnOutput(self, 'CaArn',
                  description='The Amazon Resource Name (ARN) for the private CA that issued the certificate.',
                  value=self.ca.attr_arn,
                  )
        CfnOutput(self, 'CertificateSigningRequest',
                  description='The Base64 PEM-encoded certificate signing request (CSR) for your certificate '
                              'authority certificate.',
                  value=self.ca.attr_certificate_signing_request,
                  )
        CfnOutput(self, 'CaKeyAlgorithm',
                  description='Type of the public key algorithm and size, in bits, of the key pair that your CA '
                              'creates when it issues a certificate.',
                  value=self.ca.key_algorithm,
                  )
        CfnOutput(self, 'CaStorageSecurityStandard',
                  description='Specifies a cryptographic key management compliance standard used for handling CA keys.',
                  value=str(self.ca.key_storage_security_standard),
                  )
        CfnOutput(self, 'CaSigningAlgorithm',
                  description='Name of the algorithm your private CA uses to sign certificate requests.',
                  value=self.ca.signing_algorithm,
                  )
        CfnOutput(self, 'CaSubjectOrganization',
                  description='Structure that contains X.500 distinguished name information for your private CA.',
                  value=str(self.ca.subject.organization),
                  )
        CfnOutput(self, 'CaType',
                  description='Type of your private CA.',
                  value=self.ca.type,
                  )

        self.cert = CfnCertificate(self, "MyCfnCertificate",
                                   certificate_authority_arn=self.ca.attr_arn,
                                   certificate_signing_request=self.ca.attr_certificate_signing_request,
                                   signing_algorithm=self.ca.signing_algorithm,
                                   validity=CfnCertificate.ValidityProperty(
                                       type="MONTHS",
                                       value=3
                                   )
                                   )

        self.cert.apply_removal_policy(RemovalPolicy.DESTROY)

        CfnOutput(self, 'CertificateArn',
                  description='The Amazon Resource Name (ARN) for the certificate.',
                  value=self.cert.attr_arn,
                  )

        CfnOutput(self, 'CertificateAuthorityArn',
                  description='The Amazon Resource Name (ARN) for the certificate authority that issued the '
                              'certificate.',
                  value=self.cert.attr_certificate_authority_arn,
                  )
