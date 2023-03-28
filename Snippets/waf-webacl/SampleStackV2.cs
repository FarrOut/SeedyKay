using Amazon.CDK;
using Amazon.CDK.AWS.WAFv2;

namespace Sample
{
    public class SampleStackV2 : Stack
    {
        internal SampleStackV2(Construct scope, string id, IStackProps props = null) : base(scope, id, props)
        {
            // WAFv2
            var WebACL = new CfnWebACL(this, "WebACL", new CfnWebACLProps{
               Name = "MyWebACL",
               Scope = "REGIONAL",
               DefaultAction =  new CfnWebACL.DefaultActionProperty {
                   Allow = new CfnWebACL.AllowActionProperty{}
               },
               VisibilityConfig = new CfnWebACL.VisibilityConfigProperty {
                   SampledRequestsEnabled = true,
                   CloudWatchMetricsEnabled = true,
                   MetricName = "WebACL",
               },
               Rules = new CfnWebACL.RuleProperty[] {}
              });

             new CfnOutput(this, "WebACLNameOutput", new CfnOutputProps{
               Value = WebACL.Name,
               Description = "WebACL Name."
               });
        }
    }
}
