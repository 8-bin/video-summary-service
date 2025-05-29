def run_transcribe(s3_uri):
    import boto3
    import time
    import uuid
    import requests

    transcribe = boto3.client('transcribe')

    # ✅ 매번 유니크한 job 이름 생성
    job_name = f"youtube-transcribe-job-{uuid.uuid4()}"

    transcribe.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': s3_uri},
        MediaFormat='mp4',
        LanguageCode='ko-KR'
    )

    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        time.sleep(10)

    if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
        transcript_file_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        response = requests.get(transcript_file_uri)
        transcript_json = response.json()
        return transcript_json['results']['transcripts'][0]['transcript']
    else:
        return "Transcription failed."
