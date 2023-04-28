import json
import boto3


dynamodb = boto3.resource('dynamodb')
client = boto3.client('dynamodb')
tablename = dynamodb.Table('website-StaticWebStack-counttable94281A0C-1SWZTCYVB639G')

def lambda_handler(event, context):
    tablename.update_item(
        #Key={'ID': event['ID']},
        Key={'count': 'ID'},
        UpdateExpression='ADD Visits :incr',
        ExpressionAttributeValues={':incr': 1},
        ReturnValues="UPDATED_NEW"
       
    )

    data = client.get_item(
    TableName='website-StaticWebStack-counttable94281A0C-1SWZTCYVB639G',
    Key={
        'count': {
          'S': 'ID'

        }

    }
    )
    count = data['Item']
   #return count
    print(count)
    print(data)
   
    return count
             
             