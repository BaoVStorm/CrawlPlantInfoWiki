import pandas as pd

# Đọc file plants.csv
df = pd.read_csv('plants.csv', encoding='utf-8-sig')

# Các cột cần xử lý
cols = [
    'Giới (Kingdom)',
    'Nhánh (Clade)',
    'Không phân hạng',
    'Bộ (Order)',
    'Họ (Family)',
    'Chi (Genus)',
    'Loài'
]

# Kết quả lưu ở đây
results = []

for col in cols:
    # Thay '' thành NaN nếu muốn bỏ qua rỗng
    df[col] = df[col].replace('', pd.NA)

    # Đếm tần suất
    counts = df[col].value_counts(dropna=True)

    if counts.empty:
        continue  # Bỏ qua cột trống hoàn toàn

    # Giá trị lớn nhất
    max_count = counts.iloc[0]
    max_values = counts[counts == max_count].index.tolist()

    for value in max_values:
        results.append({
            'Column': col,
            'Value': value,
            'MaxCount': max_count
        })

# Chuyển thành DataFrame
result_df = pd.DataFrame(results)

print(result_df)

# Lưu ra file
result_df.to_csv('optional/plants_max_counts.csv', index=False, encoding='utf-8-sig')
