using Amazon.CDK;
using Constructs;
using Amazon.CDK.AWS.SecretsManager;
using System.Collections.Generic;
using Amazon.CDK.AWS.IAM;
using Amazon.CDK.AWS.Lambda;
using Amazon.CDK.AWS.RDS;


namespace Demo
{

    public class UserStackProps : INestedStackProps
    {

        public string UserName { get; set; }
        public RemovalPolicy RemovalPolicy { get; set; } = RemovalPolicy.RETAIN;
    }
    public class UserStack : NestedStack
    {
        public User User { get; }
        public Secret Secret { get; }


        public UserStack(Construct scope, string id, UserStackProps props) : base(scope, id)
        {
            // Admin User //
            User = new User(this, "User", new UserProps { UserName = props.UserName });
            User.ApplyRemovalPolicy(props.RemovalPolicy);

            var accessKey = new AccessKey(this, "AccessKey", new AccessKeyProps { User = User });
            accessKey.ApplyRemovalPolicy(props.RemovalPolicy);

            Secret = new Secret(this, "Secret", new SecretProps
            {
                SecretObjectValue = new Dictionary<string, SecretValue> {
                { "username", SecretValue.UnsafePlainText(User.UserName) },
                { "database", SecretValue.UnsafePlainText("foo") },
                { "password", accessKey.SecretAccessKey }
            }
            });
            Secret.ApplyRemovalPolicy(props.RemovalPolicy);

            _ = new CfnOutput(this, "SecretArn", new CfnOutputProps { Value = Secret.SecretArn, Description = "The ARN of the secret in AWS Secrets Manager." });

            _ = new CfnOutput(this, "SecretFullArn", new CfnOutputProps { Value = Secret.SecretFullArn, Description = "The full ARN of the secret in AWS Secrets Manager, which is the ARN including the Secrets Manager-supplied 6-character suffix." });

            _ = new CfnOutput(this, "SecretName", new CfnOutputProps { Value = Secret.SecretName, Description = "The name of the secret." });
        }
    }
}
