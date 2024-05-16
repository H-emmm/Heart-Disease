
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv('heart_2020_cleaned.csv')
df.columns = ["心脏病", "BMI", "吸烟", "重度饮酒", "中风", "30天内身体不健康天数", "30天内心理不健康天数", "走路或爬楼是否困难", "性别",
              "年龄", "种族", "糖尿病", "身体锻炼", "总体健康", "睡眠时间", "哮喘", "肾病", "皮肤癌"]

pd.set_option("display.max_columns", 100)
print(df.head())
print("整体情况：\n", df.describe(include="all"))
print("各列情况：\n", df.info)
print("缺失值情况：\n", df.isnull().sum())
# 无数据异常
sns.set_style("darkgrid")  # 设置样式

# colRange = [['Smoking', 'AlcoholDrinking', 'Stroke'], ['DiffWalking', 'Sex', 'PhysicalActivity'],
#             ['Asthma', 'KidneyDisease', 'SkinCancer']]
# 存在9个类，数值仅分为“Yes”或“No”
colRange = [["吸烟", "重度饮酒", "中风"], ["走路或爬楼是否困难", "性别", "身体锻炼"],
            ["哮喘", "肾病", "皮肤癌"]]


fig, axes = plt.subplots(3, 3, figsize=(20, 20))  # 3*3显示子图
for row in range(3):
    for col in range(3):
        column = colRange[row][col]
        sns.countplot(ax=axes[row, col], x=df[column], hue=df["心脏病"])  # 柱状图
        axes[row, col].set_ylabel("数量")
        axes[row, col].set_xlabel(format(column))
plt.subplots_adjust(hspace=0.5)  # 设置间距
plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文
plt.show()

df["性别"] = df["性别"].replace(to_replace=["Male", "Female"], value=["Yes", "No"])
fig, axes = plt.subplots(3, 3, figsize=(20, 20))
for row in range(3):
    for col in range(3):
        column = colRange[row][col]
        df_number_yes = len(df.loc[(df[column] == "Yes") & (df["心脏病"] == "Yes")])  # 得心脏病情况下，该类中“Yes”的数量
        df_number_no = len(df.loc[(df[column] == "No") & (df["心脏病"] == "Yes")])
        if column != "性别":
            x = ["Yes", "No"]
        else:
            x = ["男", "女"]
        # 该类“Yes”情况下，得心脏病比例    该类“No”情况下，得心脏病比例
        y = [df_number_yes / df[column].value_counts()["Yes"], df_number_no / df[column].value_counts()["No"]]
        sns.barplot(x, y, ax=axes[row, col])
        axes[row, col].set_ylabel("比例")
        axes[row, col].set_xlabel(format(column))
        axes[row, col].set_title("患心脏病情况下，{}类不同情况所占比例".format(column))
plt.subplots_adjust(hspace=0.5)  # 设置间距
plt.rcParams['font.sans-serif'] = ['SimHei']  # 正常显示中文
plt.show()

# 种族对心脏病影响
df["种族"] = df["种族"].replace(to_replace=["White", "Black", "Asian", "American Indian/Alaskan Native", "Other",
                                        "Hispanic"], value=["白种人", "黑种人", "亚洲人", "美国印第安人/阿拉斯加本地", "其他", "西班牙人"])
plt.figure(figsize=(12, 6))
sns.countplot(df["种族"], hue=df["心脏病"])
plt.title('种族影响')
plt.ylabel("数量")

# 糖尿病对心脏病影响
df["糖尿病"] = df["糖尿病"].replace(to_replace=["No, borderline diabetes", "Yes (during pregnancy)"], value=["No(边缘型糖尿病)",
                                                                                                       "Yes(怀孕期间)"])
plt.figure(figsize=(12, 6))
sns.countplot(df["糖尿病"], hue=df["心脏病"])
plt.title('糖尿病影响')
plt.ylabel("数量")

# BMI对心脏病影响
plt.figure(figsize=(12, 6))
sns.histplot(data=df[df["心脏病"] == 'Yes'], x='BMI', kde=True, color='red')
sns.histplot(data=df[df["心脏病"] == 'No'], x='BMI', kde=True, color='blue')
plt.title('BMI影响')
plt.ylabel("数量")

# 身体健康对心脏病影响
plt.figure(figsize=(12, 6))
sns.kdeplot(df[df["心脏病"] == 'Yes']["30天内身体不健康天数"], shade=True, color='red')
sns.kdeplot(df[df["心脏病"] == 'No']["30天内身体不健康天数"], shade=True, color='blue')
plt.title('身体健康影响')
plt.ylabel("密度")

# 心理健康对心脏病影响
plt.figure(figsize=(12, 6))
sns.kdeplot(df[df["心脏病"] == 'Yes']["30天内心理不健康天数"], shade=True, color='red')
sns.kdeplot(df[df["心脏病"] == 'No']["30天内心理不健康天数"], shade=True, color='blue')
plt.title('心理健康影响')
plt.ylabel("密度")


plt.show()
