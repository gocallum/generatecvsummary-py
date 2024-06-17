import json
import boto3
import logging

# Setup logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Log the entire incoming event for debugging
    logger.info(f"Received event: {json.dumps(event)}")
    
    # Extract and log the body field
    body = event.get('body', '{}')
    logger.info(f"Raw body content: {body}")
    
    try:
        # Parse the body as JSON
        parsed_body = json.loads(body)
        logger.info(f"Parsed body content: {json.dumps(parsed_body)}")
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse body as JSON: {str(e)}")
        return {
            'statusCode': 400,
            'body': json.dumps('Invalid JSON body')
        }

    # Extract CV text from the parsed body
    cv_text = parsed_body.get('cv_text', '')
    
    # Log the extracted CV text
    logger.info(f"Extracted cv_text: '{cv_text}'")
    
    if not cv_text:
        logger.warning("No CV text provided in the request.")
        return {
            'statusCode': 400,
            'body': json.dumps('No CV text provided')
        }
    
    # System prompt
    system_prompt = (
        "generate a summary based on CV below in the format eg "
        "\"3 years of experience as a {Role} with {list of companies worked at} "
        "followed by brief list of projects or types of projects, and in just 1 sentence. "
        "based on the following CV: "
    )
    
    # Construct the request body for Bedrock
    request_body = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{system_prompt}{cv_text}"
                    }
                ]
            }
        ],
        "anthropic_version": "bedrock-2023-05-31",  # Required key
        "system": system_prompt,
        "max_tokens": 1000,
        "top_k": 250,
        "top_p": 0.999,
        "stop_sequences": ["\n\nHuman:"]
    }
    
    # Log the constructed request body
    logger.info(f"Constructed request body for Bedrock: {json.dumps(request_body)}")
    
    # Initialize Bedrock client
    client = boto3.client('bedrock-runtime', region_name='ap-southeast-2')
    
    try:
        # Invoke the Bedrock model
        response = client.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            body=json.dumps(request_body),
            contentType='application/json'
        )
        
        # Parse the model's response
        response_body = response['body'].read().decode()
        result = json.loads(response_body)
        
        # Log the response from the model
        logger.info(f"Model Response: {json.dumps(result)}")
        
        # Extract the summary from the response
        content_list = result.get('content', [])
        summary = next((item['text'] for item in content_list if item['type'] == 'text'), 'No summary generated')
        
        logger.info(f"Generated summary: '{summary}'")
        
        return {
            'statusCode': 200,
            'body': json.dumps(summary)
        }
        
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}", exc_info=True)
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error generating summary: {str(e)}")
        }
