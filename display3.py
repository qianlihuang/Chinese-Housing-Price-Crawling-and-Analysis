# 计算和分析每个城市不同板块的均价情况，并采用合适的图或表形式进行展示。

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

matplotlib.use("TKAgg")
plt.rcParams["font.sans-serif"] = ["SimHei"]


def plot_mean_price(city):
    # Read data from the processed file
    df = pd.read_json(f"./lianjia_{city}_processed.json", lines=True)

    # Group by district and calculate the mean price and count of houses
    groupby_district = df.groupby("district")
    mean_price = groupby_district["price_per_m2"].mean().sort_values(ascending=False)
    house_count = groupby_district.size().sort_values(ascending=False)

    # Plot the mean price using seaborn
    fig, ax1 = plt.subplots(figsize=(20, 10))
    ax1.bar(mean_price.index, mean_price.values, color="blue")
    ax1.set_xticklabels(mean_price.index, rotation=90, fontsize=4.34)
    ax1.set_xlabel("板块")
    ax1.set_ylabel("均价（元/㎡每月）")
    ax1.set_title(f"{city}各个板块的均价和房子数量")

    # Create a secondary y-axis for house count
    ax2 = ax1.twinx()
    ax2.bar(house_count.index, house_count.values, alpha=0.5, color="red")
    ax2.set_ylabel("房子数量")

    plt.show()

    # Get the top 10 and last 10 districts by mean price
    top_10_districts = mean_price.head(10)
    last_10_districts = mean_price.tail(10)

    # Plot the top 10 districts
    plt.figure(figsize=(10, 5))
    sns.barplot(x=top_10_districts.index, y=top_10_districts.values, color="blue")
    plt.xticks(rotation=90)
    plt.xlabel("板块")
    plt.ylabel("均价（元/㎡每月）")
    plt.title("前十个板块的均价")
    plt.show()

    # Plot the last 10 districts
    plt.figure(figsize=(10, 5))
    sns.barplot(x=last_10_districts.index, y=last_10_districts.values, color="blue")
    plt.xticks(rotation=90)
    plt.xlabel("板块")
    plt.ylabel("均价（元/㎡每月）")
    plt.title("后十个板块的均价")
    plt.show()


# Call the function for a specific city
plot_mean_price("suzhou")
