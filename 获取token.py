# 程序功能：在百度AI中获取自己的access_token
# 原创作者：马哥python说
import requests
from pprint import pprint


def main():
	API_KEY = '换成自己的API_KEY'
	SECRET_KEY = '换成自己的SECRET_KEY'
	# 获取token地址
	url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}".format(
		API_KEY, SECRET_KEY)
	payload = ""
	# 请求头
	headers = {
		'Content-Type': 'application/json',
		'Accept': 'application/json'
	}
	# 发送post请求
	response = requests.request("POST", url, headers=headers, data=payload)
	# 打印结果
	pprint(response.json())


if __name__ == '__main__':
	main()
