import json
from tqdm import tqdm

# Specify the city
city = "shenzhen"

# Read the data
with open(f"spiderall/3_spider/lianjia_{city}.json", "r") as f:
    data = [json.loads(line) for line in f.readlines()]

# 先去重，所有字段都相同的数据，只保留一条
# 1. 定义一个空列表，用于存放去重后的数据
data_processed = []
# 2. 遍历data，如果data_processed中没有该条数据，则加入data_processed
for line in tqdm(data, desc="Deduplication", ncols=80):
    if line not in data_processed:
        data_processed.append(line)
# 3. 将data_processed赋值给data
data = data_processed


total_lines = len(data)
processed_lines = 0

for line in tqdm(data, desc="Processing", ncols=80):
    # 1. 处理数据，area_direction_layout字段，将其拆分为area、direction、layout三个字段
    area_direction_layout = line["area_direction_layout"]
    # 三个字段位置不确定
    # area字段的特点是带有㎡，direction字段的特点是带有东西南北，layout字段的特点是带有室厅卫，所以可以通过这些特点来拆分
    # area字段
    area = ""
    for i in area_direction_layout:
        if "㎡" in i:
            area = i
            break
    # 去掉㎡，转换为float类型，20.28-21.14这种情况，取中位数
    area = area.replace("㎡", "")
    if "-" in area:
        area = float(area.split("-")[0]) + float(area.split("-")[1]) / 2
    else:
        try:
            area = float(area)
        except ValueError:
            area = None
    # direction字段
    direction = ""
    for i in area_direction_layout:
        if "东" in i or "西" in i or "南" in i or "北" in i:
            direction = i
            break
    # layout字段
    layout = ""
    for i in area_direction_layout:
        if "室" in i or "厅" in i or "卫" in i:
            layout = i
            break

    # 2. 处理数据，total_price字段，将其转换为int类型
    # "total_price": "5900-6100" 这种情况，取中位数
    total_price = line["total_price"]
    if "-" in total_price:
        total_price = (
            int(total_price.split("-")[0]) + int(total_price.split("-")[1]) / 2
        )
    else:
        total_price = int(total_price)

    # 3. 加入price_per_m2字段，保留两位小数
    if area != 0 and area is not None:
        price_per_m2 = round(total_price / area, 2)
    else:
        price_per_m2 = None

    line["price_per_m2"] = price_per_m2

    line["area"] = area
    line["direction"] = direction
    line["layout"] = layout
    line["total_price"] = total_price
    line.pop("area_direction_layout")

    processed_lines += 1

    if processed_lines % 100 == 0:
        tqdm.write(f"Processed {processed_lines}/{total_lines} lines")

# 写入数据，lianjia_beijing_processed.json

with open(f"lianjia_{city}_processed.json", "w") as f:
    for line in data:
        f.write(json.dumps(line, ensure_ascii=False))
        f.write("\n")
