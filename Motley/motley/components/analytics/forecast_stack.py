from aws_cdk import (
    # Duration,
    CfnTag, NestedStack, aws_kinesis as kinesis,aws_forecast as forecast,
    CfnOutput, RemovalPolicy, Duration, )
from constructs import Construct


class ForecastStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        dataset = forecast.CfnDataset(self, "MyCfnDataset",
            dataset_name="Loggie",
            dataset_type="RELATED_TIME_SERIES",
            domain="INVENTORY_PLANNING",
            schema={
                'item_id': 'string',
                'timestamp': 'string',
                'price': 'double'
            },

            # the properties below are optional
            data_frequency="1D",
            # encryption_config=encryption_config,
            tags=[forecast.CfnDataset.TagsItemsProperty(
                key="key",
                value="value"
            )]
        )

        CfnOutput(self, "DatasetArn", value=dataset.ref)

        # dataset_group = forecast.CfnDatasetGroup(self, "MyCfnDatasetGroup",
        #     dataset_group_name="Nostradamus",
        #     domain="domain",

        #     # the properties below are optional
        #     dataset_arns=["datasetArns"],
        #     tags=[CfnTag(
        #         key="Name",
        #         value="Nostradamus"
        #     )]
        # )