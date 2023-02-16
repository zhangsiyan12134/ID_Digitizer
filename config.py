import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    IMAGE_PATH = '/home/siyan/Documents/ECE1779/Assignment_3/ID_Digitizer/image_library'    # for debug only
    AWS_LAMBDA_API = 'https://a61curyqmd.execute-api.us-east-1.amazonaws.com/dev/gettextfromimage'
    AWS_LAMBDA_KEY = ''
    DROPZONE_UPLOAD_ON_CLICK = True
    DROPZONE_MAX_FILE_SIZE = 3
    DROPZONE_MAX_FILES = 1
    DROPZONE_UPLOAD_MULTIPLE = False
    DROPZONE_PARALLEL_UPLOADS = 1
    ASW_CONFIG = {
        'REGION': 'us-east-1',
        'AWS_ACCESS_KEY_ID': '',
        'SECRET_ACCESS_KEY': ''
    }
    RDS_CONFIG = {
        'host': '',
        'port': 3306,
        'user': 'r',
        'password': '',
        'database': 'ECE1779'
    }
