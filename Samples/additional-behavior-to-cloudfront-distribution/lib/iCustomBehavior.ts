import {AddBehaviorOptions, IOrigin} from "aws-cdk-lib/aws-cloudfront";


export interface iCustomBehavior {
    pathPattern: string;
    origin: IOrigin;
    behaviorOptions?: AddBehaviorOptions;
}
