# AWS Polly project

This project display the text to speech conversion abilities of aws polly. It uses amazon polly to conver text to speech, then uploads the mp3 audio file to an s3 bucket. The s3 url of the audio file is fed in the audio html tag which uses it as a source. This project supports only indian english and hindi and only two voice ids Aditi and Kajal You can add more as per your need.

After creating the function add the function url or the api gateway url in the index.html file.