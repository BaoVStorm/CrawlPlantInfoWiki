import pandas as pd

df = pd.read_csv('plants.csv', encoding='utf-8-sig')

kingdom_col = 'Giới (Kingdom)'

df[kingdom_col] = df[kingdom_col].replace('', pd.NA)

kingdom_counts = df.groupby(kingdom_col).size().reset_index(name='Count')

kingdom_counts = kingdom_counts.sort_values(by='Count', ascending=False)

print(kingdom_counts)

kingdom_counts.to_csv('optional/plants_kingdom_counts.csv', index=False, encoding='utf-8-sig')
