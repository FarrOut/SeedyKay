from aws_cdk import (
    # Duration,
    Stack, aws_kinesis as kinesis,
    CfnOutput, RemovalPolicy, Duration, )
from constructs import Construct


class KinesisStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        stream = kinesis.Stream(self, "Stream",
                                retention_period=Duration.days(1),

                                )
        stream.apply_removal_policy(RemovalPolicy.DESTROY)

        CfnOutput(self, "StreamName",
                  description='The name of the stream.',
                  value=stream.stream_name,
                  )
        CfnOutput(self, "StreamArn",
                  description='The ARN of the stream.',
                  value=stream.stream_arn,
                  )
        # CfnOutput(self, "EncryptionKey",
        #           description='Optional KMS encryption key associated with this stream.',
        #           value=str(stream.encryption_key.key_arn),
        #           )

        consumer = kinesis.CfnStreamConsumer(self, "MyCfnStreamConsumer",
                                             consumer_name="Sheeple",
                                             stream_arn=stream.stream_arn,
                                             )
        consumer.apply_removal_policy(RemovalPolicy.DESTROY)

        CfnOutput(self, "ConsumerArn",
                  description='When you register a consumer, Kinesis Data Streams generates an ARN for it.',
                  value=consumer.attr_consumer_arn,
                  )
        CfnOutput(self, "ConsumerCreationTimestamp",
                  description='The time at which the consumer was created.',
                  value=consumer.attr_consumer_creation_timestamp,
                  )
        CfnOutput(self, "ConsumerName",
                  description='The name you gave the consumer when you registered it.',
                  value=consumer.attr_consumer_name,
                  )
        CfnOutput(self, "ConsumerStatus",
                  description='A consumer can’t read data while in the CREATING or DELETING states.',
                  value=consumer.attr_consumer_status,
                  )
        CfnOutput(self, "ConsumerStreamArn",
                  description='The ARN of the data stream with which the consumer is registered.',
                  value=consumer.attr_stream_arn,
                  )
