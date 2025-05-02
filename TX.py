from matplotlib import pyplot as plt
import pandas as pd
from DataFest_2025 import lease_data_cleaning

df = lease_data_cleaning.df
rent = 'overall_rent'
df = df.dropna(subset=[rent])
df['quarter_num'] = df['quarter'].map({'Q1': 1, 'Q2': 2, 'Q3': 3, 'Q4': 4})

years = list(range(2018, 2025))
cities = ['Houston', 'Dallas', 'Austin']
classes = ['A', 'O']

for year in years:
    plt.figure(figsize=(10, 6))
    for city in cities:
        for cls in classes:
            subset = df[
                (df['year'] == year) &
                (df['city'] == city) &
                (df['internal_class'] == cls)
            ]
            grouped = (
                subset.groupby('quarter_num')[rent]
                .mean()
                .reset_index()
                .sort_values('quarter_num')
            )
            label = f"{city} - Class {cls}"
            plt.plot(
                grouped['quarter_num'],
                grouped[rent],
                marker='o',
                label=label
            )

    plt.title(f'Rent Trend by Quarter in {year}')
    plt.xlabel('Quarter')
    plt.ylabel('Average Direct Rent')
    plt.xticks([1, 2, 3, 4], labels=['Q1', 'Q2', 'Q3', 'Q4'])
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()



df = pd.read_csv('/Users/kevinhou/Documents/DataFest_2025/derived_data/tx_.csv')
rent = 'overall_rent'
df = df.dropna(subset=[rent])
df = df[df['CBD_suburban'].isin(['CBD', 'Suburban'])]

# 1.行数统计
cbd_count = df[df['CBD_suburban'] == 'CBD'].shape[0]
suburban_count = df[df['CBD_suburban'] == 'Suburban'].shape[0]

print(f"\nNumber of rows (leases) in CBD: {cbd_count}")
print(f"Number of rows (leases) in Suburban: {suburban_count}")

# 2.年度租金走势
location_rent_trend = (
    df.groupby(['year', 'CBD_suburban'])[rent]
    .mean()
    .reset_index()
    .sort_values(['CBD_suburban', 'year'])
)

plt.figure(figsize=(10, 6))
for loc_type in ['CBD', 'Suburban']:
    loc_data = location_rent_trend[location_rent_trend['CBD_suburban'] == loc_type]
    plt.plot(
        loc_data['year'],
        loc_data[rent],
        marker='o',
        label=loc_type
    )

plt.title('CBD vs Suburban Average Rent Trend (2018–2024)')
plt.xlabel('Year')
plt.ylabel('Average Overall Rent')
plt.legend(title='Location Type')
plt.grid(True)
plt.tight_layout()
plt.show()