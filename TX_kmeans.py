import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
df = pd.read_csv("/Users/kevinhou/Documents/DataFest_2025/2025 ASA DataFest-update2-2025-03-19/Leases.csv")

target_industry = "Technology, Advertising, Media, and Information"
df = df[df["internal_industry"] == target_industry]

grouped = df.groupby("market").agg({
    "leasedSF": "mean",
    "overall_rent": "mean",
    "availability_proportion": "mean"
}).dropna()
# grouped = df.groupby("market").agg({
#     "leasedSF": "mean",
#     "overall_rent": "mean",
#     "availability_proportion": "mean",
#     "available_space": "mean",
#     "RBA": "mean",
#     "sublet_availability_proportion": "mean"
# }).dropna()

print(f"市场样本数量（仅 TAMI 行业）: {len(grouped)}")

if len(grouped) < 2:
    raise ValueError("样本数量太少，无法聚类")

scaler = StandardScaler()
X_scaled = scaler.fit_transform(grouped)

k = min(4, len(grouped))  # 最多4类
print(f"聚类数量设为: {k}")

kmeans = KMeans(n_clusters=k, random_state=42)
grouped["cluster"] = kmeans.fit_predict(X_scaled)

fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

x = grouped["leasedSF"]
y = grouped["overall_rent"]
z = grouped["availability_proportion"]
colors = grouped["cluster"]

scatter = ax.scatter(
    x, y, z,
    c=colors,
    cmap="Set1",
    s=100,
    edgecolor='k'
)

# 添加市场标签
for i, market in enumerate(grouped.index):
    ax.text(x.iloc[i], y.iloc[i], z.iloc[i], market, fontsize=8)

ax.set_title("3D K-means Clustering of TAMI Office Markets")
ax.set_xlabel("Avg Leased SF (TAMI)")
ax.set_ylabel("Avg Rent ($/SF)")
ax.set_zlabel("Availability %")
plt.tight_layout()
plt.show()

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt

# Group by market and calculate mean values
grouped = df.groupby("market").agg({
    "leasedSF": "mean",
    "overall_rent": "mean"
}).dropna()

print(f"Number of markets (TAMI only): {len(grouped)}")

if len(grouped) < 2:
    raise ValueError("Too few samples to perform clustering.")

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(grouped)

# Determine number of clusters
k = min(4, len(grouped))
print(f"Number of clusters: {k}")

# K-means clustering
kmeans = KMeans(n_clusters=k, random_state=42)
grouped["cluster"] = kmeans.fit_predict(X_scaled)

# 2D visualization
plt.figure(figsize=(10, 6))
plt.scatter(
    grouped["leasedSF"],
    grouped["overall_rent"],
    c=grouped["cluster"],
    cmap="Set1",
    s=100,
    edgecolor="k"
)

# Market labels
for i, market in enumerate(grouped.index):
    plt.text(
        grouped["leasedSF"].iloc[i],
        grouped["overall_rent"].iloc[i],
        market,
        fontsize=8,
        ha='right'
    )

plt.title("2D K-means Clustering of TAMI Office Markets")
plt.xlabel("Average Leased SF")
plt.ylabel("Average Rent ($/SF)")
plt.grid(True)
plt.tight_layout()
plt.show()
