import json

city = "suzhou"

# 打开文件并读取内容，指定编码为 'utf-8'
with open(f"lianjia_{city}.json", "r", encoding="utf-8") as f:
    content = f.read()

# 按行分割内容以获取 JSON 字符串列表
json_strings = content.split("\n")

# 将每个 JSON 字符串解析为 Python 对象
data = [json.loads(js) for js in json_strings if js]

# 创建一个空列表来存储唯一项
unique_data = []

# 遍历字典列表
for item in data:
    # 如果项不在唯一列表中，添加它
    if item not in unique_data:
        unique_data.append(item)

# 以 JSON 格式将唯一列表中的每个项单独写入文件，每个项占一行
with open(f"lianjia_{city}_processed.json", "w", encoding="utf-8") as f:
    for item in unique_data:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")
