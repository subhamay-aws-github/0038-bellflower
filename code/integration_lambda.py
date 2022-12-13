import json
import logging
import boto3
import os

# Load the exceptions for error handling
from botocore.exceptions import ClientError, ParamValidationError
from boto3.dynamodb.types import TypeDeserializer, TypeSerializer

logger = logging.getLogger()
logger.setLevel(logging.INFO)

sfn_client = boto3.client('stepfunctions', region_name=os.environ.get('AWS_REGION'))
ses_client = boto3.client('ses', region_name=os.environ.get('AWS_REGION')) 
s3_resource = boto3.resource('s3', region_name=os.environ.get('AWS_REGION'))
s3_client = boto3.client('s3', region_name=os.environ.get('AWS_REGION'))
account_id = boto3.client('sts').get_caller_identity().get('Account')
region = os.environ.get('AWS_REGION')
state_machine = os.environ.get("STATE_MACHINE")
s3_bucket_name = os.environ.get("S3_BUCKET_NAME")

logger.info(f"account_id = {account_id}")
logger.info(f"region = {region}")
logger.info(f"state_machine = {state_machine}")

def get_event_source(event):
    if "Records" in event:
        if event["Records"][0]["eventSource"] == "aws:sqs":
            return "sqs"
        elif event["Records"][0]["eventSource"] == "aws:s3":
            return "s3"
        else:
            return "unknown"
    else:
        return "unknown"
        
def write_to_s3(bucket_name, execution_id, file_name, data):
    
    try:
        s3_object = s3_resource.Object(bucket_name, f"outbound/{execution_id}/{file_name}")
        
        result = s3_object.put(Body=data)
        
        response = result.get('ResponseMetadata')
    
        if response.get('HTTPStatusCode') == 200:
            logger.info('File Uploaded Successfully')
            
            return response.get('HTTPStatusCode')
        else:
            logger.error('File Not Uploaded')
            return response.get('HTTPStatusCode')
            
    # An error occurred
    except ParamValidationError as e:
        logger.error(f"Parameter validation error: {e}")
    except ClientError as e:
        logger.error(f"Client error: {e}")
        
def read_from_s3(bucket_name, key):
    
    try:
        data_object = s3_client.get_object(
            Bucket=bucket_name,
            Key=key
            )
        data_string = data_object['Body'].read().decode('utf-8')
        
        return data_string
    # An error occurred
    except ParamValidationError as e:
        logger.error(f"Parameter validation error: {e}")
    except ClientError as e:
        logger.error(f"Client error: {e}")
    
    
def lambda_handler(event, context):
    # TODO implement
    
    logger.info(f"event = {json.dumps(event)}") 
    logger.info(f"function_name = {context.function_name} : event_source = {get_event_source(event)}")
    try:
        if get_event_source(event) == "sqs":
            sfn_input = json.loads(event['Records'][0]['body'])
            input = sfn_input.get('Input')
            task_token = sfn_input.get('TaskToken')
            execution_id = input.get("execution_id")
            info = dict(info=input.get("info"))
            
            logger.info(f"execution_id = {execution_id}")
            logger.info(f"info = {json.dumps(info)}")
            
            response = write_to_s3(s3_bucket_name, execution_id, 'task_token.txt' , task_token)
            
            if response == '200':
                logger.info(f"task_token uploaded to S3 bucket outbound folder successfully !")
            
            response = write_to_s3(s3_bucket_name, execution_id, 'data.json' , json.dumps(info))
            if response == '200':
                logger.info(f"info uploaded to S3 bucket outbound folder successfully !")
          
            return {
                'function_name': context.function_name,
                'status': 'success',
                'status_code': 200
            }      
        elif get_event_source(event) == "s3":
            object_key = event["Records"][0]["s3"]["object"]["key"]
            execution_id = (object_key.split("/")[1]).split(".")[0]
            
            logger.info(f"execution_id = {execution_id}")
            
            task_token = read_from_s3(s3_bucket_name, f"outbound/{execution_id}/task_token.txt")
            
            response = sfn_client.send_task_success(taskToken=task_token,
                                                    output=json.dumps({'status':'Response Received'})
                                                    )
    
            logger.info(f"response = {response}")
        else:
            logger.error("Invalid Event Source")
    except Exception as e:
        logger.error(f"write_to_s3 : Error {e}") 
        return {
            'function_name': context.function_name,
            'status': 'failure',
            'status_code': -1
        } 
        
