import * as cdk from 'aws-cdk-lib';
import {CfnOutput} from 'aws-cdk-lib';
import {Construct} from 'constructs';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';
import {MockIntegration, PassthroughBehavior} from 'aws-cdk-lib/aws-apigateway';

export class LabStack extends cdk.Stack {
    constructor(scope: Construct, id: string, props?: cdk.StackProps) {
        super(scope, id, props);

        const api = new apigateway.RestApi(this, 'demo-api', {
            restApiName: 'Pretty fly for an API',

            // You can add CORS at the resource-level using addCorsPreflight.
            // https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_apigateway.RestApi.html#defaultcorspreflightoptions
            // defaultCorsPreflightOptions: {
            //     allowOrigins: ['http://localhost:3000'],
            //     allowMethods: apigateway.Cors.DEFAULT_HEADERS
            // }
        });


        //                   _
        //   /\/\   ___   ___| | _____ _ __ _   _
        //  /    \ / _ \ / __| |/ / _ \ '__| | | |
        // / /\/\ \ (_) | (__|   <  __/ |  | |_| |
        // \/    \/\___/ \___|_|\_\___|_|   \__, |
        //                                  |___/

        const integration = new MockIntegration({
            integrationResponses: [
                {statusCode: '200'},
            ],
            passthroughBehavior: PassthroughBehavior.NEVER,
            requestTemplates: {
                'application/json': '{ "statusCode": 200 }',
            },
        })

        let resource = api.root.addResource('mock');

        resource.addMethod('GET', integration, {
            methodResponses: [
                {statusCode: '200'},
            ],
        })

        //  _____ _              ___   ___  __  __
        // /__   \ |__   ___    / __\ /___\/__\/ _\
        //   / /\/ '_ \ / _ \  / /   //  // \//\ \
        //  / /  | | | |  __/ / /___/ \_// _  \_\ \
        //  \/   |_| |_|\___| \____/\___/\/ \_/\__/
        //
        let cors_preflight_options = {
            allowOrigins: ['https://mock.amazon.com'],
            allowMethods: ['GET', 'PUT']
        }

        // Enable CORS
        resource.addCorsPreflight(cors_preflight_options)


        //   ___       _               _
        //   /___\_   _| |_ _ __  _   _| |_ ___
        //  //  // | | | __| '_ \| | | | __/ __|
        // / \_//| |_| | |_| |_) | |_| | |_\__ \
        // \___/  \__,_|\__| .__/ \__,_|\__|___/
        //                 |_|

        new CfnOutput(this, 'RestApiName', {
            description: 'A human friendly name for this Rest API.',
            value: api.restApiName,
        })
        new CfnOutput(this, 'RestApiId', {
            description: 'The ID of this API Gateway RestApi.',
            value: api.restApiId,
        })
        new CfnOutput(this, 'DemoResourceId', {
            description: 'The resource ID of the demo resource.',
            value: resource.resourceId,
        })
    }
}
