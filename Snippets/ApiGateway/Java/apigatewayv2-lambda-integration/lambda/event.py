import os
import json

def handler(event, context):

    print('## ENVIRONMENT VARIABLES')
    print(os.environ)
    print('## EVENT')
    print(json.dumps(event))

    return {
        "statusCode": 202
    }