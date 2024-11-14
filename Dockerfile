# Use the official Amazon Linux 2 image for AWS Lambda functions
FROM public.ecr.aws/lambda/python:3.8

# Install required packages
RUN pip install boto3

# Copy the application code to the container
COPY . ${LAMBDA_TASK_ROOT}

# Set environment variables (optional)
ENV DYNAMODB_TABLE_NAME=ImageMetadata

# Command to run the Lambda function handler
CMD ["lambda_function.lambda_handler"]
