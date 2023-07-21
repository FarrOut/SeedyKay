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
            // Users //

            var AdminUserStack = new UserStack(this, "AdminUserStack", new UserStackProps
            {
                UserName = "Admin",
                RemovalPolicy = RemovalPolicy.DESTROY
            });

            var BobUserStack = new UserStack(this, "BobUserStack", new UserStackProps
            {
                UserName = "Bob",
                RemovalPolicy = RemovalPolicy.DESTROY
            });

            var CharlieUserStack = new UserStack(this, "CharlieUserStack", new UserStackProps
            {
                UserName = "Charlie",
                RemovalPolicy = RemovalPolicy.DESTROY
            });

            // --------------------- //

            var SecretRotationStack = new SecretRotationStack(this, "SecretRotationStack", new SecretRotationStackProps
            {
                MasterSecret = AdminUserStack.Secret,
                RemovalPolicy = RemovalPolicy.DESTROY
            });




        }


    }
}
