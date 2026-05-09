# 【NLP教程】用 python 调用百度 AI 开放平台进行批量情感倾向分析

---

## 一、背景

Hi，大家！我是 [@马哥python说](https://github.com/mashukui)，一名 10 年程序猿。

今天我来分享：通过百度 AI 开放平台，利用 python 调用百度接口进行中文情感倾向分析，并得出情感极性分为积极、消极还是中性以及置信度结果。

---

## 二、操作步骤

首先，打开百度 AI 首页：[百度AI开放平台](https://ai.baidu.com/)

在顶部菜单，依次选择：**开放能力** → **语言与知识** → **语言理解** → **情感倾向分析**，如图所示：<img width="1440" height="874" alt="image" src="https://github.com/user-attachments/assets/1f71b3d1-aabd-4395-863b-bc40231c0d61" />


在服务列表中，选择「情感倾向分析」，点击开通（我的已经开通了）：<img width="1440" height="873" alt="image" src="https://github.com/user-attachments/assets/2333bfec-ebd0-4b4a-89a5-070da1a5e435" />


通过查看[技术文档](https://ai.baidu.com/ai-doc/NLP/zk6z52hds)得知，请求服务需要用 `access_token`，而想要得到 `access_token`，又得需要 **API Key** 和 **Secret Key**，想要得到 Key 就得创建应用。因此，梳理思路如下：

1. 创建应用，得到 API Key 和 Secret Key
2. 利用 Key，得到 access_token
3. 有了 access_token，向情感分析接口发送请求，得到返回结果

### 2.1 创建应用

打开[应用列表](https://console.bce.baidu.com/ai/?_=1681545511289&fromai=1#/ai/nlp/app/list)，点击创建应用：<img width="1440" height="511" alt="image" src="https://github.com/user-attachments/assets/34c93423-df22-48bf-a412-4521a56e821e" />


选择「自然语言处理」，点击创建：<img width="1440" height="875" alt="image" src="https://github.com/user-attachments/assets/ec278d6e-9ef5-4076-b880-8bd37069ce51" />


创建成功之后，会得到 **AppID、API Key、Secret Key** 三个关键信息：<img width="1440" height="505" alt="image" src="https://github.com/user-attachments/assets/9954db2d-196c-4df2-bd7f-76d96703eac9" />


### 2.2 获取 token

打开鉴权认证页面，我们直接用 python 代码获取 token：<img width="1440" height="874" alt="image" src="https://github.com/user-attachments/assets/4993dba8-452b-4120-a5c1-803bdb9a5931" />


`client_id` 代入 API Key，`client_secret` 代入 Secret Key，代码运行结果：<img width="1440" height="875" alt="image" src="https://github.com/user-attachments/assets/9223d4d3-7888-4fe3-96e7-c297caf1a65d" />


返回结果中的 `access_token` 就是了。

下面是获取 access_token 的 Python 代码示例：

```python
import requests

# 获取access_token
def get_access_token():
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {
        "grant_type": "client_credentials",
        "client_id": "YOUR_API_KEY",      # 替换为你的API Key
        "client_secret": "YOUR_SECRET_KEY"  # 替换为你的Secret Key
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    response = requests.post(url, params=params, headers=headers)
    result = response.json()
    print("access_token:", result.get("access_token"))
    return result.get("access_token")
```

### 2.3 情感倾向分析

获取到 token 之后，调用情感倾向分析接口，代码如下：<img width="1440" height="875" alt="image" src="https://github.com/user-attachments/assets/60a55efd-3ec7-4f33-83fb-0a6ee35493f3" />



下面是情感倾向分析的 Python 代码示例：

```python
import requests
import json

# 情感倾向分析
def sentiment_analysis(text, access_token):
    url = f"https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?access_token={access_token}"
    payload = json.dumps({"text": text})
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=payload, headers=headers)
    result = response.json()
    print("分析结果:", result)
    return result
```

**测试 1：**

输入文本：*我今天太伤心了，因为我摔了一跤，呜呜呜*

输出结果：
- 置信度：0.831307
- 消极概率：0.924088
- 积极概率：0.0759116
- **判定结果：消极**
<img width="1440" height="875" alt="image" src="https://github.com/user-attachments/assets/231d59b0-33ef-499b-9aea-fa4b7f1af49c" />


**测试 2：**

输入文本：*我可太喜欢看《狂飙》这部电视剧了，演技全员在线！！*

输出结果：
- 置信度：0.999714
- 消极概率：0.00012881
- 积极概率：0.999871
- **判定结果：积极**
<img width="1440" height="875" alt="image" src="https://github.com/user-attachments/assets/fb3452a8-469d-435f-8d97-a88bdc99cc89" />


**测试 3：**

输入文本：*很多人是不能理解那些上有老下有小的人的，特别是家里有严重基础疾病的至亲。我不怕我自己面对新冠，但是我妈妈去年确诊肺癌，切了大半个肺，现在正在治疗中，一点感冒就让她无比痛苦，我怎么敢让她去面对新冠病毒？那些自己得了新冠又不戴口罩在公共场合潇洒快乐的人，请多去为那些弱势群体想想吧，因为总有一天你也极有可能成为他们中的一员，你才能明白那种生命不能承受之重。*

输出结果：
- 置信度：0.814589
- 消极概率：0.916565
- 积极概率：0.0834351
- **判定结果：消极**

<img width="1440" height="875" alt="image" src="https://github.com/user-attachments/assets/7f872520-c76a-489c-8343-b502171a10a0" />

---

## 三、其他情感分析

其他 python 中文情感分析库，比如 snownlp 应用我之前写的比较多，准确率有待考证。

如果你觉得准确率低，百度还提供了自训练模型的 EasyDL 平台供使用，无代码开发经验也可训练模型，很方便。

另外，阿里、腾讯、华为等 AI 开放平台也有对标的接口服务，大家可以试试看。

---

## 四、讲解视频

如看文章还是不懂，我本人也录制了同步讲解视频，手把手带你完成：[点击观看](https://www.zhihu.com/zvideo/1630853760930095104)

---

文章中介绍的是针对单个文本进行情感分析。仓库中上传了批量文本分析（从Excel文件中读取批量文本，如评论，利用循环逻辑依次判断情感倾向，并输出批量分析结果），欢迎小伙伴们学习、交流！

如有帮助，点个Star⭐️，就是对我莫大的鼓励支持！
