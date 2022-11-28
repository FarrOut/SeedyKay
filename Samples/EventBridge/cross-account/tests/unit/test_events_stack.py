import aws_cdk as core
import aws_cdk.assertions as assertions

from events.sender_stack import EventsStack

# example tests. To run these tests, uncomment this file along with the example
# resource in events/sender_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = EventsStack(app, "events")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
