#!/bin/bash
set -e

# Initialize S3/MinIO storage
echo "Initializing storage..."
python << END
import os
import sys
import boto3
import botocore

# Get storage settings from environment
endpoint_url = os.environ.get('STORAGE_URL')
bucket_name = os.environ.get('STORAGE_BUCKET', 'image-service')
access_key = os.environ.get('STORAGE_ACCESS_KEY')
secret_key = os.environ.get('STORAGE_SECRET_KEY')

if not all([endpoint_url, access_key, secret_key]):
    print("Storage configuration not found. Using default filesystem storage.")
    sys.exit(0)

try:
    # Create S3 client
    s3 = boto3.client(
        's3',
        endpoint_url=endpoint_url,
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )

    # Create bucket if it doesn't exist
    try:
        s3.create_bucket(Bucket=bucket_name)
        print(f"Created bucket: {bucket_name}")
    except botocore.exceptions.ClientError as e:
        error_code = e.response.get("Error", {}).get("Code")
        if error_code == "BucketAlreadyOwnedByYou":
            print(f"Bucket already exists: {bucket_name}")
        else:
            raise e

    # Enable versioning
    s3.put_bucket_versioning(
        Bucket=bucket_name,
        VersioningConfiguration={'Status': 'Enabled'}
    )
    print("Enabled bucket versioning")

    # Set lifecycle rules
    s3.put_bucket_lifecycle_configuration(
        Bucket=bucket_name,
        LifecycleConfiguration={
            'Rules': [
                {
                    'ID': 'DeleteOldVersions',
                    'Status': 'Enabled',
                    'NoncurrentVersionExpiration': {'NoncurrentDays': 30}
                },
                {
                    'ID': 'DeleteOldGenerations',
                    'Status': 'Enabled',
                    'Expiration': {'Days': 30},
                    'Filter': {'Prefix': 'generations/'}
                }
            ]
        }
    )
    print("Set lifecycle rules")

except Exception as e:
    print(f"Error initializing storage: {e}")
    sys.exit(1)
END