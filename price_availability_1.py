import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import lease_data_cleaning
# 加载数据
df = lease_data_cleaning.df
df = df.dropna(subset=['direct_internal_class_rent'])
df['quarter_num'] = df['quarter'].map({'Q1': 1, 'Q2': 2, 'Q3': 3, 'Q4': 4})
tech_states = ['NY', 'CA', 'VA', 'TX', 'IL', 'WA', 'GA', 'DC', 'MA', 'FL']


sample_state = 'TX'
years_to_include = list(range(2018, 2025))
filtered_df = df[(df['state'] == sample_state) & (df['year'].isin(years_to_include))]

# 按 internal_class 分别分析
for cls in ['A', 'O']:
    class_df = filtered_df[filtered_df['internal_class'] == cls]

    # 时间序列图 - 空置率
    vacancy_by_quarter = (
        class_df.groupby(['year', 'quarter'])['availability_proportion']
        .mean()
        .reset_index()
    )
    vacancy_by_quarter['quarter_num'] = vacancy_by_quarter['quarter'].map({'Q1':1, 'Q2':2, 'Q3':3, 'Q4':4})
    vacancy_by_quarter = vacancy_by_quarter.sort_values(['year', 'quarter_num'])

    # 时间序列图 - 租金
    rent_by_quarter = (
        class_df.groupby(['year', 'quarter'])['direct_internal_class_rent']
        .mean()
        .reset_index()
    )
    rent_by_quarter['quarter_num'] = rent_by_quarter['quarter'].map({'Q1':1, 'Q2':2, 'Q3':3, 'Q4':4})
    rent_by_quarter = rent_by_quarter.sort_values(['year', 'quarter_num'])

    # 两图合并展示
    fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)
    for year in vacancy_by_quarter['year'].unique():
        data = vacancy_by_quarter[vacancy_by_quarter['year'] == year]
        axs[0].plot(data['quarter'], data['availability_proportion'], marker='o', label=str(year))
    axs[0].set_title(f'Vacancy Rate in {sample_state} ({cls}-Class)')
    axs[0].set_ylabel('Vacancy Rate')
    axs[0].set_ylim(0.15, 0.4)
    axs[0].legend(title='Year')
    axs[0].grid(True)

    for year in rent_by_quarter['year'].unique():
        data = rent_by_quarter[rent_by_quarter['year'] == year]
        axs[1].plot(data['quarter'], data['direct_internal_class_rent'], marker='o', label=str(year))
    axs[1].set_title(f'Rent Trend in {sample_state} ({cls}-Class)')
    axs[1].set_xlabel('Quarter')
    axs[1].set_ylabel('Direct Rent')
    axs[1].legend(title='Year')
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()

    # --- OLS 回归 ---
    grouped = (
        class_df.groupby(['year', 'quarter_num'])[['availability_proportion', 'direct_internal_class_rent']]
        .mean()
        .reset_index()
    )

    X = grouped['availability_proportion']
    y = grouped['direct_internal_class_rent']
    X_ols = sm.add_constant(X)
    model = sm.OLS(y, X_ols).fit()
    print(f"\nOLS Regression Summary for Class {cls} in {sample_state}:\n")
    print(model.summary())

    # 回归图
    sns.lmplot(
        x='availability_proportion',
        y='direct_internal_class_rent',
        data=grouped,
        aspect=1.5,
        scatter_kws={"s": 60, "alpha": 0.7}
    )
    plt.title(f'Vacancy vs Rent ({cls}-Class, {sample_state})')
    plt.xlabel('Availability Proportion')
    plt.ylabel('Direct Internal Class Rent')
    plt.tight_layout()
    plt.show()



import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 加载数据
df = df.dropna(subset=['direct_internal_class_rent'])

tech_states = ['NY', 'CA', 'VA', 'TX', 'IL', 'WA', 'GA', 'DC', 'MA', 'FL']
df_tech = df[df['state'].isin(tech_states)]

# 计算每个州按 internal_class 分组的平均租金
avg_rent_by_state_class = (
    df_tech.groupby(['state', 'internal_class'])['direct_internal_class_rent']
    .mean()
    .reset_index()
    .sort_values(by='direct_internal_class_rent', ascending=False)
)

print(avg_rent_by_state_class)

# 可视化：分 A/O 两种楼
plt.figure(figsize=(12, 6))
sns.barplot(
    data=avg_rent_by_state_class,
    x='state',
    y='direct_internal_class_rent',
    hue='internal_class',
    palette='Set2'
)
plt.title('Average Direct Rent by State and Building Class (Tech States)')
plt.ylabel('Average Direct Internal Class Rent')
plt.xlabel('State')
plt.legend(title='Building Class')
plt.grid(axis='y')
plt.tight_layout()
plt.show()
