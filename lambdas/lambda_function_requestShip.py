import json
import os
import boto3
import uuid

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')


def generate_shipper(table):
    try:
        shipperID = str(uuid.uuid1())
        table.put_item(
            Item={
                'ShipperID': shipperID,
                'Email': 'aws202001.group1.shipper@gmail.com',
                'Phone' : '090xxxxxxxx',
                'ShipperStatus' : '0' #Avaiable
            }
        )
    except Exception as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 500,
            'body': json.dumps(e.response['Error']['Message'])
        }

    return shipperID
        

def pick_shipper(table):
    response = table.scan()
    for item in response['Items']:
        if (item.get('ShipperID')):
            return item['ShipperID']
            
    return generate_shipper(table)

#-----------------------------------------------------------------------
def lambda_handler(event, context):
    print("event requestShip: " , event)
    print("=========")
    orderTable = dynamodb.Table('aws2020-01-nhom1-tomato-Orders-table')
    shiperTable = dynamodb.Table('aws2020-01-nhom1-tomato-Shipper-Table')
    
    #Pick random shiper from Shiper table...
    shipperID = pick_shipper(shiperTable)

    # 3. Fill data from logDataObject to Orders table
    # for record in event:
    try:
        orderTable.put_item(
          Item={
                'OrderID': str(uuid.uuid1()),
                'DeliveryStatus': 'new',
                'PickItemDateTime': event['pickDateTime'],
                'DeliveryDateTime': event['receiveDateTime'],
                # 'ReDeliveryDateTime': event['ReDeliveryDateTime'],
                # 'DeliveryCount': event['DeliveryCount'],
                'ShopEmail': event['EmailSend'],
                'CustomerEmail': event['EmailReceive'],
                'PickItemAddress': event['AddressSend'],
                'DeliveryAddress': event['AddressReceive'],
                'CustomerPhone': event['PhoneReceive'],
                'ShipperID': shipperID
                # ,
                # 'ProductDescription': event['ProductDescription'],
                # 'CustomerMessage': event['CustomerMessage']
            }
        )
    except Exception as e:
        raise Exception('400' + str(e))
        
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
