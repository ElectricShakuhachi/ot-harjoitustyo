import boto3
from botocore.exceptions import NoCredentialsError
import json
from tkinter import filedialog
from entities.svg_creator import SvgCreator
from svgwrite import Drawing

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

    def save_svg(self, svg):
        with filedialog.asksaveasfile(mode='w', defaultextension=".svg") as file:
            svg.write(file, indent=2, pretty=False)

    def save_midi(self, midi, name=None):
        if name:
            with open(name, "wb") as file:
                midi.writeFile(file)
        else:
            with filedialog.asksaveasfile(mode="wb", defaultextension=".mid") as file:
                midi.writeFile(file)

    def upload_to_aws_s3(self, data, name):
        try:
            client = boto3.client('s3')
            bucket = "shakunotator"
            body=json.dumps(data)
            client.put_object(Body=body, Bucket=bucket, Key=name)
            return True
        except NoCredentialsError:
            return False