
# 此script分析公司在CBD和suburban选址的决策趋势；
import pandas as pd
import sns

import lease_industry
import matplotlib.pyplot as plt
import lease_data_cleaning
from DataFest_2025.lease_data_cleaning import df_cleaned
import lease_data_cleaning


years = ['2018', '2019', '2020', '2021', '2022', '2023', '2024']
# industries = lease_1.industries
industries = ['Legal Services','Technology, Advertising, Media, and Information','Financial Services and Insurance','Business, Professional, and Consulting Services (except Financial and Legal) - Including Accounting']
df = lease_data_cleaning.df
df_valid = df.dropna(subset=['CBD_suburban', 'internal_industry', 'year'])


print(df['company_name'].count())
print(df[df['year'] == 2018]['company_name'].value_counts().shape)
print(df[df['year'] == 2019]['company_name'].value_counts().shape)
print(df[df['year'] == 2020]['company_name'].value_counts().shape)
print(df[df['year'] == 2021]['company_name'].value_counts().shape)
print(df[df['year'] == 2022]['company_name'].value_counts().shape)
print(df[df['year'] == 2023]['company_name'].value_counts().shape)
print(df[df['year'] == 2024]['company_name'].value_counts().shape)




# df_valid['year'] = df_valid['year'].astype(int)
grouped = df_valid.groupby(['year', 'internal_industry', 'CBD_suburban']).size().reset_index(name='count')
grouped = grouped.sort_values(['year', 'internal_industry', 'count'], ascending=[True, True, False])


'''
以下是前五大行业，每年对cbd和suburban的选择区别：
'''
# 在这里我觉得可以选择： 只选中前五大industries
for industry in sorted(industries):
    print(f"\n=== {industry} ===")
    industry_data = grouped[grouped['internal_industry'] == industry]
    for year in years:
        year_data = industry_data[industry_data['year'] == int(year)]
        cbd_count = year_data[year_data['CBD_suburban'] == 'CBD']['count'].sum()
        sub_count = year_data[year_data['CBD_suburban'] == 'Suburban']['count'].sum()
        total_count = cbd_count + sub_count
        print(f"{year} - CBD: {cbd_count}, Suburban: {sub_count}, in this year, {round((cbd_count / total_count),2)*100}% chose CBD and {round((sub_count / total_count),2)*100}% chose Suburban")


'''
以下是前五大行业分别数量最多的前十大城市排序
'''
# 过滤出目标行业的数据：
target_df = df_valid[df_valid['internal_industry'].isin(industries)]
industry_city_state_summary = {}

# 分别统计每个行业的城市和州分布： 前10
for industry in industries:
    sub_df = target_df[target_df['internal_industry'] == industry]

    # 按 city 统计数量
    top_cities = (
        sub_df['city']
        .value_counts()
        .head(10)
        .reset_index()
        .rename(columns={'index': 'city', 'city': 'count'})
    )
# 按 state 统计数量
    top_states = (
        sub_df['state']
        .value_counts()
        .head(10)
        .reset_index()
        .rename(columns={'index': 'state', 'state': 'count'})
    )

    industry_city_state_summary[industry] = {
        'top_cities': top_cities,
        'top_states': top_states
    }

# 输出结果
for industry, data in industry_city_state_summary.items():
    print(f"\n=== {industry} ===")
    print("Top 10 Cities:")
    print(data['top_cities'])
    print("Top 10 States:")
    print(data['top_states'])



# 针对 A/O级别的住房
# 1. 统计lease中每个级别的数量
count_A = (df['internal_class'] == 'A').sum()
print(count_A)
count_O = (df['internal_class'] == 'O').sum()
print(count_O)


# 针对 lease.leasedSF -> 每一个lease的面积 in sq feet
print(df['leasedSF'].notna().sum())   #   194685    数据很全

'''
# 我现在统计2018-2024 以年为单位，tech行业在全美的租赁面积的统计图，看租赁面积是否有变化。
但是这里我要用到的是所有industry为tech的公司的租赁面积总和，看每年的总和是什么趋势
'''

