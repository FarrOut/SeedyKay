from aws_cdk import core as cdk, aws_apigateway as apigateway


class ReproStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api_ = apigateway.RestApi(self, "pretty-fly-for-an-api",
                                  deploy_options=apigateway.StageOptions(stage_name="default"))

        request_json_schema = apigateway.JsonSchema(
            schema=apigateway.JsonSchemaVersion.DRAFT4,
            title="Map",
            type=apigateway.JsonSchemaType.OBJECT,
            additional_properties=apigateway.JsonSchema(
                type=apigateway.JsonSchemaType.OBJECT,
                ref="#/definitions/Car",
            ),
            definitions=dict(Car=apigateway.JsonSchema(
                type=apigateway.JsonSchemaType.OBJECT,
                additional_properties=False,
                properties=dict(
                    model_code=apigateway.JsonSchema(
                        type=apigateway.JsonSchemaType.STRING,
                    ),
                    part_types=apigateway.JsonSchema(
                        type=apigateway.JsonSchemaType.OBJECT,
                        additional_properties=dict(
                            # ref="#/definitions/PartInfo",
                        ),
                    )
                ),
            )),
        )

        request_model = api_.add_model("room-api-getContent-request",
                                       content_type="application/json",
                                       model_name="getContentRequest",
                                       schema=request_json_schema)

        get_content_resource = api_.root.add_resource(
            "getContent")
        get_content_resource.add_method("POST", api_key_required=True,
                                                request_validator=apigateway.RequestValidator(
                                                    scope=self,
                                                    rest_api=api_,
                                                    id="api-validator",
                                                    request_validator_name="api-validator",
                                                    validate_request_body=True
                                                ),
                                                # integration=lambda_integration,
                                                request_models={
                                                    "application/json": request_model
                                                })
