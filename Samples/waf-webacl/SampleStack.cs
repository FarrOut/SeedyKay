using Amazon.CDK;
// using Amazon.CDK.AWS.WAF;
using Amazon.CDK.AWS.WAFv2;

namespace Sample
{
    public class SampleStack : Stack
    {
        internal SampleStack(Construct scope, string id, IStackProps props = null) : base(scope, id, props)
        {
             // The CDK includes built-in constructs for most resource types, such as Queues and Topics.
             var WebACL = new CfnWebACL(this, "WebACL", new CfnWebACLProps{
                Name = "MyWebACL",
                MetricName = "WebACL",
                DefaultAction = new CfnWebACL.WafActionProperty{
                  Type = "ALLOW"
                  },
               });

             new CfnOutput(this, "WebACLNameOutput", new CfnOutputProps{
               Value = WebACL.Name,
               Description = "WebACL Name."
               });
             // new CfnOutput(this, "WebACLDefaultActionOutput", new CfnOutputProps{
             //   Value = WebACL.DefaultAction,
             //   Description = "WebACL DefaultAction."
             //   });
        }
    }
}
