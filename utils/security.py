import base64


def get_encrypted_password(password):
    return base64.b64encode(password.encode('ascii')).decode('utf-8')
