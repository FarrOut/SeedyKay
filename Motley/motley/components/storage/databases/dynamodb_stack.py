from aws_cdk import (
    # Duration,
    CfnOutput,
    RemovalPolicy,
    Stack,
    aws_dynamodb as dynamodb,
)
from constructs import Construct


class DynamoDBStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        table = dynamodb.Table(self, "Table",
                               partition_key=dynamodb.Attribute(
                                   name="id", type=dynamodb.AttributeType.STRING),
                               table_class=dynamodb.TableClass.STANDARD,
                               removal_policy=RemovalPolicy.DESTROY,
                               )

        CfnOutput(self, "TableName",
                  value=table.table_name,
                  description="DynamoDB Table Name")

        CfnOutput(self, "TableArn",
                  value=table.table_arn,
                  description="DynamoDB Table ARN")
        CfnOutput(self, "TableStreamArn",
                  value=str(table.table_stream_arn),
                  description="DynamoDB Table Stream ARN")
