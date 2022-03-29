from app import id_digitizer, DEBUG
from flask import render_template, request, flash, jsonify, redirect, url_for, json
from app.db_access import get_user_info, put_user_info, delete_user_info
from app.lambda_access import send_image_to_lambda
import os
from datetime import datetime
from werkzeug.utils import secure_filename

global userdata
userdata = list()

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
        global userdata
        f = request.files.get('file')
        image_path = os.path.join(id_digitizer.config['IMAGE_PATH'], f.filename)
        f.save(image_path)  # for debugging only
        with open(image_path, "rb") as image:
            userdata = send_image_to_lambda(image).split('\n')
        # TODO: upload image to S3 bucket here
        if DEBUG:
            print('Image Received!')
    return redirect(url_for('get_result'))


@id_digitizer.route('/receive', methods=['GET', 'POST'])
def get_result():
    """
    listen to the result from Textract in Lambda function
    :return:
    """
    global userdata
    if not userdata:
        flash('Text Recognition Failed!')
    else:
        flash('User ' + userdata[3] + ' ' + userdata[2] + ' added!')
        put_user_info(userdata[4], userdata[3], userdata[2], datetime.strptime(userdata[8], '%d-%B-%Y'))
        if DEBUG:
            print('Response Received!')
            print(userdata)
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
