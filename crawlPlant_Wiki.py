import os
import requests
from bs4 import BeautifulSoup

base_dir = r"D:\Homework\NC\original_images"  

label_to_filename = {
    "Giới": "Gioi.txt",
    "Bộ": "Bo.txt",
    "Họ": "Ho.txt",
    "Chi": "Chi.txt",
    "Loài": "Loai.txt",
    "nhánh": "Nhanh.txt",
    "(không phân hạng)": "KhongPhanLoai.txt",
    "không phân hạng": "KhongPhanLoai.txt"
}

def save_text_append(folder, filename, content):
    path = os.path.join(folder, filename)
    with open(path, "a", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"=== Đã ghi thêm vào {filename}")

def remove_old_taxonomy_files(folder):
    for fname in label_to_filename.values():
        file_path = os.path.join(folder, fname)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"=== Đã xoá {fname} trong {folder}")

def crawl_taxonomy(scientific_name, folder_path):
    url = r"https://vi.wikipedia.org/wiki/" + scientific_name

    response = requests.get(url)

    if response.status_code != 200:
        print(f"=== Không truy cập được {url}")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", class_="infobox taxobox")
    if not table:
        print(f"=== Không tìm thấy bảng phân loại ở {scientific_name}")
        return

    trs = table.find_all("tr")

    for tr in trs:
        label = ""
        content = ""

        tds = tr.find_all("td")
        if len(tds) == 2:
            # Case: <td><td>
            label = tds[0].get_text(strip=True).rstrip(":")
            content = tds[1].get_text(strip=True)

        elif tr.find("th") and tr.find("td"):
            # Case: <th><td>
            th = tr.find("th")
            td = tr.find("td")
            label = th.get_text(strip=True).rstrip(":")
            content = td.get_text(strip=True)

        if not label:
            continue

        for key in label_to_filename:
            if label == key or label.lower().startswith(key.lower()):
                filename = label_to_filename[key]
                save_text_append(folder_path, filename, content)
                break

# === Chạy toàn bộ ===
def main():
    missing_data = [] 

    for folder in os.listdir(base_dir):
        folder_path = os.path.join(base_dir, folder)
        if os.path.isdir(folder_path):
            print(f"\n=== Đang xử lý: {folder}")
            remove_old_taxonomy_files(folder_path)
            crawl_taxonomy(folder, folder_path)

            # Sau khi crawl xong → kiểm tra các file taxonomy
            has_taxonomy = False
            for fname in ["Gioi.txt", "Bo.txt", "Ho.txt", "Chi.txt", "Loai.txt", "Nhanh.txt"]:
                if os.path.exists(os.path.join(folder_path, fname)):
                    has_taxonomy = True
                    break

            if not has_taxonomy:
                print(f"=== Không có thông tin phân loại cho: {folder}")
                missing_data.append(folder)

    if missing_data:
        df_missing = pd.DataFrame(missing_data, columns=["Missing Taxonomy"])
        output_path = os.path.join(base_dir, "missing_taxonomy.csv")
        df_missing.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"\n=== Đã lưu danh sách thiếu taxonomy vào: {output_path}")
    else:
        print("\n=== Tất cả cây đều có dữ liệu taxonomy.")

if __name__ == "__main__":
    main()
