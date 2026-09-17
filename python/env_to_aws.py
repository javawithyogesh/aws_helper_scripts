import os
import boto3
from botocore.exceptions import ClientError
from dotenv import dotenv_values

# --- Configuration ---
ENV_FILE = ".env"
APP_NAME = "my-app"
ENVIRONMENT = "prod"  # e.g., dev, staging, prod
PARAMETER_TYPE = "SecureString"  # Use 'SecureString' for secrets, 'String' for public config
AWS_REGION = "us-east-1"  # Change to your target AWS region

def bulk_upload_to_ssm():
    # 1. Check if the .env file exists
    if not os.path.exists(ENV_FILE):
        print(f"Error: {ENV_FILE} file not found!")
        return

    # 2. Parse the .env file cleanly (handles comments, quotes, and empty lines automatically)
    config = dotenv_values(ENV_FILE)
    if not config:
        print("No variables found to upload.")
        return

    # 3. Initialize the AWS SSM Client
    ssm_client = boto3.client('ssm', region_name=AWS_REGION)
    
    print(f"Starting bulk upload of {len(config)} variables to AWS Parameter Store...\n")

    # 4. Iterate and upload each key-value pair
    for key, value in config.items():
        # Build a structured, hierarchical parameter path
        param_name = f"/{APP_NAME}/{ENVIRONMENT}/{key}"
        
        try:
            print(f"Uploading: {param_name}")
            ssm_client.put_parameter(
                Name=param_name,
                Value=value,
                Type=PARAMETER_TYPE,
                Overwrite=True
            )
            print(f"✅ Successfully uploaded {key}")
        except ClientError as e:
            print(f"❌ Failed to upload {key}. Error: {e.response['Error']['Message']}")

    print("\nBulk upload complete!")

if __name__ == "__main__":
    bulk_upload_to_ssm()