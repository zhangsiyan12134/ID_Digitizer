from flask import Flask
from config import Config
from flask_dropzone import Dropzone
import boto3

id_digitizer = Flask(__name__)

global DEBUG

DEBUG = True

cloudwatch_client = boto3.client(
        'cloudwatch',
        region_name=Config.ASW_CONFIG['REGION'],
        aws_access_key_id=Config.ASW_CONFIG['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=Config.ASW_CONFIG['SECRET_ACCESS_KEY']
    )

ec2_client = boto3.client(
        'ec2',
        region_name=Config.ASW_CONFIG['REGION'],
        aws_access_key_id=Config.ASW_CONFIG['AWS_ACCESS_KEY_ID'],
        aws_secret_access_key=Config.ASW_CONFIG['SECRET_ACCESS_KEY']
    )

id_digitizer.config.from_object(Config)

id_digitizer.config.update(
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=30,
)

dropzone = Dropzone(id_digitizer)

from app import routes
