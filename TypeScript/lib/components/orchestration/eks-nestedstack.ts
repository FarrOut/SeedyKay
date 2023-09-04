
import * as eks from 'aws-cdk-lib/aws-eks';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as kms from 'aws-cdk-lib/aws-kms';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import { Cluster, EndpointAccess, KubernetesVersion } from 'aws-cdk-lib/aws-eks';
import { PhysicalName } from 'aws-cdk-lib';

import * as lambda from 'aws-cdk-lib/aws-lambda';

interface EksClusterProps extends cdk.StackProps {
  SecretsEncryptionKey?: kms.Key,
  MastersRole?: iam.Role,
  k8sVersion: KubernetesVersion,
  Vpc?: ec2.IVpc,
  PlaceClusterHandlerInVpc?: boolean,
  KubectlLayer?: lambda.ILayerVersion,
}


export class EksNestedStack extends cdk.NestedStack {

  public readonly cluster: eks.Cluster;  

  constructor(scope: Construct, id: string, props: EksClusterProps) {
    super(scope, id, props);      

    this.cluster = new Cluster(this, 'EKSCluster', {
      version: props.k8sVersion,
      defaultCapacity: 0,
      // https://aws.github.io/aws-eks-best-practices/security/docs/iam/#make-the-eks-cluster-endpoint-private
      endpointAccess: EndpointAccess.PRIVATE,
      vpc: props.Vpc,
      secretsEncryptionKey: props.SecretsEncryptionKey,
      mastersRole: props.MastersRole,
      clusterName: PhysicalName.GENERATE_IF_NEEDED,
      kubectlLayer: props.KubectlLayer,

      // Ensure EKS helper lambadas are in private subnets
      placeClusterHandlerInVpc: props.PlaceClusterHandlerInVpc,
    });
  }
}