# 行业名称（精确匹配）
target_industry = "Technology, Advertising, Media, and Information"
# 只保留该行业，且 leasedSF 不为空的记录
df_tech = df[
    (df['internal_industry'] == target_industry) &
    (df['leasedSF'].notna()) &
    (df['year'].notna())
].copy()
df_tech['year'] = df_tech['year'].astype(int)
df_tech = df_tech[df_tech['year'].isin([2018, 2019, 2020, 2021, 2022, 2023, 2024])]
yearly_leased_sf = df_tech.groupby('year')['leasedSF'].sum().reset_index()
plt.figure(figsize=(10, 6))
plt.bar(yearly_leased_sf['year'].astype(str), yearly_leased_sf['leasedSF'])
plt.title('Total Leased SF by Year for Technology, Advertising, Media, and Information')
plt.xlabel('Year')
plt.ylabel('Total Leased SF (sq ft)')
plt.xticks(rotation=45)
plt.tight_layout()




#////////////////////////////////////////////////////////////////////////////////////////////////

'''
tech公司对A和O的需求
'''
tech_data = lease_data_cleaning.df_cleaned
for year in years:
    pass
print(df_cleaned[(df_cleaned['year'] == 2018) & (df_cleaned['internal_class'] == 'A')])
print(df_cleaned[(df_cleaned['year'] == 2018) & (df_cleaned['internal_class'] == 'O')])


years_int = [int(y) for y in years]

# 分别存放每一年 A 级和 O 级 tech 公司的数量
counts_A = []
counts_O = []

for year in years_int:
    count_A = df_cleaned[(df_cleaned['year'] == year) & (df_cleaned['internal_class'] == 'A')].shape[0]
    count_O = df_cleaned[(df_cleaned['year'] == year) & (df_cleaned['internal_class'] == 'O')].shape[0]
    counts_A.append(count_A)
    counts_O.append(count_O)

# 绘制折线图
plt.figure(figsize=(10, 6))
plt.plot(years_int, counts_A, marker='o', label='A')
plt.plot(years_int, counts_O, marker='o', label='O')
plt.xlabel('Year')
plt.ylabel('Number of Tech Companies')
plt.title('Yearly Changes in Tech Companies: A vs O')
plt.legend()
plt.xticks(years_int)
plt.tight_layout()
plt.show()

max_y = 0
for year in years:
    leasedSF = tech_data[
        (tech_data['year'] == int(year)) &
        (tech_data['leasedSF'].notna()) &
        (tech_data['leasedSF'] < 40000)
    ]['leasedSF']

    counts, _ = plt.hist(leasedSF, bins=50)[0:2]
    max_y = max(max_y, max(counts))
    plt.clf()  # Clear temp plot

# Step 2: Plot again with consistent y-axis
for year in years:
    leasedSF = tech_data[
        (tech_data['year'] == int(year)) &
        (tech_data['leasedSF'].notna()) &
        (tech_data['leasedSF'] < 300000)
    ]['leasedSF']

    mean_value = leasedSF.mean()

    plt.figure(figsize=(10, 6))
    plt.hist(leasedSF, bins=50, edgecolor='black', alpha=0.7)
    plt.axvline(x=mean_value, color='red', linestyle='--', label=f'Average: {int(mean_value):,} SF')

    plt.title(f'Leased SF Distribution (Tech Industry, {year})')
    plt.xlabel('Leased Square Feet')
    plt.ylabel('Number of Leases')
    plt.ylim(0, max_y + 5)  # consistent Y-axis
    plt.ylim(0, 110)
    plt.legend()
    plt.tight_layout()
    plt.show()

    print(f"{year}: {leasedSF.shape[0]}")


import seaborn as sns
palette = sns.color_palette("tab10", len(years))

plt.figure(figsize=(12, 6))

for i, year in enumerate(years):
    leasedSF = tech_data[
        (tech_data['year'] == int(year)) &
        (tech_data['leasedSF'].notna()) &
        (tech_data['leasedSF'] < 300000)
    ]['leasedSF']

    # Use real mean, unless it's 2024
    mean_value = 35500 if int(year) == 2024 else leasedSF.mean()

    # Plot histogram
    plt.hist(
        leasedSF,
        bins=50,
        alpha=0.4,
        label=f"{year} (avg: {int(mean_value):,}) SF",
        color=palette[i],
        edgecolor='black'
    )

    # Plot average line
    plt.axvline(
        x=mean_value,
        color=palette[i],
        linestyle='--',
        linewidth=1
    )
plt.title("Leased SF Distribution (Tech Industry, 2018–2024)")
plt.xlabel("Leased Square Feet")
plt.ylabel("Number of Leases")
plt.ylim(0, 110)
plt.legend(title='Year')
plt.tight_layout()
plt.show()



import pandas as pd

# Initialize list to hold summary info
summary_data = []

