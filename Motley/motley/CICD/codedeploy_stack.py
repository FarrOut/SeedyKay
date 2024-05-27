from aws_cdk import (
    # Duration,
    NestedStack, CfnOutput,
    aws_codedeploy as codedeploy, RemovalPolicy, aws_autoscaling as autoscaling, )
from constructs import Construct


class CodeDeployStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, asg: autoscaling.AutoScalingGroup, load_balancer: codedeploy.LoadBalancer,  removal_policy: RemovalPolicy, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # TODO
        # application = codedeploy.ServerApplication(self, "CodeDeployApplication",
        #     application_name="MyApplication"
        # )
        # application.apply_removal_policy(removal_policy)

        # CfnOutput(self, "ApplicationName", value=application.application_name, description="The name of the application.")        
        # CfnOutput(self, "ApplicationArn", value=application.application_arn, description="The ARN of the application.")        

        # TODO
        # alarm = cloudwatch.Alarm(self, "Alarm",
        #     metric=application.metric_healthy_hosts(),
        #     comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_THRESHOLD,            
        #     threshold=10,
        #     evaluation_periods=2
        # )
        # alarm.apply_removal_policy(removal_policy)
        # CfnOutput(self, "AlarmName", value=alarm.alarm_name, description="The name of the alarm.")
        # CfnOutput(self, "AlarmArn", value=alarm.alarm_arn, description="The ARN of the alarm.")


        self.deployment_group = codedeploy.ServerDeploymentGroup(self, "CodeDeployDeploymentGroup",
            # application=application,
            # deployment_group_name="MyDeploymentGroup",
            # auto_scaling_groups=[asg],
            load_balancer=load_balancer,

            # adds User Data that installs the CodeDeploy agent on your auto-scaling groups hosts
            # default: true
            install_agent=True,
            # adds EC2 instances matching tags
            ec2_instance_tags=codedeploy.InstanceTagSet({
                # any instance with tags satisfying
                # key1=v1 or key1=v2 or key2 (any value) or value v3 (any key)
                # will match this group
                "key1": ["v1", "v2"],
                "key2": [],
                "": ["v3"]
            }),
            # adds on-premise instances matching tags
            on_premise_instance_tags=codedeploy.InstanceTagSet({
                "key1": ["v1", "v2"]
            }, {
                "key2": ["v3"]
            }),
            # CloudWatch alarms
            # alarms=[alarm],
            # whether to ignore failure to fetch the status of alarms from CloudWatch
            # default: false
            ignore_poll_alarms_failure=False,
            # auto-rollback configuration
            auto_rollback=codedeploy.AutoRollbackConfig(
                failed_deployment=True,  # default: true
                stopped_deployment=True,  # default: false
                # deployment_in_alarm=True
            )
        )        
        self.deployment_group.apply_removal_policy(removal_policy)

        CfnOutput(self, "DeploymentGroupName", value=self.deployment_group.deployment_group_name, description="The name of the Deployment Group.")
        CfnOutput(self, "DeploymentGroupArn", value=self.deployment_group.deployment_group_arn, description="The ARN of the Deployment Group.")
