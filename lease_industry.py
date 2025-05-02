import pandas as pd
import lease_data_cleaning
# 时间序列：
years = ['2018', '2019', '2020', '2021', '2022', '2023', '2024']

# 对于industry的统计，仅限于有value的
df = lease_data_cleaning.df
df_valid_industry = df.dropna(subset=['internal_industry'])
industries = list(set(df_valid_industry['internal_industry']))
print(len(industries))
total_count = 0
result = []
for industry in industries:
    industry_count = df_valid_industry['internal_industry'].value_counts().get(industry)
    # print(industry, industry_count)
    total_count += industry_count
    result.append([industry, int(industry_count)])

result.sort(key=lambda x: x[1], reverse=True)
print(result)


# 对于city的统计
cities = df['city'].unique() # 682
# states = df['state'].unique() # 22
# 2018 CA health 299 -> 2019 CA health -> 384
# 创建一个按 year, state, internal_industry 分组的计数表
grouped = df.dropna(subset=['internal_industry']).groupby(['year', 'state', 'internal_industry']).size().reset_index(name='count')

# state = 'CA'
industry = 'Healthcare'

# for state in states:
#     for year in years:
#         a = df_valid_industry[
#             (df_valid_industry['year'] == int(year)) &
#             (df_valid_industry['state'] == state) &
#             (df_valid_industry['internal_industry'] == industry)
#         ]
#         print(f"{year} {state} {industry} -> {len(a)}")



# 只保留有 internal_industry 的行
year_state_industry_counts = (
    df_valid_industry
    .groupby(['year', 'state', 'internal_industry'])
    .size()
    .reset_index(name='count')
)
sorted_counts = year_state_industry_counts.sort_values(['year', 'state', 'count'], ascending=[True, True, False])
years = sorted(df_valid_industry['year'].unique())
states = sorted(df_valid_industry['state'].unique())

top3_rows = []

for state in states:
    for year in years:
        subset = sorted_counts[(sorted_counts['year'] == year) & (sorted_counts['state'] == state)].head(3)
        for _, row in subset.iterrows():
            top3_rows.append({
                'year': year,
                'state': state,
                'internal_industry': row['internal_industry'],
                'count': row['count']
            })
top3_df = pd.DataFrame(top3_rows)
print(top3_df)
# top3_df.to_csv('/Users/kevinhou/Documents/DataFest_2025/derived_data/top3_state_industry.csv', index=False)




