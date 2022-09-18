import base64


def get_encrypted_password(password):
    """
    encode password

    :param password: Password as a plain text
    :return:  Password as a cypher text
    """
    return base64.b64encode(password.encode('ascii')).decode('utf-8')
