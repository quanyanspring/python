import logging
from flask import Flask,render_template

app = Flask(__name__)

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

@app.route('/',methods = ['GET'])
def hello():
    app.logger.debug('这是一个调试日志消息')
    app.logger.info('这是一个信息日志消息')
    app.logger.warning('这是一个警告日志消息')
    app.logger.error('这是一个错误日志消息')
    logging.info(f'这是一个错误日志消息')
    return render_template('/Users/wlq/Desktop/瀑布流.html')

if __name__ == '__main__':
    app.run()
