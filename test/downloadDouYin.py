import requests
import json
import re

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    # 这个貌似很重要
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36',
}


def download(url):
    """
    下载抖音无水印视频
    """
    # 获取接口参数
    html = requests.get(url=url)
    html.encoding = 'utf-8'
    title = re.findall('itemId: "(.*?)",', html.text)[0]
    dytk = re.findall('dytk: "(.*?)" }', html.text)[0]

    # 拼接接口
    url_item = 'https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=' + title + '&dytk=' + dytk

    # 获取抖音无水印视频链接
    html_item = requests.get(url=url_item, headers=headers)
    # 字符串转字典
    content = json.loads(html_item.text)

    # 视频接口
    url_video = content['item_list'][0]['video']['play_addr']['url_list'][1]
    response = requests.get(url_video, headers=headers, allow_redirects=True)

    # 获取重定向后的链接,这个也是无水印视频的下载链接,不过本次没用
    redirect = response.url
    print(redirect)

    # 视频是二进制,需要这种下载办法
    video = requests.get(url_video, headers=headers).content
    video_name = "/Users/admin/Desktop/douyin/douyin.mp4"
    with open(video_name, 'wb') as f:
        f.write(video)
        f.flush()
    print("下载完成")


if __name__ == '__main__':
    # 抖音链接
    url = 'https://v.douyin.com/XJj85H/'
    download(url)