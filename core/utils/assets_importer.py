def qrcImage(name: str, extension: str = 'png'):
    """
    returns a string of the name of the qrc component we want
    :param name:
    :param extension:
    :return:
    """

    return f":/images/{name}.{extension}"
