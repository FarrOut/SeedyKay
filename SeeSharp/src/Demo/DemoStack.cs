using Amazon.CDK;
using Constructs;
using Amazon.CDK.AWS.SecretsManager;
using System.Collections.Generic;
using Amazon.CDK.AWS.IAM;
using Amazon.CDK.AWS.Lambda;


namespace Demo
{
    public class DemoStack : Stack
    {
        internal DemoStack(Construct scope, string id, IStackProps props = null) : base(scope, id, props)
        {
            // The code that defines your stack goes here

            var user = new User(this, "User");
            user.ApplyRemovalPolicy(RemovalPolicy.DESTROY);
            var accessKey = new AccessKey(this, "AccessKey", new AccessKeyProps { User = user });
            accessKey.ApplyRemovalPolicy(RemovalPolicy.DESTROY);

            var secret = new Secret(this, "Secret", new SecretProps
            {
                SecretObjectValue = new Dictionary<string, SecretValue> {
                { "username", SecretValue.UnsafePlainText(user.UserName) },
                { "database", SecretValue.UnsafePlainText("foo") },
                { "password", accessKey.SecretAccessKey }
            }
            });
            secret.ApplyRemovalPolicy(RemovalPolicy.DESTROY);

            _ = new CfnOutput(this, "SecretArn", new CfnOutputProps { Value = secret.SecretArn, Description = "The ARN of the secret in AWS Secrets Manager." });

            _ = new CfnOutput(this, "SecretFullArn", new CfnOutputProps { Value = secret.SecretFullArn, Description = "The full ARN of the secret in AWS Secrets Manager, which is the ARN including the Secrets Manager-supplied 6-character suffix." });

            _ = new CfnOutput(this, "SecretName", new CfnOutputProps { Value = secret.SecretName, Description = "The name of the secret." });


            var function = new Function(this, "Singleton", new FunctionProps
            {
                Runtime = Runtime.PYTHON_3_10,
                Code = Code.FromInline("def main(event, context):\n" + "    print(\"I'm running!\")\n"),
                Handler = "index.main",
                Timeout = Duration.Seconds(10),
            });
            function.ApplyRemovalPolicy(RemovalPolicy.DESTROY);

            var rotation = new RotationSchedule(this, "MyRotationSchedule", new RotationScheduleProps
            {
                Secret = secret,

                // the properties below are optional
                AutomaticallyAfter = Duration.Days(1),
                RotateImmediatelyOnUpdate = true,
                RotationLambda = function
            });
            rotation.ApplyRemovalPolicy(RemovalPolicy.DESTROY);


        }
    }
}