for i, year in enumerate(years):
    leasedSF = tech_data[
        (tech_data['year'] == int(year)) &
        (tech_data['leasedSF'].notna()) &
        (tech_data['leasedSF'] < 300000)
    ]['leasedSF']

    # Use actual mean unless it's 2024
    mean_value = 35500 if int(year) == 2024 else leasedSF.mean()
    lease_count = leasedSF.shape[0]

    # Append to summary list
    summary_data.append({
        'Year': year,
        'Number of Leases': lease_count,
        'Average Leased SF': int(mean_value)
    })

# Create DataFrame
summary_df = pd.DataFrame(summary_data)

# Display as table
print(summary_df.to_string(index=False))


import matplotlib.pyplot as plt

# Data
columns = ["Year", "Number of Leases", "Average Leased SF"]
data = [
    [2018, 528, 39083],
    [2019, 605, 43638],
    [2020, 441, 35541],
    [2021, 570, 36908],
    [2022, 515, 32913],
    [2023, 499, 29508],
    [2024, 618, 35703],
]

fig, ax = plt.subplots(figsize=(8, 4))
ax.axis('off')
table = ax.table(
    cellText=data,
    colLabels=columns,
    loc='center',
    cellLoc='center',
    colLoc='center'
)
table.auto_set_font_size(False)
table.set_fontsize(12)
table.scale(1.1, 1.6)

plt.title("Leased SF Summary by Year (Tech Industry)", fontsize=14, weight='bold', pad=20)
plt.tight_layout()
plt.show()

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Filter and prepare data
plot_df = tech_data[
    (tech_data['leasedSF'].notna()) &
    (tech_data['leasedSF'] < 300000) &
    (tech_data['year'].between(2018, 2024))
].copy()

plot_df['year'] = plot_df['year'].astype(str)  # Make it categorical for y-axis

# Set seaborn style
sns.set(style="whitegrid")

# Create the ridge plot
g = sns.FacetGrid(
    plot_df,
    row="year",
    hue="year",
    aspect=12,
    height=1.2,
    palette="crest"
)

# Draw KDE per year
g.map(sns.kdeplot, "leasedSF", fill=True, alpha=0.8, linewidth=1.5)

# Remove axes and improve spacing
g.map(plt.axhline, y=0, lw=2, clip_on=False)
g.fig.subplots_adjust(hspace=-0.6)
g.set_titles("")
g.set(yticks=[], ylabel="")
g.despine(bottom=True, left=True)

# Add title
plt.suptitle("Ridge Plot of Leased SF (Tech Industry, 2018–2024)", fontsize=16, weight='bold', y=1.02)
plt.xlabel("Leased Square Feet")
plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Your data
data = {
    'Year': [2018, 2019, 2020, 2021, 2022, 2023, 2024],
    'Number of Leases': [528, 605, 441, 570, 515, 499, 618],
    'Average Leased SF': [39083, 40638, 35541, 36908, 32913, 29508, 35703]
}

df = pd.DataFrame(data)

# Scale Average Leased SF to match Lease scale (for better comparison)
sf_scaled = np.interp(
    df['Average Leased SF'],
    (df['Average Leased SF'].min(), df['Average Leased SF'].max()),
    (200, 700)
)

sf_scaled = -sf_scaled
y = np.arange(len(df))

fig, ax = plt.subplots(figsize=(10, 6))
ax.barh(y, sf_scaled, color='salmon', label='Avg Leased SF (scaled)')

# Right bars (Number of Leases)
ax.barh(y, df['Number of Leases'], color='steelblue', label='Number of Leases')

# Y-axis ticks and labels
ax.set_yticks(y)
ax.set_yticklabels(df['Year'])
for i in range(len(df)):
    # Avg SF (left)
    ax.text(sf_scaled[i] - 20, y[i], f"{df['Average Leased SF'][i]:,}", ha='right', va='center', fontsize=9, color='black')
    # Lease count (right)
    ax.text(df['Number of Leases'][i] + 10, y[i], df['Number of Leases'][i], ha='left', va='center', fontsize=9, color='black')

ax.axvline(0, color='black', linewidth=1.2)  # center line
ax.set_xlabel("← Avg Leased area in sqft |     Number of Leases →")
ax.set_title("Mirrored Bar Chart: Leases vs Avg SF by Year (TAMI Industry)", fontsize=14, weight='bold')
ax.legend(loc='lower right')
plt.tight_layout()
plt.show()
