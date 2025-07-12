import os
import pandas as pd

root_dir = r"D:\Homework\NC\original_images"

data = []

missing_all = []

for idx, folder in enumerate(os.listdir(root_dir), 1):
    folder_path = os.path.join(root_dir, folder)
    if not os.path.isdir(folder_path):
        continue

    name_plant = folder
    kingdom = ''
    clade = ''
    unranked = ''
    order = ''
    family = ''
    genus = ''
    species = ''
    description = ''
    num_images = 0

    # Đếm file ảnh
    for f in os.listdir(folder_path):
        if f.lower().endswith(('.png', '.jpg', '.jpeg')):
            num_images += 1

    description_file = os.path.join(folder_path, f"{folder}.txt")
    if os.path.isfile(description_file):
        with open(description_file, encoding='utf-8') as f:
            description = f.read().strip()

    gioi_file = os.path.join(folder_path, 'Gioi.txt')
    if os.path.isfile(gioi_file):
        with open(gioi_file, encoding='utf-8') as f:
            kingdom = f.read().strip()

    nhanh_file = os.path.join(folder_path, 'Nhanh.txt')
    if os.path.isfile(nhanh_file):
        with open(nhanh_file, encoding='utf-8') as f:
            clade = f.read().strip()

    khongphanloai_file = os.path.join(folder_path, 'KhongPhanLoai.txt')
    if os.path.isfile(khongphanloai_file):
        with open(khongphanloai_file, encoding='utf-8') as f:
            unranked = f.read().strip()

    bo_file = os.path.join(folder_path, 'Bo.txt')
    if os.path.isfile(bo_file):
        with open(bo_file, encoding='utf-8') as f:
            order = f.read().strip()

    ho_file = os.path.join(folder_path, 'Ho.txt')
    if os.path.isfile(ho_file):
        with open(ho_file, encoding='utf-8') as f:
            family = f.read().strip()

    chi_file = os.path.join(folder_path, 'Chi.txt')
    if os.path.isfile(chi_file):
        with open(chi_file, encoding='utf-8') as f:
            genus = f.read().strip()

    loai_file = os.path.join(folder_path, 'Loai.txt')
    if os.path.isfile(loai_file):
        with open(loai_file, encoding='utf-8') as f:
            species = f.read().strip()

    # append data
    data.append({
        'no': idx,
        'Folder(NamePlant)': name_plant,
        'Giới (Kingdom)': kingdom,
        'Nhánh (Clade)': clade,
        'Không phân hạng': unranked,
        'Bộ (Order)': order,
        'Họ (Family)': family,
        'Chi (Genus)': genus,
        'Loài': species,
        'Số lượng ảnh': num_images,
        'Mô tả': description
    })

    if not (os.path.isfile(gioi_file) or os.path.isfile(nhanh_file) or os.path.isfile(khongphanloai_file) or os.path.isfile(bo_file) or os.path.isfile(ho_file) or os.path.isfile(chi_file) or os.path.isfile(loai_file)):
        missing_all.append({
            'no': idx,
            'Folder(NamePlant)': name_plant
        })

df = pd.DataFrame(data)

# plants.csv
df.to_csv('plants.csv', index=False, encoding='utf-8-sig')

# summary.csv
# Cột cần check
cols_to_check = [
    'Giới (Kingdom)',
    'Nhánh (Clade)',
    'Không phân hạng',
    'Bộ (Order)',
    'Họ (Family)',
    'Chi (Genus)',
    'Loài',
    'Mô tả'
]

summary_data = {
    'Loại': ['Có giá trị', 'Không có giá trị']
}

for col in cols_to_check:
    has_value = df[col].notna().sum()
    no_value = df.shape[0] - has_value
    summary_data[col] = [has_value, no_value]

summary_df = pd.DataFrame(summary_data)

# save
summary_df.to_csv('summary.csv', index=False, encoding='utf-8-sig')

print("==== Done ====")