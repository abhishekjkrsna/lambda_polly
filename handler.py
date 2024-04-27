import boto3
import uuid
import json

# Initialize clients
polly_client = boto3.client("polly")
s3_client = boto3.client("s3")

# s3 bucket
bucket = "Enter your bucket name here"

def validate_request(event):
    """Validate the request body."""
    try:
        body = event.get("body", False)
        if not body:
            return False, {"message": "Body is missing in the request."}
        text = json.loads(body).get("text", False)
        if not text:
            return False, {
                "message": "Request body must include a 'text' key with a string value."
            }
        lang_code = json.loads(body).get("lang_code", False)
        if not lang_code or lang_code not in ["hi-IN", "en-IN"]:
            return False, {"message": "Missing or Invalid language code."}

        voice_id = json.loads(body).get("voice_id", False)
        if not voice_id or voice_id not in ["Aditi", "Kajal"]:
            return False, {"message": "Missing or Invalid Voice ID."}

        if voice_id == "Kajal":
            engine = "neural"
        else:
            engine = "standard"

        return True, {
            "text": text,
            "lang_code": lang_code,
            "voice_id": voice_id,
            "engine": engine,
        }
    except Exception as e:
        return False, {"message": str(e)}


def lambda_handler(event, context):
    """Synthesize speech using Amazon Polly and upload to S3."""
    try:

        valid, message = validate_request(event)
        if not valid:
            return {
                "statusCode": 400,
                "body": json.dumps(message),
            }

        text = message["text"]
        lang_code = message["lang_code"]
        voice_id = message["voice_id"]
        engine = message["engine"]

        # Synthesize speech using Amazon Polly
        response = polly_client.synthesize_speech(
            Engine=engine,
            LanguageCode=lang_code,
            OutputFormat="mp3",
            Text=text,
            VoiceId=voice_id,  # Replace with your desired voice
        )

        # Generate a unique filename
        filename = f"{uuid.uuid4()}.mp3"

        # Upload audio to S3
        s3_response = s3_client.put_object(
            Body=response["AudioStream"].read(),
            Bucket=bucket,  # Replace with your bucket name
            Key=filename,
        )

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "url": f"https://{bucket}.s3.ap-south-1.amazonaws.com/{filename}",
                }
            ),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"message": str(e)}),
        }
