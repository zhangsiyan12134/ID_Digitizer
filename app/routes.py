from app import id_digitizer, DEBUG
from flask import render_template, request, flash, jsonify, redirect, url_for, json
from app.db_access import get_user_info, put_user_info, delete_user_info
from app.lambda_access import send_image_to_lambda
import os
from datetime import datetime
from dateutil import parser
from werkzeug.utils import secure_filename
import base64
from config import Config

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
        response = send_image_to_lambda(f)
        userdata = response
        # put_user_info(response['student_id'],
        #               response['first_name'],
        #               response['last_name'],
        #               response['issue_date'])
        # image_path = os.path.join(Config.IMAGE_PATH, f.filename)
        # f.save(image_path)  # for debugging only
        # with open(image_path, "rb") as image:
        #     userdata = send_image_to_lambda(image).split('\n')
        #
        # # !!MUST Reopen b/c doesn't read properly somehow if it's encoded first
        # with open(image_path, 'rb') as img:
        #     img_64 = base64.b64encode(img.read()).decode('utf-8')
        #     # print(img_64)
        #     try:
        #         s3.put_object(Bucket='1779test', Key=str(Config.s3_counter), Body=img_64)
        #         Config.s3_counter += 1
        #     except Exception as e:
        #         print(e)
        #
        # if DEBUG:
        #     print('Image Received!')
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
        student_id = userdata['student_id']
        first_name = userdata['first_name']
        last_name = userdata['last_name']

        flash('User ' + last_name + ' ' + first_name + ' added!')
        # datetime_obj = parser.parse(userdata[8])
        put_user_info(student_id, first_name, last_name)
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


@id_digitizer.route('/db_del/<id_num>', methods=['GET', 'POST'])
def db_del(id_num):
    """
    remove a user by id_num from database
    :param id_num:
    :return:
    """
    delete_user_info(id_num)
    rows = get_user_info()
    return render_template('management.html', rows=rows)


@id_digitizer.route('/db_add/', methods=['GET', 'POST'])
def db_add():
    """
    add a user manually to database
    :param id_num:
    :return:
    """
    id_num = request.form.get('id_num')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    issue_date = request.form.get('issue_date')
    put_user_info(id_num, first_name, last_name)
    return redirect(url_for('management_page'))


# Route for upload image
@id_digitizer.route('/test_upload', methods=['GET', 'POST'])
def test_upload_page():
    """
    got an image from user
    :return:
    """
    if request.method == 'POST':
        global userdata
        f = request.files['file']
        response = send_image_to_lambda(f)
        print(response)
    return redirect(url_for('get_result'))
