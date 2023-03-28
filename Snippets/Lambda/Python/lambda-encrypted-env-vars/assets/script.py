import os
import boto3

secret_token = os.environ['secret_token']
secretsmanager_ = boto3.client('secretsmanager')

def handler(event, context):
    plaintext = secretsmanager_.get_secret_value(
        SecretId=secret_token)['SecretString']

    print("SECRET_TOKEN: " + str(secret_token))
    print("DECRYPTED: " + str(plaintext))
