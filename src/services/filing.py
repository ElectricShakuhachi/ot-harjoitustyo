import json
from json.decoder import JSONDecodeError
from tkinter import filedialog
import boto3
from botocore.exceptions import NoCredentialsError
from svgwrite import Drawing
from PIL import Image
from midiutil import MIDIFile
import config.shaku_constants as consts

class FileManager:
    """Class handling saving, loading and uploading files"""
    def save_shaku(self, data: dict, filename=None):
        """Promtps user with file dialog and saves file into .shaku -format if file was specified

        Args:
            data (dict): [description]

        Returns:
            True if file was saved, else False
        """
        if filename is not None:
            with open(filename, "w") as file:
                json.dump(data, file, indent=4)
            return True
        else:
            try:
                with filedialog.asksaveasfile(mode='w', defaultextension=".shaku") as file:
                    json.dump(data, file, indent=4)
                return file.name
            except AttributeError:
                return False

    def load(self):
        """Promtps user with file dialog, and loads file from .shaku -format if file was specified

        Returns:
            Loaded JSON data, if any was loaded, else None
        """
        try:
            with filedialog.askopenfile(mode='r', defaultextension=".shaku") as file:
                data = json.load(file)
            return data
        except JSONDecodeError:
            return "JSON Error"
        except AttributeError:
            return None

    def save_pdf(self, image: Image):
        """Promtps user with file dialog and exports file into .pdf -format if file was specified

        Args:
            image (Image): [description]

        Returns:
            True if file was exported to PDF, else False
        """
        try:
            with filedialog.asksaveasfile(mode='wb', defaultextension=".pdf") as file:
                image.save(file, format="pdf")
            return True
        except AttributeError:
            return False

    def save_svg(self, svg: Drawing):
        """Promtps user with file dialog and exports file into .svg -format if file was specified

        Args:
            svg (Drawing): [description]

        Returns:
            True if file was exported to SVG, else False
        """
        try:
            with filedialog.asksaveasfile(mode='w', defaultextension=".svg") as file:
                svg.write(file, indent=2, pretty=False)
            return True
        except AttributeError:
            return False

    def save_midi(self, midi: MIDIFile, name: str=None):
        """Exports file into .mid -format if file is specified

        Args:
            midi: MIDI -format data
            name: Filename to be used. Defaults to None.

        Returns:
            True if file was exported to MIDI, else False
        """
        if name:
            with open(name, "wb") as file:
                midi.writeFile(file)
            return True
        try:
            with filedialog.asksaveasfile(mode="wb", defaultextension=".mid") as file:
                midi.writeFile(file)
            return True
        except AttributeError:
            return False

    def upload_to_aws_s3(self, data: dict, name: str):
        """Uploads .shaku -format (JSON) -data to AWS S3 -bucket

        Args:
            data: JSON format data
            name: filename

        Returns:
            True if file was uploaded to AWS S3, else False
        """
        try:
            client = boto3.client('s3')
            bucket = consts.AWS_S3_BUCKET
            body=json.dumps(data)
            client.put_object(Body=body, Bucket=bucket, Key=name)
            return True
        except NoCredentialsError:
            return False
