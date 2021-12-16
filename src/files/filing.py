import boto3
from botocore.exceptions import NoCredentialsError
import json
from tkinter import filedialog
import svgwrite

class FileManager:
    def save_shaku(self, data):
        with filedialog.asksaveasfile(mode='w', defaultextension=".shaku") as file:
            json.dump(data, file, indent=4)

    def load(self):
        with filedialog.askopenfile(mode='r', defaultextension=".shaku") as file:
            data = json.load(file)
            return data

    def save_pdf(self, image):
        with filedialog.asksaveasfile(mode='wb', defaultextension=".pdf") as file:
            image.save(file, format="pdf")

    def save_svg(self, music):
        with filedialog.asksaveasfile(mode='wb', defaultextension=".svg") as file:
            pass

    def upload_to_aws_s3(self, data, name):
        try:
            client = boto3.client('s3')
            bucket = "shakunotator"
            body=json.dumps(data)
            client.put_object(Body=body, Bucket=bucket, Key=name)
            return True
        except NoCredentialsError:
            return False