"""Module containing the AWS S3 demonstration."""
import datetime
import json
import os

import boto3


def main() -> None:
    """Execute the main process."""

    project_path = os.path.sep.join(__file__.split(os.path.sep)[:-1])
    secrets_file = os.path.join(project_path, "secrets", "creds.json")

    with open(secrets_file, "r") as file:
        creds = json.load(file)

    client_kwargs = {
        "aws_access_key_id": creds["id"],
        "aws_secret_access_key": creds["secret"]
    }

    client = boto3.resource("s3", **client_kwargs)

    bucket_name = creds["bucket"]
    bucket = client.Bucket(bucket_name)

    stamp = datetime.datetime.now().strftime("%y-%m-%d_%H-%M-%S")

    local_filename = f"{stamp}_testfile.txt"
    download_path = "samples/file_1.txt"
    upload_path = f"upload/{stamp}_testfile.txt"

    with open(local_filename, "wb") as file:
        bucket.download_fileobj(download_path, file)

    print("Downloaded file successfully from S3 bucket.")

    with open(local_filename, "rb") as file:
        bucket.upload_fileobj(file, upload_path)

    print("Uploaded file successfully to S3 bucket.")

    os.remove(local_filename)


if __name__ == "__main__":
    main()
