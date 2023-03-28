import aws_cdk as core
import aws_cdk.assertions as assertions

from cicd.codepipeline_stack import CicdStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cicd/codepipeline_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CicdStack(app, "cicd")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
