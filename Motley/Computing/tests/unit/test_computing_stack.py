import aws_cdk as core
import aws_cdk.assertions as assertions

from computing.computing_stack import ComputingStack

# example tests. To run these tests, uncomment this file along with the example
# resource in computing/computing_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ComputingStack(app, "computing")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
