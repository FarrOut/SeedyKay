import aws_cdk as core
import aws_cdk.assertions as assertions

from security.secret_stack import SecurityStack

# example tests. To run these tests, uncomment this file along with the example
# resource in security/secret_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = SecurityStack(app, "security")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
