import json
import boto3
import os

sns_client = boto3.client('sns')

def lambda_handler(event, context):
    topic_arn = os.environ.get('SNS_TOPIC_ARN')
    
    if not topic_arn:
        return {
            'statusCode': 500,
            'body': json.dumps('Error: SNS_TOPIC_ARN environment variable is not set')
        }

    message = event.get('body', '本文なし')
    subject = "AWS Lambda Notification"

    try:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Message=message,
            Subject=subject
        )
        print(f"Message published: {response['MessageId']}")
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },            
            'body': json.dumps('Message published successfully')
        }
        
    except Exception as e:
        print(f"Error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST, OPTIONS'
            },            
            'body': json.dumps('Error publishing message')
        }