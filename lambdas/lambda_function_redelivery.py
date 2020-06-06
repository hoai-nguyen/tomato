import json
import os
import boto3
import uuid

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    print("event requestShip: ", event)
    print("=========")
    
    try:

        table = dynamodb.Table('aws2020-01-nhom1-tomato-Orders-table')
        table.update_item(
                Key={
            'OrderID': event['OrderID']
            #  event['OrderID'] event.get('OrderID')
            },
            UpdateExpression="set DeliveryDateTime = :d, DeliveryAddress = :a",
            ExpressionAttributeValues={
                ':d': event['receiveDateTime'],
                ':a': event['receiveItemAddress']
            },
            ReturnValues="UPDATED_NEW"
        )
    except Exception as e:
        print(e)
        raise Exception('400')
        
    return {
        'statusCode': 200,
        'body': json.dumps('OK')
    }
