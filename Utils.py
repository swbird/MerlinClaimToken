import re
import hashlib
import sys

from loguru import logger

md5 = lambda x: hashlib.md5(x.encode('utf-8')).hexdigest()

def error_handler(func):
    def wrapper(*args, **kwargs):
        error_count = 0
        while True:
            try:
                print(f'通过筛选-> {func.__name__},{args},{kwargs}')
                return func(*args, **kwargs)
            except Exception as e:
                error_count += 1
                logger.debug(f"ERROR -> function: {func.__name__} => {e}")
                if error_count >= 30:
                    logger.debug(f'ERROR -> function: {func.__name__} => {e}, 因出现致命错误,程序停止')
                    sys.exit(0)


    return wrapper

class regex:
    def __init__(self):
        pass

    @staticmethod
    # @error_handler
    def addressRegex():
        return re.compile(r'(0x[A-Fa-f0-9]{40})[^A-Fa-f0-9]+') # 仅匹配地址 不匹配私钥
    @staticmethod
    def privateKeyRegex():
        return re.compile(r'(0x[A-Fa-f0-9]{64})')
    @staticmethod
    def idRegex():
        return re.compile(r'----([0-9]{1,8})\n')
@error_handler
def load_from_file_pro(filename=''):
    with open(filename, encoding='utf-8') as f:
        result = f.read()
    addresses = regex.addressRegex().findall(result)
    privateKeys = regex.privateKeyRegex().findall(result)
    return addresses, privateKeys

@error_handler
def load_from_file_pro_plus(filename=''):
    with open(filename, encoding='utf-8') as f:
        result = f.read()
    addresses = regex.addressRegex().findall(result)
    privateKeys = regex.privateKeyRegex().findall(result)
    ids = regex.idRegex().findall(result)
    return addresses, privateKeys, ids





if __name__ == '__main__':

   pass