import json
from urllib.request import urlopen, quote
import requests


# def getlnglat(address):
#     url = "https://api.map.baidu.com/geocoding/v3/"
#     output = "json"
#     ak = "pwuU3PVgUDwat8xsU0RVa40XqTG1seWV"
#     address = quote(address)
#     uri = url + "?" + "address=" + address + "&output=" + output + "&ak=" + ak
#     req = urlopen(uri)
#     res = req.read().decode()
#     try:
#         temp = json.loads(res)
#         lat = temp["result"]["location"]["lat"]
#         lng = temp["result"]["location"]["lng"]
#     except KeyError:
#         lat = 0
#         lng = 0
#     return lat, lng


# with open("lianjia_shanghai_processed.json", "r", encoding="utf-8") as f:
#     lines = f.readlines()
#     xiaoqu_dict = {}  # 创建一个字典来保存已查询过的小区信息
#     for line in lines[16612:]:
#         data = json.loads(line)
#         xiaoqu = data["name"].split()[0]
#         xiaoqu = xiaoqu[3:]

#         if xiaoqu in xiaoqu_dict:  # 检查字典中是否已存在该小区信息
#             data["lat"] = xiaoqu_dict[xiaoqu][0]
#             data["lng"] = xiaoqu_dict[xiaoqu][1]
#         else:
#             lat, lng = getlnglat("上海" + xiaoqu)  # 调用getlnglat函数查询API
#             xiaoqu_dict[xiaoqu] = (lat, lng)  # 将查询结果保存到字典中
#             data["lat"] = lat
#             data["lng"] = lng

#         with open("lianjia_shanghai_processed_ll.json", "a", encoding="utf-8") as f:
#             f.write(json.dumps(data, ensure_ascii=False) + "\n")


# {
#     "name": "整租·久耕小区 1室1厅 东南",
#     "district": "北外滩",
#     "total_price": 4692,
#     "price_per_m2": 155.83,
#     "area": 30.11,
#     "direction": "东南",
#     "layout": "1室1厅1卫",
#     "lat": 31.257715377406086,
#     "lng": 121.49715930872213
# }

import json

new_data = []

# 打开文件
with open("lianjia_shanghai_processed_ll.json", "r", encoding="utf-8") as file:
    # 读取整个文件内容
    content = file.read()

decoder = json.JSONDecoder()
while content:
    # 使用raw_decode解析出一个JSON对象
    item, idx = decoder.raw_decode(content)
    # 创建新的字典并添加到列表中
    new_data.append(
        {"lng": item["lng"], "lat": item["lat"], "count": item["price_per_m2"]}
    )
    # 处理剩下的字符串
    content = content[idx:].lstrip()

# 将新的列表转换为JSON字符串
new_data_json = json.dumps(new_data)

# 将JSON字符串写入新的文件
with open("new_data.json", "w") as file:
    file.write(new_data_json)
