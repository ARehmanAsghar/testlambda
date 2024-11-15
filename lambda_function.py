import json
import boto3
import os
from io import BytesIO
from datetime import datetime

s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table_name = os.getenv('ImageMetadata')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    object_key = None  # Initialize object_key variable here
    try:
        # Check if event structure contains 'Records'
        if 'Records' not in event:
            raise ValueError("Event structure is invalid, 'Records' not found")

        # Extract the bucket name and object key from the event
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = event['Records'][0]['s3']['object']['key']
        
        # Fetch the image from S3
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        img_data = response['Body'].read()

        # Just store the image data as-is
        buffer = BytesIO(img_data)
        original_key = 'original/' + object_key.split('/')[-1]
        s3.put_object(Bucket=bucket_name, Key=original_key, Body=buffer, ContentType='image/jpeg')

        # Metadata for the image
        metadata = {
            'ImageID': object_key.split('/')[-1],
            'Timestamp': datetime.utcnow().isoformat()
        }

        # Store metadata in DynamoDB
        table.put_item(Item=metadata)

        return {
            'statusCode': 200,
            'body': json.dumps(f"Image stored and metadata saved for {object_key}")
        }

    except Exception as e:
        # Handle errors and provide meaningful feedback
        print(f"Error processing image: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Failed to process image {object_key if object_key else 'unknown'}: {str(e)}")
        }
