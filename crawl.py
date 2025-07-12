import os
import pandas as pd

# Đường dẫn gốc
root_dir = r"D:\Homework\NC\original_images"

# List lưu dữ liệu cây
data = []

# List lưu thư mục thiếu cả 5 file txt
missing_all = []

# Duyệt qua thư mục con
for idx, folder in enumerate(os.listdir(root_dir), 1):
    folder_path = os.path.join(root_dir, folder)
    if not os.path.isdir(folder_path):
        continue

    # Các biến dữ liệu
    name_plant = folder
    kingdom = ''
    phylum = ''
    class_ = ''
    order = ''
    family = ''
    genus = ''
    description = ''
    num_images = 0

    # Đếm file ảnh
    for f in os.listdir(folder_path):
        if f.lower().endswith(('.png', '.jpg', '.jpeg')):
            num_images += 1

    # File mô tả
    description_file = os.path.join(folder_path, f"{folder}.txt")
    if os.path.isfile(description_file):
        with open(description_file, encoding='utf-8') as f:
            description = f.read().strip()

    # Các file phân loại
    gioi_file = os.path.join(folder_path, 'Gioi.txt')
    if os.path.isfile(gioi_file):
        with open(gioi_file, encoding='utf-8') as f:
            kingdom = f.read().strip()

    loai_file = os.path.join(folder_path, 'Loai.txt')
    if os.path.isfile(loai_file):
        with open(loai_file, encoding='utf-8') as f:
            phylum = f.read().strip()

    lop_file = os.path.join(folder_path, 'Lop.txt')
    if os.path.isfile(lop_file):
        with open(lop_file, encoding='utf-8') as f:
            class_ = f.read().strip()

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

    # Lưu data
    data.append({
        'no': idx,
        'Folder(NamePlant)': name_plant,
        'Giới (Kingdom)': kingdom,
        'Ngành (Phylum)': phylum,
        'Lớp (Class)': class_,
        'Bộ (Order)': order,
        'Họ (Family)': family,
        'Chi (Genus)': genus,
        'Số lượng ảnh': num_images,
        'Mô tả': description
    })

    # Kiểm tra thiếu cả 5 file
    if not (os.path.isfile(gioi_file) or os.path.isfile(loai_file) or os.path.isfile(lop_file) or os.path.isfile(bo_file) or os.path.isfile(ho_file) or os.path.isfile(chi_file)):
        missing_all.append({
            'no': idx,
            'Folder(NamePlant)': name_plant
        })

# Tạo DataFrame
df = pd.DataFrame(data)

# Lưu csv chính
df.to_csv('plants.csv', index=False, encoding='utf-8-sig')

# Tạo summary
filled = df.drop(columns=['no', 'Folder(NamePlant)', 'Số lượng ảnh', 'Mô tả']).dropna(how='all').shape[0]
missing = df.shape[0] - filled
summary_df = pd.DataFrame([
    ['Có giá trị', filled],
    ['Không có giá trị', missing]
], columns=['Loại', 'Số lượng cây'])
summary_df.to_csv('summary.csv', index=False, encoding='utf-8-sig')

# Lưu missing_all
if missing_all:
    pd.DataFrame(missing_all).to_csv('missing_all.csv', index=False, encoding='utf-8-sig')
else:
    print("Không có thư mục nào thiếu cả 5 file txt")

print("✅ Done!")
