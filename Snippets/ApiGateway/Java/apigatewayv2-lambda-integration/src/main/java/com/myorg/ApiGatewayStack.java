package com.myorg;

import software.amazon.awscdk.NestedStack;
import software.amazon.awscdk.services.apigatewayv2.CfnApi;
import software.constructs.Construct;

public class ApiGatewayStack extends NestedStack {

    public CfnApi api;
    private final String modelName = "ProductModel";

    public ApiGatewayStack(final Construct scope, final String id) {
        this(scope, id, null);
    }

    public ApiGatewayStack(final Construct scope, final String id, final ApiGatewayStackProps props) {
        super(scope, id, props);

        api = CfnApi.Builder.create(this, "MyCfnApi").name("Lambda Proxy").protocolType("HTTP").target(props.getTargetArn()).build();
    }


}


