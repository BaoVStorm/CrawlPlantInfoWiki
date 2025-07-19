import pandas as pd
import os
import shutil

# ============= 1. SETUP ==============

# Đường dẫn gốc chứa cây
root_dir = r"D:\Homework\NC\original_images"

# Đường dẫn output
output_dir = r"E:\output_images"

# Đọc file plants.csv
df = pd.read_csv('plants.csv', encoding='utf-8-sig')

# Danh sách phân loại và số ảnh (số ảnh không cần thiết ở bước này)
all_cols = {
    # 'Giới (Kingdom)': 200,
    # 'Nhánh (Clade)': 150,
    # 'Không phân hạng': 150,
    'Nhánh_KPL': 150,
    'Bộ (Order)': 100,
    'Họ (Family)': 80,
    'Chi (Genus)': 40,
    # 'Loài': 20
}

# Tạo cột mới Nhánh_KPL nếu chưa có (phòng khi plants.csv chưa có sẵn)
if 'Nhánh_KPL' not in df.columns:
    def merge_clade_unranked(row):
        clade = str(row['Nhánh (Clade)']) if pd.notna(row['Nhánh (Clade)']) else ''
        unranked = str(row['Không phân hạng']) if pd.notna(row['Không phân hạng']) else ''
        if clade and unranked:
            return clade + '\n' + unranked
        else:
            return clade or unranked

    df['Nhánh_KPL'] = df.apply(merge_clade_unranked, axis=1)

# Kết quả lưu ở đây
result_dict = {}

for col, _ in all_cols.items():
    # Đọc file distinct tương ứng
    safe_col_name = col.replace(' ', '_').replace('(', '').replace(')', '').replace('/', '_')
    distinct_file = f'DistinctCount/taxonomy/distinct_{safe_col_name}.csv'

    # Đọc các giá trị distinct
    distinct_df = pd.read_csv(distinct_file, encoding='utf-8-sig')
    distinct_values = distinct_df['Value'].dropna().astype(str).tolist()

    # Tạo dict con cho từng giá trị
    value_dict = {}

    for value in distinct_values:
        index_list = []

        # Với mỗi dòng, kiểm tra giá trị có nằm trong ô không
        for idx, cell in df[col].dropna().astype(str).items():
            items = [item.strip() for item in cell.split('\n') if item.strip()]
            if value in items:
                index_list.append(idx)

        value_dict[value] = index_list

    result_dict[col] = value_dict

# print(result_dict)

# ============= 2. BẮT ĐẦU LẶP ==============

for col, max_images in all_cols.items():
    value_dict = result_dict[col]

    for value, index_list in value_dict.items():
        print(f"Đang xử lý: Phân loại {col} - Giá trị {value}")

        # --- 2.1 Lấy số lượng ảnh ban đầu ---
        image_counts = df.loc[index_list, 'Số lượng ảnh'].astype(int).tolist()

        total_images = sum(image_counts)

        # --- 2.2 Nếu nhỏ hơn giới hạn, giữ nguyên ---
        if total_images <= max_images:
            final_counts = image_counts.copy()
        else:
            # --- 2.3 Giảm đồng đều ---
            n = len(image_counts)
            # Phân phối đều trước
            avg = max_images // n
            final_counts = [min(count, avg) for count in image_counts]

            # Nếu vẫn dư, phân phối phần dư
            diff = max_images - sum(final_counts)
            i = 0
            while diff > 0:
                if final_counts[i] < image_counts[i]:
                    final_counts[i] += 1
                    diff -= 1
                i = (i + 1) % n

        print(f"Số lượng ảnh ban đầu: {image_counts}")
        print(f"Số lượng ảnh đã điều chỉnh: {final_counts}")
        print("------------------------")

        # --- 2.4 Copy ảnh ---
        for idx, num_images in zip(index_list, final_counts):
            row = df.iloc[idx]
            folder_name = row['Folder(NamePlant)']

            src_folder = os.path.join(root_dir, folder_name)
            dst_folder = os.path.join(output_dir, col, value)

            os.makedirs(dst_folder, exist_ok=True)

            # Liệt kê ảnh gốc
            images = [f for f in os.listdir(src_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

            # Lấy đúng số ảnh (nếu ít hơn thì lấy hết)
            selected_images = images[:num_images]

            for img_name in selected_images:
                src_img = os.path.join(src_folder, img_name)
                dst_img = os.path.join(dst_folder, f"{folder_name}_{img_name}")
                shutil.copy2(src_img, dst_img)
