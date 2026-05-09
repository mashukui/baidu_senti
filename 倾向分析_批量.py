# 程序功能：利用百度API实现批量情感分析
# 原创作者：马哥python说
import pandas as pd
import requests
import json


def trans_senti(v_value):
	"""转换情感分析判定结果"""
	if v_value == 0:
		return '消极'
	elif v_value == 1:
		return '中性'
	elif v_value == 2:
		return '积极'
	else:
		return '未知'


def get_senti(v_text):
	"""情感判定函数"""
	access_token = '换成自己的access_token'
	# 请求地址
	url = "https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token={}&charset=utf-8".format(
		access_token)
	# 请求参数
	payload = json.dumps({
		"text": v_text
	})
	# 请求头
	headers = {
		'Content-Type': 'application/json',
		'Accept': 'application/json'
	}
	# 发送post请求
	response = requests.request("POST", url, headers=headers, data=payload)
	# 解析返回结果
	json_data = response.json()
	# 获取情感判定值
	senti_value = json_data['items'][0]['sentiment']
	# 转换情感判定结果
	senti_result = trans_senti(senti_value)
	return senti_result


if __name__ == '__main__':
	# 读取数据源
	df = pd.read_csv('微博评论.csv')
	text_list = df['评论内容'].values.tolist()
	senti_result_list = []
	# 循环处理情感判定
	for text in text_list:
		senti_result = get_senti(text)
		senti_result_list.append(senti_result)
		print(text, senti_result)
	df['情感结果'] = senti_result_list
	# 把判定结果保存到新的csv
	df.to_csv('微博评论_判定后.csv', index=False, encoding='utf_8_sig')
	print('判定后csv已保存！')
