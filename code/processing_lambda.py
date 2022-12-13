import json
import logging
import uuid
import random
import string
import time

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    print("Random string of length", length, "is:", result_str)
    return result_str
    
    
def lambda_handler(event, context):
    # TODO implement
    
    output_event = event
    logger.info(f"event : {json.dumps(event)}") 
    time.sleep(5)
    
    output_event['execution_id'] = str(uuid.uuid4())
    output_event['info'] = [get_random_string(5) for x in range(0, random.randint(0,10))]
    output_event['status_code'] = 200
    
    return output_event
