# Week 3: Python & Data Wrangling — completed assignment
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Read the Excel dataset (or use pd.read_csv("data.csv") for CSV files)
df = pd.read_excel("data.xlsx")
print(df.head())
print(df.info())
print(df.isnull().sum())

# 2. Clean the Date column
df["Date"] = df["Date"].astype("string").str.replace("'", "", regex=False).str.strip()
df["Date"] = pd.to_datetime(df["Date"], format="mixed", errors="coerce")
for i in df.index[df["Date"].isna()]:
    if i > 0 and i < len(df)-1 and pd.notna(df.loc[i-1,"Date"]) and pd.notna(df.loc[i+1,"Date"]):
        df.loc[i,"Date"] = df.loc[i-1,"Date"] + (df.loc[i+1,"Date"]-df.loc[i-1,"Date"])/2

# 3. Remove duplicates and handle missing values
df = df.drop_duplicates()
df["Calories"] = df["Calories"].fillna(df["Calories"].median())

# 4. Filter implausible records
df = df[(df["Duration"] <= 120) & (df["Maxpulse"] >= df["Pulse"])].copy()

# 5. Create new columns
df["Calories_per_Minute"] = (df["Calories"] / df["Duration"]).round(2)
df["Duration_Category"] = pd.cut(df["Duration"], bins=[0,30,45,60,120], labels=["Short (≤30 min)","Medium (31–45 min)","Standard (46–60 min)","Long (61–120 min)"], include_lowest=True)
df["Pulse_Difference"] = df["Maxpulse"] - df["Pulse"]

# 6. Filter rows for focused analysis
filtered = df[(df["Duration"] >= 60) & (df["Calories"] >= 300)]
print(filtered)
print(df.describe(include="all"))

# 7. Visualize data with Matplotlib and Seaborn
sns.set_theme(style="whitegrid")
sns.histplot(df["Calories"], kde=True); plt.title("Distribution of Calories Burned"); plt.show()
sns.scatterplot(data=df, x="Duration", y="Calories", hue="Duration_Category"); plt.title("Workout Duration vs Calories"); plt.show()
sns.barplot(data=df, x="Duration_Category", y="Calories", errorbar=None); plt.xticks(rotation=15); plt.title("Average Calories by Duration Category"); plt.show()
sns.heatmap(df[["Duration","Pulse","Maxpulse","Calories","Calories_per_Minute","Pulse_Difference"]].corr(numeric_only=True), annot=True, cmap="coolwarm"); plt.title("Correlation Heatmap"); plt.show()

# 8. Save the cleaned and filtered results
df.to_excel("cleaned_data.xlsx", index=False)
filtered.to_excel("filtered_data.xlsx", index=False)
