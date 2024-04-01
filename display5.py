# 与2022年的租房数据进行对比（只比较北上广深4个城市，原始数据会给出），总结你观察到的变化情况，并用图、表、文字等支撑你得到的结论。

# 2022年的租房数据,RawData2022/{city}HouseInfo.json
# 2023年的租房数据,lianjia_{city}_processed.json

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

matplotlib.use("TKAgg")

matplotlib.rcParams["font.family"] = "SimHei"


cities = ["beijing", "shanghai", "guangzhou", "shenzhen"]

data_2022 = {}
data_2023 = {}

for city in cities:
    data_2022[city] = pd.read_json(
        f"RawData2022/{city.capitalize()}HouseInfo.json", lines=True
    )
    data_2023[city] = pd.read_json(f"lianjia_{city}_processed.json", lines=True)

avg_prices_2022 = {city: df["total_price"].mean() for city, df in data_2022.items()}
avg_prices_2023 = {
    city: df[df["name"].str.startswith("整租")]["total_price"].mean()
    for city, df in data_2023.items()
}

df_2022 = pd.DataFrame.from_dict(
    avg_prices_2022, orient="index", columns=["Avg Price 2022"]
)
df_2023 = pd.DataFrame.from_dict(
    avg_prices_2023, orient="index", columns=["Avg Price 2023"]
)

df = pd.concat([df_2022, df_2023], axis=1)

df.plot(kind="bar", figsize=(10, 6))
plt.title("Average Rental Prices in 2022 vs 2023")
plt.ylabel("Average Price")
plt.show()
