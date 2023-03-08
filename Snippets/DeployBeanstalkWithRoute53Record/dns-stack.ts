import * as cdk from '@aws-cdk/core';
import * as eb from '@aws-cdk/aws-elasticbeanstalk';
import * as ec2 from '@aws-cdk/aws-ec2';
import * as route53 from '@aws-cdk/aws-route53';
import * as route53targets from '@aws-cdk/aws-route53-targets';
import * as s3assets from '@aws-cdk/aws-s3-assets';

export class DnsStack extends cdk.Stack {
  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // ====================================================
    // VPC
    // ====================================================

    const vpc = new ec2.Vpc(this, 'VPC');

    const publicSubnets = vpc.selectSubnets({
      subnetType: ec2.SubnetType.PUBLIC
    });

    const privateSubnets = vpc.selectSubnets({
      subnetType: ec2.SubnetType.PRIVATE
    });


    // ====================================================
    // ElasticBeanstalk
    // ====================================================

    const appName = 'MyApp';

    // Construct an S3 asset from the ZIP located from directory up.
    const elbZipArchive = new s3assets.Asset(this, 'MyElbAppZip', {
      path: `${__dirname}/../nodejs.zip`,
    });

    const app = new eb.CfnApplication(this, 'Application', {
      applicationName: appName
    });

    // Example of some options which can be configured
    const optionSettingProperties: eb.CfnEnvironment.OptionSettingProperty[] = [
      {
        namespace: 'aws:autoscaling:launchconfiguration',
        optionName: 'InstanceType',
        value: 't3.small',
      },
      {
        namespace: "aws:autoscaling:asg",
        optionName: "MinSize",
        value: "2"
      },
      {
        namespace: "aws:autoscaling:asg",
        optionName: "MaxSize",
        value: "6"
      },
      {
        namespace: 'aws:autoscaling:launchconfiguration',
        optionName: 'IamInstanceProfile',
        // Here you could reference an instance profile by ARN (e.g. myIamInstanceProfile.attrArn)
        // For the default setup, leave this as is (it is assumed this role exists)
        // https://stackoverflow.com/a/55033663/6894670
        value: 'aws-elasticbeanstalk-ec2-role',
      },
      {
        namespace: "aws:elasticbeanstalk:environment",
        optionName: "EnvironmentType",
        value: "LoadBalanced"
      },
      {
        namespace: 'aws:ec2:vpc',
        optionName: 'VPCId',
        value: vpc.vpcId
      },
      {
        namespace: 'aws:ec2:vpc',
        optionName: 'AssociatePublicIpAddress',
        value: 'true'
      },
      {
        namespace: 'aws:ec2:vpc',
        optionName: 'ELBScheme',
        value: 'public'
      },
      {
        namespace: 'aws:ec2:vpc',
        optionName: 'ELBSubnets',
        value: publicSubnets.subnetIds.toString()
      },
      {
        resourceName: 'AWSEBAutoScalingGroup',
        namespace: 'aws:ec2:vpc',
        optionName: 'Subnets',
        // Private vpc subnets
        value: privateSubnets.subnetIds.toString()
      }
    ];

    const appVersionProps = new eb.CfnApplicationVersion(this, 'AppVersion', {
      applicationName: appName,
      sourceBundle: {
        s3Bucket: elbZipArchive.s3BucketName,
        s3Key: elbZipArchive.s3ObjectKey,
      },
    });

    const env = new eb.CfnEnvironment(this, 'Environment', {
      environmentName: 'MyEnvironment',
      applicationName: app.applicationName || appName,
      solutionStackName: '64bit Amazon Linux 2 v5.5.5 running Node.js 16',
      optionSettings: optionSettingProperties,
      // This line is critical - reference the label created in this same stack
      versionLabel: appVersionProps.ref,
    });


    // Also very important - make sure that `app` exists before creating an app version
    appVersionProps.addDependsOn(app);

    // to ensure the application is created before the environment
    env.addDependsOn(app);


    new cdk.CfnOutput(this, 'BeanstalkEndpoint', {
      description: 'Endpoint of ElasticBeanstalk environment.',
      value: env.attrEndpointUrl
    })

    // ====================================================
    // Route 53
    // ====================================================
    var domainName = 'example.com'
    const zone = new route53.PrivateHostedZone(this, 'HostedZone', {
      zoneName: domainName,
      vpc    // At least one VPC has to be added to a Private Hosted Zone.
    });

    const record: route53.IAliasRecordTarget = {
      bind: (): route53.AliasRecordTargetConfig => ({
        dnsName: env.attrEndpointUrl,
        // For more regions' service endpoints, please see:
        // https://docs.aws.amazon.com/general/latest/gr/elb.html
        hostedZoneId: 'Z32O12XQLNTSW2', // for eu-west-1 ELB
      }),
    }

    new route53.ARecord(this, 'aliasrecord-elb', {
        zone,
        recordName: 'jack',
        target: route53.AddressRecordTarget.fromAlias(record),
    })

  }
}
