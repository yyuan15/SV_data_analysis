import pandas as pd


# 只保留tech行业
df = pd.read_csv('/Users/kevinhou/Documents/DataFest_2025/2025 ASA DataFest-update2-2025-03-19/Leases.csv')
df_cleaned = df[df['internal_industry'] == 'Technology, Advertising, Media, and Information']
print(df_cleaned.shape)

# df_cleaned.to_csv('/Users/kevinhou/Documents/DataFest_2025/2025 ASA DataFest-update2-2025-03-19/cleaned_leases.csv')

