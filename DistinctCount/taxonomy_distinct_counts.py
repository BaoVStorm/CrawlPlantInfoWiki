import pandas as pd

# Đọc file CSV
df = pd.read_csv('plants.csv', encoding='utf-8-sig')

# Các cột gốc
taxonomy_cols = [
    'no',
    'Folder(NamePlant)',
    'Giới (Kingdom)',
    'Nhánh (Clade)',
    'Không phân hạng',
    'Bộ (Order)',
    'Họ (Family)',
    'Chi (Genus)',
    'Loài'
]

taxonomy_df = df[taxonomy_cols].copy()

# Tạo cột mới Nhánh_KPH: gộp Nhánh (Clade) và Không phân hạng
def merge_clade_unranked(row):
    clade = str(row['Nhánh (Clade)']) if pd.notna(row['Nhánh (Clade)']) else ''
    unranked = str(row['Không phân hạng']) if pd.notna(row['Không phân hạng']) else ''
    if clade and unranked:
        return clade + '\n' + unranked
    else:
        return clade or unranked

taxonomy_df['Nhánh_KPL'] = taxonomy_df.apply(merge_clade_unranked, axis=1)

# Danh sách cột cần xử lý
all_cols = [
    'Giới (Kingdom)',
    'Nhánh (Clade)',
    'Không phân hạng',
    'Nhánh_KPL',
    'Bộ (Order)',
    'Họ (Family)',
    'Chi (Genus)',
    'Loài'
]

results = []

for col in all_cols:
    # Tách theo \n, explode
    exploded = taxonomy_df[col].dropna().astype(str).str.split('\n').explode().str.strip()
    exploded = exploded[exploded != '']

    # Tạo DataFrame distinct
    unique_values = exploded.drop_duplicates().sort_values().reset_index(drop=True).to_frame(name='Value')

    # Lưu ra file CSV, thay dấu cách & dấu đặc biệt bằng _
    safe_col_name = col.replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_')
    file_name = f'distinct_{safe_col_name}.csv'
    unique_values.to_csv('DistinctCount/taxonomy/' + file_name, index=False, encoding='utf-8-sig')

    # Cũng lưu số lượng để tổng hợp
    results.append({'Column': col, 'DistinctCount': unique_values.shape[0]})

# Tạo tổng hợp
distinct_df = pd.DataFrame(results)
print(distinct_df)

distinct_df.to_csv('DistinctCount/taxonomy_distinct_counts.csv', index=False, encoding='utf-8-sig')
