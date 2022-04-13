import requests, base64
from app import id_digitizer,  DEBUG


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
    headers = {
        'Content-type': 'text/plain',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'x-api-key': id_digitizer.config['AWS_LAMBDA_KEY']
    }
    try:
        r = requests.post(addr, json=params, headers=headers)
        print(r)
        return r.json()
    except requests.exceptions.RequestException as e:
        print("Warning: Exception happened when sending the request")
        if DEBUG is True:
            print(e)


def send_image_to_lambda(image, id_num=''):
    """
    encode and send a image to lambda function for Textrect
    :param image: image file
    :return:
    """
    params = {
        "Image": base64.b64encode(image.read()).decode('utf-8'),
        "Id_num": id_num
    }
    text = send_post_request_with_body(id_digitizer.config['AWS_LAMBDA_API'], params)
    return text
