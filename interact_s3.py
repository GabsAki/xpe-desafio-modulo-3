import boto3
import os

env_var = os.environ

DATA_PATH = env_var["DATA_PATH"]
TF_VAR_s3_bucket_name = env_var["TF_VAR_s3_bucket_name"]

session = boto3.Session(profile_name='gabs_study')
s3_client = session.client("s3")

if __name__ == "__main__":

    for path in os.scandir(DATA_PATH):

        s3_client.upload_file(
            DATA_PATH + "/" + path.name, TF_VAR_s3_bucket_name, "zona_raw/enade/" + path.name
        )
