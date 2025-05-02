import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm

import lease_data_cleaning
# Load the cleaned DataFrame (you already have this)
df = lease_data_cleaning.df_cleaned

cities = ['Austin', 'Atlanta', 'Houston', 'San Francisco']
# Filter relevant rows
df = df[
    (df['city'].isin(cities)) &
    (df['transaction_type'] == 'New') &
    (df['year'].between(2018, 2024)) &
    (df['quarter'].notna())
].copy()

# Convert quarter to datetime for plotting
quarter_map = {'Q1': '01', 'Q2': '04', 'Q3': '07', 'Q4': '10'}
df['date'] = pd.to_datetime(df['year'].astype(str) + '-' + df['quarter'].map(quarter_map) + '-01')

# Count new leases per city per quarter
grouped = df.groupby(['city', 'date']).size().reset_index(name='count')

# Add date ordinal for regression
grouped['date_ordinal'] = grouped['date'].map(lambda x: x.toordinal())

# Filter cities with enough data to regress on
valid_cities = grouped['city'].value_counts()[lambda x: x > 1].index.tolist()

# Plot scatter + fitted trendlines
plt.figure(figsize=(12, 6))
sns.set(style="whitegrid")

for city in valid_cities:
    city_data = grouped[grouped['city'] == city]

    # Scatter plot
    plt.scatter(city_data['date'], city_data['count'], label=city, alpha=0.6)

    # Linear regression
    X = sm.add_constant(city_data['date_ordinal'])
    y = city_data['count']
    model = sm.OLS(y, X).fit()
    y_pred = model.predict(X)

    # Trend line
    plt.plot(city_data['date'], y_pred, label=f"{city} Trend")

plt.title("Linear Regression on New Lease Trends by City (2018–2024)")
plt.xlabel("Quarter")
plt.ylabel("Number of New Leases")
plt.legend(title='City')
plt.grid(True)
plt.tight_layout()
plt.show()


print(grouped['city'].value_counts())