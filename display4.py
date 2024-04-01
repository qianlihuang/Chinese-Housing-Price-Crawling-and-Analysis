# 比较各个城市不同朝向的单位面积租金分布情况，采用合适的图或表形式进行展示。哪个方向最高，哪个方向最低？各个城市是否一致？如果不一致，你认为原因是什么？


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

matplotlib.use("TKAgg")

matplotlib.rcParams["font.family"] = "SimHei"


# 读取数据，lianjia_{city}_processed.json
def plot_direction(city):
    df = pd.read_json(f"./lianjia_{city}_processed.json", lines=True)
    # print(df.head(3))
    # print(df.info())
    # print(df.describe())

    # 将空字符串替换为其他值
    df["direction"] = df["direction"].replace("", "其他")

    # 以朝向为分组，计算每个朝向的平均价格和房子总数
    groupby_direction = df.groupby("direction")
    mean_price = groupby_direction["price_per_m2"].mean().sort_values(ascending=False)
    count = groupby_direction.size().sort_values(ascending=False)

    # 画图
    fig, ax1 = plt.subplots(figsize=(20, 10))
    ax2 = ax1.twinx()
    sns.barplot(x=mean_price.index, y=mean_price.values, ax=ax1)
    sns.lineplot(x=count.index, y=count.values, color="red", marker="o", ax=ax2)
    ax1.set_xticklabels(mean_price.index, rotation=90, fontsize=8.68)
    ax1.set_xlabel("朝向")
    ax1.set_ylabel("均价（元/㎡每月）")
    ax2.set_ylabel("房子总数")
    ax1.set_title(f"{city}各个朝向的均价和房子总数")
    plt.show()


plot_direction("suzhou")
