from ast import Str
import logging
import boto3
from boto3.dynamodb.conditions import Key
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region_name = os.getenv('REGION_NAME')
db_users = os.getenv('DB_USERS')


async def check_email(email: Str):
    session = boto3.Session(aws_access_key_id=aws_access_key_id,
                            aws_secret_access_key=aws_secret_access_key, region_name=region_name)

    # DynamoDB table name for users data (Key = email)
    # Updates are made to "discord" attribute in welcome_bot.py
    DB_USERS = db_users

    # Setup AWS resources
    dynamodb = session.resource("dynamodb", region_name)
    table = dynamodb.Table(DB_USERS)
    
    try:
        response = table.query(KeyConditionExpression=Key('email').eq(email))

        if response['Items'][0]['email'] == email:
            name = response['Items'][0]['name']
            role = response['Items'][0]['role']
            teamname = response['Items'][0]['teamname'][0]
            return [True, name, role, teamname]
        else:
            return False
    except:
        return False

print(check_email('woodson.tlm@gmail.com'))
