import base64
from Crypto.Cipher import AES
from Crypto import Random
import json
import MarketDb


class AESCipher:
    def __init__(self):
        '''
        CBC加密需要一个十六位的key(密钥)和一个十六位iv(偏移量)
        '''
        self.key = self.check_key('1111222233334444')
        # 数据块的大小  16位
        self.BS = 16
        # CBC模式 相对安全 因为有偏移向量 iv 也是16位字节的
        self.mode = AES.MODE_CBC
        # 填充函数 因为AES加密是一段一段加密的  每段都是BS位字节，不够的话是需要自己填充的
        self.pad = lambda s: s + (self.BS - len(s.encode()) % self.BS) * chr(self.BS - len(s.encode()) % self.BS)
        # 将填充的数据剔除
        self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    def check_key(self, key):
        '''
        检测key的长度是否为16,24或者32bytes的长度
        '''
        try:
            if isinstance(key, bytes):
                assert len(key) in [16, 24, 32]
                return key
            elif isinstance(key, str):
                assert len(key.encode()) in [16, 24, 32]
                return key.encode()
            else:
                raise Exception(f'密钥必须为str或bytes,不能为{type(key)}')
        except AssertionError:
            print('输入的长度不正确')

    def check_data(self, data):
        '''
        检测加密的数据类型
        '''
        if isinstance(data, int):
            data = str(data)
        elif isinstance(data, bytes):
            data = data.decode()
        elif isinstance(data, str):
            pass
        else:
            raise Exception(f'加密的数据必须为str或bytes,不能为{type(data)}')
        return data

    def encrypt(self, raw):
        raw = self.check_data(raw)
        raw = self.pad(raw).encode()
        # 随机获取iv
        iv = Random.new().read(AES.block_size)
        # 定义初始化
        cipher = AES.new(self.key, self.mode, iv)
        # 此处是将密文和iv一起 base64 解密的时候就可以根据这个iv来解密
        return base64.b64encode(iv + cipher.encrypt(raw)).decode()

    def decrypt(self, enc):
        # 先将密文进行base64解码
        enc = base64.b64decode(enc)
        # 取出iv值
        iv = enc[:self.BS]
        # 初始化自定义
        cipher = AES.new(self.key, self.mode, iv)
        # 返回utf8格式的数据
        return self.unpad(cipher.decrypt(enc[self.BS:])).decode()


def encrypt(params):
    aes = AES.new("1111222233334444", AES.MODE_CBC)
    en_text = aes.encrypt(params)
    print(en_text)


def AES_Encrypt(key, data):
    vi = '0102030405060708'
    pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
    data = pad(data)
    # 字符串补位
    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, vi.encode('utf8'))
    encryptedbytes = cipher.encrypt(data.encode('utf8'))
    # 加密后得到的是bytes类型的数据
    encodestrs = base64.b64encode(encryptedbytes)
    # 使用Base64进行编码,返回byte字符串
    enctext = encodestrs.decode('utf8')
    # 对byte字符串按utf-8进行解码
    return enctext


def encrypt_1(data, key):
    """
    加密时使用的key，只能是长度16,24和32的字符串
    data: 要加密的内容，bytes
    key：密钥，len必须是16, 24, 32之一 bytes
    result：加密内容，bytes
    """
    keySzie = len(key)
    if keySzie == 16 or keySzie == 24 or keySzie == 32:
        cipher = AES.new(key, AES.MODE_ECB)
        padData = _padData(data)
        encrypted = cipher.encrypt(padData)
        result = base64.b64encode(encrypted)
        return result
    else:
        # 加密失败，返回原数据
        return data


def _padData(data):
    """
    按AES加密的要求，填充内容，使其为block_size的整数倍
    """
    block_size = 16
    padding = b"\0"
    padData = data + (block_size - len(data) % block_size) * padding
    return padData


if __name__ == "__main__":
    aes = AESCipher()
    data = []
    data.append("00512780021653754567622621120000")
    # data.append("00156318851653785728742065540000")
    data_js = json.dumps(data)
    # encrypt1 = encrypt_1(data_js.encode("utf-8"), "1111222233334444".encode("utf-8"))
    # print(encrypt1)

    decrypt = aes.decrypt("YmFHVC9ITkIrMlJLVFlYT0s5TGtoT2VJNlhjRStTbTJzVGlSRTQreStmK1VFU3pYRW5SaDU4SWFEVmV1ZU1TVw==")
    print(decrypt)
    # encrypt = aes.encrypt(data_js)
    # print(encrypt)
    # lmarketing = lmarketingUtils.post_lmarketing(encrypt)
    # print(lmarketing)
    # params = ("encryptData",encrypt)

    # aes.encrypt()
    # df = pd.DataFrame(data=[13462403256, 13462403286], columns=['id'])
    # print(df)
    # df['id'] = df['id'].map(aes.encrypt)
    # print(df)
    # df['id'] = df['id'].map(aes.decrypt)
    # print(df)
