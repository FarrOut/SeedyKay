package com.myorg;

import software.amazon.awscdk.CfnOutput;
import software.amazon.awscdk.Stack;
import software.amazon.awscdk.StackProps;
import software.amazon.awscdk.services.apigatewayv2.CfnIntegration;
import software.amazon.awscdk.services.lambda.Code;
import software.amazon.awscdk.services.lambda.FunctionProps;
import software.amazon.awscdk.services.lambda.Runtime;
import software.amazon.awsconstructs.services.apigatewaylambda.ApiGatewayToLambda;
import software.amazon.awsconstructs.services.apigatewaylambda.ApiGatewayToLambdaProps;
import software.constructs.Construct;

public class IntegrationStack extends Stack {
    public IntegrationStack(final Construct scope, final String id) {
        this(scope, id, null);
    }

    public IntegrationStack(final Construct scope, final String id, final StackProps props) {
        super(scope, id, props);

        LambdaStack lambdaStack = new LambdaStack(this, "LambdaStack");
        ApiGatewayStack apiGatewayStack = new ApiGatewayStack(this, "ApiGatewayStack",
                new ApiGatewayStackProps().setTargetArn(lambdaStack.function.getFunctionArn()));


        CfnOutput.Builder.create(this, "FunctionArn").value(lambdaStack.function.getFunctionArn()).build();
        CfnOutput.Builder.create(this, "ApiGatewayId").value(apiGatewayStack.api.getAttrApiId()).build();

        StringBuilder integrationUri = new StringBuilder();
        integrationUri.append("");
        integrationUri.append("arn:");
        integrationUri.append(this.getPartition());
        integrationUri.append(":apigateway:");
        integrationUri.append(this.getRegion());
        integrationUri.append(":lambda:path/2015-03-31/functions/");
        integrationUri.append(lambdaStack.function.getFunctionArn());
        integrationUri.append("/invocations");

        /**
         *
         * Plain integration using CfnIntegration L1 construct.
         *
         */
        CfnIntegration cfnIntegration = CfnIntegration.Builder.create(this, "MyCfnIntegration")
                .apiId(apiGatewayStack.api.getRef())
                .integrationType("AWS_PROXY")
                .integrationUri(integrationUri.toString())
                .payloadFormatVersion("2.0")
                .build();

        CfnOutput.Builder.create(this, "IntegrationId").value(cfnIntegration.getRef()).
                description("Returns the Integration resource ID, such as abcd123.").build();

        CfnOutput.Builder.create(this, "IntegrationUri").value(integrationUri.toString()).
                description("For a Lambda integration, specify the URI of a Lambda function.").build();

        /**
         * AWS Solutions Constructs
         * aws-apigateway-lambda
         *
         * @see https://docs.aws.amazon.com/solutions/latest/constructs/aws-apigateway-lambda.html
         */
        ApiGatewayToLambda integrationSolution = new ApiGatewayToLambda(this, "ApiGatewayToLambdaPattern", new ApiGatewayToLambdaProps.Builder()
                .lambdaFunctionProps(new FunctionProps.Builder()
                        .runtime(Runtime.NODEJS_18_X) // execution environment
                        .code(Code.fromAsset("lambda")) // code loaded from the "lambda" directory
                        .handler("hello.handler") // file is "hello", function is "handler"
                        .build())
                .build());

        CfnOutput.Builder.create(this, "IntegrationSolutionLogGroupArn").value(integrationSolution.getApiGatewayLogGroup().getLogGroupArn()).
                description("Arn of CloudWatch LogGroup to which this AWS Solutions ApiGatewayToLambda integration pushes logs.").build();
    }
}
