from Crypto.Cipher import AES
import base64
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

class AESTest:

    # 随机生成16字节（即128位）的加密密钥
    # key = get_random_bytes(16)
    def encrypt_1(self,data):
        key = "0102030405060708".encode("utf8")
        # 实例化加密套件，使用CBC模式
        cipher = AES.new(key, AES.MODE_CBC)
        # 对内容进行加密，pad函数用于分组和填充
        encrypted_data = cipher.encrypt(pad(data.encode("utf-8"), AES.block_size))
        # 加密后得到的是bytes类型的数据

        encodestrs = base64.b64encode(encrypted_data)
        # 使用Base64进行编码,返回byte字符串
        enctext = encodestrs.decode('utf8')
        return enctext



    def decrypt(self, enc):
        # 先将密文进行base64解码
        enc = base64.b64decode(enc)
        # 取出iv值
        iv = enc[:self.BS]
        # 初始化自定义
        cipher = AES.new(self.key, self.mode, iv)
        # 返回utf8格式的数据
        return self.unpad(cipher.decrypt(enc[self.BS:])).decode()



if __name__ == "__main__":
    enctext = AESTest.encrypt_1("00512780021653754567622621120000")
    print(enctext)
    print(AESTest.decrypt(enctext))



# 将加密内容写入文件
# file_out = open(data)
# 在文件中依次写入key、iv和密文encrypted_data
# [file_out.write(x) for x in (key, cipher.iv,  encrypted_data)]