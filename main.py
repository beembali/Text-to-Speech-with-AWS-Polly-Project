# Too tired to read? This python script takes a PDF file, identifies the
# text and converts the text to speech. Effectively creating a free audiobook.

# Chosen Text to Speech API
# https://aws.amazon.com/polly/

# Importing required classes
from pypdf import PdfReader
import boto3
from botocore.exceptions import NoCredentialsError
import os
import sys

# AWS Credentials for IAM User
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_default_region = os.getenv('AWS_DEFAULT_REGION')


# Get the PDF file

# Creating a pdf reader object
reader = PdfReader('a_kitchen_in_rome.pdf')
# Creating a page object
page = reader.pages[0]
# Extract text from page
text = page.extract_text()


# Pass the text to the API to convert text to speech and save file
try:
    # Retrieve envrionment variables
    session = boto3.Session(aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_default_region)

    if not aws_access_key_id or not aws_secret_access_key or not aws_default_region:
        raise NoCredentialsError

    # Create a client using the credentials for the AWS IAM user
    polly = session.client("polly")
    # Request speech synthesis
    response = polly.synthesize_speech(Text=text, OutputFormat="mp3",
                                        VoiceId="Joanna")


    # Access the audio stream from the response
    if "AudioStream" in response:
        file_name = 'voice.mp3'
        body = response['AudioStream'].read()
        try:
            # Save the audio to a file
            with open(file_name, "wb") as file:
                file.write(body)
                file.close()
        except IOError as error:
            # Could not write to file, exit gracefully
            print(error)
            sys.exit(-1)
    else:
        # The response didn't contain audio data, exit gracefully
        print("Could not stream audio")
        sys.exit(-1)

except NoCredentialsError as error:
    print("Credentials not available. Please check your AWS configuration.")
    print(error)