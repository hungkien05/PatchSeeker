import csv
import json
import re
from collections import defaultdict
import sys

# Tăng giới hạn kích thước trường của csv
csv.field_size_limit(sys.maxsize)

# Hàm xác định loại file từ đường dẫn
def get_file_type(file_path):
    extension = file_path.split('.')[-1].lower()
    if extension == 'c':
        return 'cpp'
    elif extension == 'cpp':
        return 'cpp'
    elif extension == 'py':
        return 'python'
    elif extension == 'java':
        return 'java'
    elif extension == 'cs':
        return 'cs'
    elif extension == 'js':
        return 'js'
    return None
cpp = 0
py =0 
java = 0
cs = 0
js = 0
# Hàm này sẽ được gọi để đếm số lượng file theo loại
def count_file_type(file_type):
    global cpp, py, java, cs, js
    if file_type == 'cpp':
        cpp += 1
    elif file_type == 'python':
        py += 1
    elif file_type == 'java':
        java += 1
    elif file_type == 'cs':
        cs += 1
    elif file_type == 'js':
        js += 1

# Đọc file CSV và xử lý dữ liệu
def process_csv_to_jsonl(csv_file_path):
    file_types_data = defaultdict(list)
    
    try:
        with open(csv_file_path, 'r', encoding='latin-1') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                diff = row["diff_token"]
                lines = diff.splitlines()
                for line in lines:
                    if line.startswith('--- ') or line.startswith('+++ '):
                        file_path = line.split()[1]
                        file_type = get_file_type(file_path)
                        if file_type:
                                count_file_type(file_type)
                                file_types_data[file_type].append({
                                    "nl": row["msg_token"],
                                    "diff": diff
                                })
                        break
    except Exception as e:
            print(f"Lỗi khác khi đọc file: {e}")
            return

    # Lưu vào file JSONL
    if file_types_data:
        for file_type, records in file_types_data.items():
            output_file = f"cct5_test_new_{file_type}.jsonl"
            with open(output_file, 'w', encoding='latin-1') as f:  # Lưu file JSONL luôn dùng UTF-8
                for record in records:
                    json.dump(record, f)
                    f.write('\n')
        print(f"Đã tạo các file JSONL: {', '.join([f'cct5_test_new_{ft}.jsonl' for ft in file_types_data.keys()])}")
    else:
        print("Không thể đọc file với bất kỳ mã hóa nào trong danh sách.")

# Gọi hàm
csv_file_path = "/mnt/moon-data/hung/wp1b_data_new/test_0806/429.csv"  # Thay bằng đường dẫn thực tế
process_csv_to_jsonl(csv_file_path)
print(f"Số lượng file cpp: {cpp}")
print(f"Số lượng file python: {py}")  
print(f"Số lượng file java: {java}")
print(f"Số lượng file cs: {cs}")
print(f"Số lượng file js: {js}")
