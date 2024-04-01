# 比较5个城市的总体房租情况，包含租金的均价、最高价、最低价、中位数等信息，单位面积租金（元/平米）的均价、最高价、最低价、中位数等信息。采用合适的图或表形式进行展示。

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("TKAgg")
import seaborn as sns

cities = ["beijing", "shanghai", "shenzhen", "guangzhou", "suzhou"]

# 读取数据,lianjia_{city}_processed.json
data = pd.DataFrame()
for city in cities:
    file_path = f"lianjia_{city}_processed.json"
    city_data = pd.read_json(file_path, lines=True)
    city_data["city"] = city  # Add city column
    data = pd.concat([data, city_data])


# {"name": "整租·方丹苑 2室1厅 东北", "district": "潘家园", "total_price": 8200, "price_per_m2": 92.13, "area": 89.0, "direction": "东北", "layout": "2室1厅1卫"}

# 存在没有总价的情况，将其删除
data["total_price"] = pd.to_numeric(data["total_price"], errors="coerce")
# # 找出包含字符串值的行
# string_values = data[pd.isna(data['total_price'])]
# print(string_values)

# 租金的均价，total_price字段
avg_total_price = data.groupby("city")["total_price"].mean().reset_index()
avg_total_price.columns = ["city", "avg_total_price"]


# 租金的最高价，total_price字段
max_total_price = data.groupby("city")["total_price"].max().reset_index()
max_total_price.columns = ["city", "max_total_price"]

# 租金的最低价，total_price字段
min_total_price = data.groupby("city")["total_price"].min().reset_index()
min_total_price.columns = ["city", "min_total_price"]

# 租金的中位数，total_price字段
median_total_price = data.groupby("city")["total_price"].median().reset_index()
median_total_price.columns = ["city", "median_total_price"]

# 单位面积租金的均价，price_per_m2字段
avg_price_per_m2 = data.groupby("city")["price_per_m2"].mean().reset_index()
avg_price_per_m2.columns = ["city", "avg_price_per_m2"]

# 单位面积租金的最高价，price_per_m2字段
max_price_per_m2 = data.groupby("city")["price_per_m2"].max().reset_index()
max_price_per_m2.columns = ["city", "max_price_per_m2"]

# 单位面积租金的最低价，price_per_m2字段
min_price_per_m2 = data.groupby("city")["price_per_m2"].min().reset_index()
min_price_per_m2.columns = ["city", "min_price_per_m2"]

# 单位面积租金的中位数，price_per_m2字段
median_price_per_m2 = data.groupby("city")["price_per_m2"].median().reset_index()
median_price_per_m2.columns = ["city", "median_price_per_m2"]

# 采用合适的图或表形式进行展示
# total_price
# 柱状图
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
sns.barplot(x="city", y="avg_total_price", data=avg_total_price, ax=axes[0][0])
sns.barplot(x="city", y="max_total_price", data=max_total_price, ax=axes[0][1])
sns.barplot(x="city", y="min_total_price", data=min_total_price, ax=axes[1][0])
sns.barplot(x="city", y="median_total_price", data=median_total_price, ax=axes[1][1])

plt.show()


# price_per_m2
# 柱状图
fig, axes = plt.subplots(2, 2, figsize=(12, 8))
sns.barplot(x="city", y="avg_price_per_m2", data=avg_price_per_m2, ax=axes[0][0])
sns.barplot(x="city", y="max_price_per_m2", data=max_price_per_m2, ax=axes[0][1])
sns.barplot(x="city", y="min_price_per_m2", data=min_price_per_m2, ax=axes[1][0])
sns.barplot(x="city", y="median_price_per_m2", data=median_price_per_m2, ax=axes[1][1])

plt.show()
