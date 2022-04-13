from flask import g
from app import id_digitizer, DEBUG, s3_client


def get_user_face(id_num):
    """
    delete the given user by id_num
    :return:
    """
    response = s3_client.get_object(
        Bucket='1779test',
        Key=id_num
    )
    return response
