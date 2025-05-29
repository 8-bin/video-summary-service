import boto3
import json

# Bedrock 클라이언트 생성
bedrock = boto3.client('bedrock-runtime', region_name='ap-northeast-2')

def call_bedrock(prompt, max_tokens=1000):
    body_payload = {
        "anthropic_version": "bedrock-2023-05-31",  # ✅ 반드시 포함!
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": max_tokens
    }

    response = bedrock.invoke_model(
        modelId='anthropic.claude-3-5-sonnet-20240620-v1:0',
        body=json.dumps(body_payload).encode('utf-8'),
        contentType='application/json'
    )

    # 응답 본문 파싱
    response_body = response['body'].read().decode('utf-8')
    response_json = json.loads(response_body)

    # Claude 응답에서 content 배열 꺼내기
    if 'content' in response_json:
        return ''.join(part['text'] for part in response_json['content'])
    else:
        return "⚠️ Claude 응답에 content 필드가 없습니다."
