#!/usr/bin/env python3
import os

import aws_cdk as cdk

from events.receiver_stack import ReceiverStack
from events.sender_stack import SenderStack

app = cdk.App()

default_env = cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                              region=os.getenv('CDK_DEFAULT_REGION'))
sender_env = cdk.Environment(account='111111111111',
                             region=os.getenv('CDK_DEFAULT_REGION'))
receiver_env = cdk.Environment(account='222222222222',
                               region=os.getenv('CDK_DEFAULT_REGION'))

custom_source = "com.mycompany.myapp"

sender = SenderStack(app, "SenderStack",
                     receiver_account='222222222222',
                     source=custom_source,
                     env=sender_env,
                     )

receiver = ReceiverStack(app, "ReceiverStack",
                         sender_account='111111111111',
                         source=custom_source,
                         env=receiver_env,
                         )

app.synth()
