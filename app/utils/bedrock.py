def call_bedrock(prompt):
    import boto3
    bedrock = boto3.client('bedrock-runtime')
    
    response = bedrock.invoke_model(
        modelId='anthropic.claude-v2',
        body={
            "prompt": prompt,
            "max_tokens_to_sample": 500
        }
    )
    return response['completion']