# AWS Lambda Function for CV Summary Generation

This AWS Lambda function generates a summary of a CV using the Anthropic Claude-3 Sonnet model from AWS Bedrock. The function receives CV text, processes it, and returns a brief summary.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Deployment](#deployment)
- [Usage](#usage)
- [Logging](#logging)
- [Error Handling](#error-handling)
- [License](#license)

## Overview

This Lambda function leverages AWS Bedrock to generate concise summaries of CVs. The Bedrock service provides access to state-of-the-art language models that are capable of understanding and generating human-like text.

## Prerequisites

Before you begin, ensure you have the following:

- An AWS account with necessary permissions to create and manage Lambda functions and access AWS Bedrock.
- AWS CLI configured on your local machine.
- Python 3.7 or later installed.

## Setup

### Install Dependencies

1. **Clone the repository** (or create a directory for your Lambda function):
    ```bash
    git clone https://github.com/yourusername/lambda-cv-summary.git
    cd lambda-cv-summary
    ```

2. **Install necessary Python packages**:
    ```bash
    pip install boto3
    ```

### Create IAM Role

1. **Create an IAM role** with the following permissions:
    - AWS Lambda basic execution role.
    - Permissions to invoke the Bedrock model.
    - Permissions to write logs to CloudWatch.

    Example policy for Bedrock:
    ```json
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Effect": "Allow",
          "Action": "logs:*",
          "Resource": "arn:aws:logs:YOUR_REGION:YOUR_ACCOUNT_ID:*"
        },
        {
          "Effect": "Allow",
          "Action": "bedrock:InvokeModel",
          "Resource": "*"
        }
      ]
    }
    ```

## Deployment

### Create and Deploy Lambda Function

1. **Create a zip file** of the Lambda function:
    ```bash
    zip -r function.zip .
    ```

2. **Deploy the Lambda function** using the AWS CLI:
    ```bash
    aws lambda create-function --function-name GenerateCVSummary \
        --runtime python3.8 --role arn:aws:iam::YOUR_ACCOUNT_ID:role/YOUR_LAMBDA_ROLE \
        --handler lambda_function.lambda_handler --zip-file fileb://function.zip
    ```

3. **Update function code** (for future updates):
    ```bash
    aws lambda update-function-code --function-name GenerateCVSummary \
        --zip-file fileb://function.zip
    ```

### Configure Environment Variables

Set the necessary environment variables for your Lambda function through the AWS Management Console or AWS CLI:

1. Go to your Lambda function in the AWS Management Console.
2. Click on "Configuration".
3. Select "Environment variables" and add the following:
    - `MODEL_ID`: `anthropic.claude-3-sonnet-20240229-v1:0`
    - `AWS_REGION`: `ap-southeast-2`

## Usage

### Sending Requests

To send a request to the Lambda function, use an HTTP client or invoke it directly through AWS services. Here's an example using `curl`:

```bash
curl -X POST https://YOUR_API_GATEWAY_URL/GenerateCVSummary \
    -H "Content-Type: application/json" \
    -d '{"cv_text": "Your CV text goes here..."}'
```

### Expected Response

The function will return a JSON response containing the summary:

```json

{
    "statusCode": 200,
    "body": "\"5 years of experience as a Business Analyst with NSW Department of Education, ...\""
}
```

### Logging
The function logs detailed information about incoming requests and errors to AWS CloudWatch. You can view these logs by navigating to the CloudWatch service in the AWS Management Console.

### Example Log Output

```Event Logging: Logs the entire incoming event for debugging.
Body Content: Logs raw and parsed body content.
Generated Summary: Logs the generated summary text.
Error Handling
The Lambda function includes robust error handling to manage common issues such as:

Invalid JSON: Returns a 400 status code with a message "Invalid JSON body".
Missing CV Text: Returns a 400 status code with a message "No CV text provided".
Model Invocation Error: Returns a 500 status code with details of the error.
```
# License
This project is licensed under the MIT License. See the LICENSE file for more details.

