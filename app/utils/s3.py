def upload_to_s3(file_path):
    import boto3
    s3 = boto3.client('s3')
    bucket_name = "smry-demo" 
    s3_key = "uploads/output.mp4"
    s3.upload_file(file_path, bucket_name, s3_key)
    return f"s3://{bucket_name}/{s3_key}"
