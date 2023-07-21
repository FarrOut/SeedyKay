using Amazon.CDK;
using Constructs;
using Amazon.CDK.AWS.SecretsManager;
using System.Collections.Generic;
using Amazon.CDK.AWS.IAM;
using Amazon.CDK.AWS.Lambda;
using Amazon.CDK.AWS.RDS;
using Amazon.CDK.AWS.S3;
using Amazon.CDK.AWS.S3.Deployment;


namespace Demo
{

    public class SecretRotationStackProps : INestedStackProps
    {
        public Secret MasterSecret { get; set; }
        public RemovalPolicy RemovalPolicy { get; set; } = RemovalPolicy.RETAIN;

    }

    public class SecretRotationStack : NestedStack
    {
        public Function RotationLambda { get; }

        public SecretRotationStack(Construct scope, string id, SecretRotationStackProps props) : base(scope, id)
        {
            RotationLambda = new Function(this, "Singleton", new FunctionProps
            {
                Runtime = Runtime.PYTHON_3_10,
                Code = Code.FromAsset("src/scripts"),
                Handler = "index.main",
                Timeout = Duration.Seconds(10),
            });
            RotationLambda.ApplyRemovalPolicy(props.RemovalPolicy);

            var rotation = new RotationSchedule(this, "MyRotationSchedule", new RotationScheduleProps
            {
                Secret = props.MasterSecret,

                // the properties below are optional
                AutomaticallyAfter = Duration.Days(1),
                RotateImmediatelyOnUpdate = true,
                RotationLambda = RotationLambda,
            });
            rotation.ApplyRemovalPolicy(props.RemovalPolicy);

        }
    }
}
