# 查询各个城市的平均工资，分析并展示其和单位面积租金分布的关系。比较一下在哪个城市租房的负担最重？

# 北京 13251
# 上海 13433
# 深圳 12668
# 广州 10913
# 苏州 11037


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

# 存在没有总价的情况，将其删除
data["total_price"] = pd.to_numeric(data["total_price"], errors="coerce")

# 单位面积租金的均价，price_per_m2字段
avg_price_per_m2 = data.groupby("city")["price_per_m2"].mean().reset_index()
avg_price_per_m2.columns = ["city", "avg_price_per_m2"]

# 月工资数据
monthly_salaries = [13251, 13433, 12668, 10913, 11037]
avg_price_per_m2["monthly_salary"] = monthly_salaries

# 采用合适的图或表形式进行展示
# price_per_m2
# 柱状图
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

# 绘制单位面积租金的均价柱状图
sns.barplot(x="city", y="avg_price_per_m2", data=avg_price_per_m2, ax=axes[0])
axes[0].set_title("Average Price per m2")

# 绘制月工资的柱状图
sns.barplot(x="city", y="monthly_salary", data=avg_price_per_m2, ax=axes[1])
axes[1].set_title("Monthly Salary")
# 计算单位面积租金和月工资的比值
avg_price_per_m2["price_salary_ratio"] = (
    avg_price_per_m2["avg_price_per_m2"] / avg_price_per_m2["monthly_salary"]
)

# 创建比值表
ratio_table = avg_price_per_m2[["city", "price_salary_ratio"]]

# 打印比值表
print(ratio_table)

plt.show()
