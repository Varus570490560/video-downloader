import configparser


def get_path():
    cf = configparser.ConfigParser()
    cf.read('./config/config.ini')
    return cf.get('position', 'path')
