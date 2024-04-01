# 比较5个城市一居、二居、三居的情况，包含均价、最高价、最低价、中位数等信息，采用合适的图或表形式进行展示。

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use("TKAgg")
import seaborn as sns

plt.rcParams["font.sans-serif"] = ["SimHei"]


cities = ["beijing", "shanghai", "shenzhen", "guangzhou", "suzhou"]

# 读取数据,lianjia_{city}_processed.json
data = pd.DataFrame()
for city in cities:
    file_path = f"lianjia_{city}_processed.json"
    city_data = pd.read_json(file_path, lines=True)
    city_data["city"] = city  # Add city column
    data = pd.concat([data, city_data])


# 因为根据房型来分析，所以需要先分为整租、合租、独栋三种租赁类型
data["rent_type"] = ""
# 整租
data.loc[data["name"].str.contains("整租"), "rent_type"] = "整租"
# 合租
data.loc[data["name"].str.contains("合租"), "rent_type"] = "合租"
# 独栋
data.loc[data["name"].str.contains("独栋"), "rent_type"] = "独栋"
# 都不是
data.loc[data["rent_type"] == "", "rent_type"] = "其他"

# 比较同一租赁方式，同一房型在不同城市的数量、均价、最高价、最低价、中位数等信息，采用合适的图或表形式进行展示

# 不同房型还是需要聚合一下，比如1室1厅、1室0厅、1室2厅都是1室，所以需要把这些房型都归为1室

nan_rows = data[data["layout"].isna()]
print(nan_rows)

# 1室或1房间
data.loc[data["layout"].str.contains("1室", na=False), "layout"] = "1居室"
data.loc[data["layout"].str.contains("1房间", na=False), "layout"] = "1居室"
# 2室或2房间
data.loc[data["layout"].str.contains("2室", na=False), "layout"] = "2居室"
data.loc[data["layout"].str.contains("2房间", na=False), "layout"] = "2居室"
# 3室或3房间
data.loc[data["layout"].str.contains("3室", na=False), "layout"] = "3居室"
data.loc[data["layout"].str.contains("3房间", na=False), "layout"] = "3居室"


# Group the data and calculate the statistics
grouped_data = data.groupby(["rent_type", "city", "layout"])["total_price"].agg(
    ["count", "mean", "max", "min", "median"]
)

# Reset the index to make 'rent_type', 'city', and 'layout' columns again
grouped_data = grouped_data.reset_index()

# Filter the layout to only include 1居室, 2居室, and 3居室
filtered_data = grouped_data[grouped_data["layout"].isin(["1居室", "2居室", "3居室"])]

# Print the table
# print(filtered_data)


def plot_rent_type(filtered_data, rent_type):
    fig, axes = plt.subplots(2, 2, figsize=(12, 8))
    sns.barplot(
        x="city",
        y="mean",
        hue="layout",
        data=filtered_data[filtered_data["rent_type"] == rent_type],
        ax=axes[0][0],
    )
    axes[0][0].set_title(f"{rent_type} - 均价")
    sns.barplot(
        x="city",
        y="max",
        hue="layout",
        data=filtered_data[filtered_data["rent_type"] == rent_type],
        ax=axes[0][1],
    )
    axes[0][1].set_title(f"{rent_type} - 最高价")
    sns.barplot(
        x="city",
        y="min",
        hue="layout",
        data=filtered_data[filtered_data["rent_type"] == rent_type],
        ax=axes[1][0],
    )
    axes[1][0].set_title(f"{rent_type} - 最低价")
    sns.barplot(
        x="city",
        y="median",
        hue="layout",
        data=filtered_data[filtered_data["rent_type"] == rent_type],
        ax=axes[1][1],
    )
    axes[1][1].set_title(f"{rent_type} - 中位数")
    plt.show()


plot_rent_type(filtered_data, "整租")
# plot_rent_type(filtered_data, "合租")
# plot_rent_type(filtered_data, "独栋")
