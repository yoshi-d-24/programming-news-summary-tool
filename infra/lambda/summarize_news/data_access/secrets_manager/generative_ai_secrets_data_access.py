# Use this code snippet in your app.
# If you need more information about configurations
# or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developer/language/python/

import boto3
import json

session = boto3.session.Session()

class GenerateAiSecretsDataAccess:
    def __init__(self) -> None:
        self.client = session.client(
            service_name='secretsmanager',
        )

    def get_secret(self, key: str):
        secret_name: str = 'prod/PNST/GenerativeAI'

        get_secret_value_response = self.client.get_secret_value(
            SecretId=secret_name)

        secrets = json.loads(get_secret_value_response['SecretString'])

        return secrets[key]