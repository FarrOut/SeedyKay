
import * as iam from 'aws-cdk-lib/aws-iam';
import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';

interface CustomProps extends cdk.StackProps {
  RemovalPolicy: cdk.RemovalPolicy,
}

export class IamNestedStack extends cdk.NestedStack {

  constructor(scope: Construct, id: string, props: CustomProps) {
    super(scope, id, props);

    let AccountRootPrincipal = new iam.AccountRootPrincipal()
    let AccountRootPrincipalJson = AccountRootPrincipal.toJSON()

    let PolicyDocJson = {
      "Version": "2008-10-17",
      "Statement": [
        {
          "Action": "sts:AssumeRole",
          "Effect": "Allow",
          "Principal": AccountRootPrincipalJson
        }
      ]
    }

    new cdk.CfnOutput(this, 'AccountRootPrincipalJson', {
      value: JSON.stringify(AccountRootPrincipalJson),
      description: 'AccountRootPrincipal Json', // Optional
    });
    new cdk.CfnOutput(this, 'PolicyDocJson', {
      value: JSON.stringify(PolicyDocJson),
      description: 'PolicyDoc Json', // Optional
    });

    const Version2008Role = new iam.Role(this, 'Version2008Role', {
      /* 
      * assumedBy is redundant as it will be overriden later anyway
      * but it is a mandatory property for the L2 IRole construct...
      * so we just populate it with something anyway.
      */
      assumedBy: AccountRootPrincipal,
      description: 'Example role using policy document version 2008...',
    });
    Version2008Role.applyRemovalPolicy(props.RemovalPolicy)

    new cdk.CfnOutput(this, 'Role2008Name', {
      value: Version2008Role.roleName,
      description: 'Returns the name of the role.', // Optional
    });

    new cdk.CfnOutput(this, 'Role2008Arn', {
      value: Version2008Role.roleArn,
      description: 'Returns the ARN of this role.', // Optional
    });

    /*
    * Here we are overriding the AssumeRolePolicyDocument property of the L2 IRole construct.
    * Using a raw override Escape Hatch
    * See https://docs.aws.amazon.com/cdk/v2/guide/cfn_layer.html#cfn_layer_raw    
    */
    const cfnRole = Version2008Role.node.defaultChild as iam.CfnRole;
    cfnRole.addPropertyOverride('AssumeRolePolicyDocument', PolicyDocJson)

  }
}