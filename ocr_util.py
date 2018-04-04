from aip import AipOcr

# 认证信息
APP_ID = ''
API_KEY = 'b52a2d05d6c644518b15d747e795b78c'
SECRET_KEY = 'ceb97436c7e046468dd578db104c6025'


def get_ocr_str(file_path, origin_format=True):
    """
    图片转文字
    :param file_path:
    :return:
    """
    with open(file_path, 'rb') as fp:
        file_bytes = fp.read()
    return get_ocr_str_from_bytes(file_bytes, origin_format)


def get_ocr_str_from_bytes(file_bytes, origin_format=True):
    """
    图片转文字
    :param file_bytes:
    :return:
    """
    options = {
        'detect_direction': 'false',
        'language_type': 'CHN_ENG',
    }
    ocr = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    result_dict = ocr.basicGeneral(file_bytes, options)
    if origin_format:
        result_str = '\n'.join([entity['words'] for entity in result_dict['words_result']])
    else:
        result_str = ''.join([entity['words'] for entity in result_dict['words_result']])
    return result_str


if __name__ == '__main__':
    IMAGE_PATH = "test.jpg"
    print(get_ocr_str(IMAGE_PATH))
