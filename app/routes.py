from app import id_digitizer,  DEBUG
from flask import render_template, request, flash, jsonify, redirect, url_for, json
from app.db_access import get_user_info, put_user_info, delete_user_info
import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from werkzeug.utils import secure_filename


def send_post_request(addr, data):
    """
    Helper function to send POSt request that doesn't require a
    full hreaders
    :param addr: srt: request receiver url
    :param data: dict
    :return:
    """
    try:
        r = requests.post(addr, data=data)
    except requests.exceptions.RequestException as e:
        print("Warning: Exception happened when sending the request")
        if DEBUG is True:
            print(e)


def send_post_request_with_body(addr, params):
    """
    Helper function to send POSt request that require a full
    hreaders
    :param addr: srt: request receiver url
    :param params: dict
    :return:
    """
    data = MultipartEncoder(fields=params)
    headers = {
        'Content-type': data.content_type
    }
    try:
        r = requests.post(addr, data=data, headers=headers)
    except requests.exceptions.RequestException as e:
        print("Warning: Exception happened when sending the request")
        if DEBUG is True:
            print(e)


@id_digitizer.route('/')
def main_page():
    """
    wait user to upload an image
    :return:
    """
    return render_template('main.html')


@id_digitizer.route('/upload', methods=['GET', 'POST'])
def upload_page():
    """
    got an image from user
    :return:
    """
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(id_digitizer.config['IMAGE_PATH'], f.filename))  # for debugging only
        # TODO: upload image to S3 bucket here
        if DEBUG:
            print('Image Received!')
    return render_template('main.html')


@id_digitizer.route('/management', methods=['GET', 'POST'])
def management_page():
    """
    display all existing users in database
    :return:
    """
    rows = get_user_info()
    return render_template('management.html', rows=rows)


@id_digitizer.route('/rds_ops/<id_num>', methods=['GET', 'POST'])
def rds_ops(id_num):
    """
    remove a user by id_num from database
    :param id_num:
    :return:
    """
    delete_user_info(id_num)
    rows = get_user_info()
    return render_template('management.html', rows=rows)
