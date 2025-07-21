import json

input_file = "/raid/data/hung/tuanna/tuanna/data_repllama/implicit_2025_ground_truth.json"
output_file = "/raid/data/hung/tuanna/tuanna/data_repllama/implicit_2025_ground_truth_cleaned.json"

# Đọc file JSON đầu vào
with open(input_file, "r", encoding="latin-1") as f:
    data = json.load(f, parse_constant=lambda x: "" if x == "NaN" else x)

# Xử lý "NaN" trong positive_passages và negative_passages
for item in data:
    for passage in item["positive_passages"]:
        if passage["text"] == "NaN":
            passage["text"] = ""
    for passage in item["negative_passages"]:
        if passage["text"] == "NaN":
            passage["text"] = ""

# Lọc dữ liệu, giữ lại các item hợp lệ
n = 0
filtered_data = []
for item in data:
    if item["positive_passages"] == [] or item["negative_passages"] == []:
        n += 1
        print(f"{item['query_id']}")
    else:
        filtered_data.append(item)
print(f"Đã lọc {n} item không hợp lệ.")
# Ghi dữ liệu đã lọc vào file đầu ra
if not filtered_data:
    print("Không có dữ liệu hợp lệ để ghi vào file đầu ra.")
else:
    with open(output_file, "w", encoding="latin-1") as f:
        json.dump(filtered_data, f, indent=2, ensure_ascii=False)
    
    # Kiểm tra file đầu ra
    try:
        with open(output_file, "r", encoding="latin-1") as f:
            test_data = json.load(f)
            print("File JSON đầu ra hợp lệ!")
    except json.JSONDecodeError as e:
        print(f"Lỗi khi đọc file đầu ra: {e}")