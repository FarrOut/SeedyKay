from aws_cdk import (
    # Duration,
    aws_synthetics_alpha as synthetics, aws_lambda as lambda_, aws_cloudwatch as cloudwatch, aws_ec2 as ec2, aws_sns as sns, aws_cloudwatch_actions as cw_actions,
    NestedStack, RemovalPolicy, Duration, CfnOutput, )
from aws_cdk.aws_synthetics_alpha import Code, RuntimeFamily
from constructs import Construct


class CloudWatchDashboardNestedStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str,
                 removal_policy: RemovalPolicy = RemovalPolicy.RETAIN,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        dashboard = cloudwatch.Dashboard(self, "Dash",)
        dashboard.apply_removal_policy(removal_policy)

        CfnOutput(self, "DashboardArn", value=dashboard.dashboard_arn,
                  description='ARN of this dashboard.')
        CfnOutput(self, "DashboardName", value=dashboard.dashboard_name,
                  description='The name of this dashboard.')

        gauge_widget = dashboard.add_widgets(cloudwatch.GaugeWidget(
            title="My gauge widget",
            metrics=[cloudwatch.Metric(
                metric_name='TunnelState',
                namespace="AWS/VPN",
                dimensions_map={
                    "TunnelIpAddress": "123.123.123.123"
                },
                statistic='Minimum'
            )],
            left_y_axis=cloudwatch.YAxisProps(
                min=0,
                max=1
            ),
            annotations=[cloudwatch.HorizontalAnnotation(
                color="#b2df8d",
                label="Up",
                value=1,
                fill=cloudwatch.Shading.ABOVE,
            )],
            statistic="Minimum",
            period=Duration.minutes(1),
            width=6,
            height=6,
        ))

        
