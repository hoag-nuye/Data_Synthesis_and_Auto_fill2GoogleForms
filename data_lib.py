# PHẦN XỬ LÝ TIỀN DỮ LIỆU NÊN LÀM TRÊN jupyter notebook hay colab
# The pre-processing of data should be done at jupyter or colab

import pandas as pd
from faker import Faker
from collections import Counter
import random

df_path = 'data/khaosat_hieubietkinhte_ydinhkhoinghiep.csv'
df = pd.read_csv(df_path)

num_record_added = 100

# ====================PREPROCESSING DATA =================
# --------------------(Handling Outliers)----------------
# Nhìn vào biểu thị excel => xoá 12 cột đầu
df = df.drop(df.index[0:12])
# Xoá toàn bộ các cột trống 100 %
# Drop all 100% empty columns
df = df.dropna(axis=1, how='all')
# Xoá trường thông tin Dấu thời gian
df = df.drop(columns=['Dấu thời gian'])
# Review columns which is empty
print(type(df.isna().sum()))

# ---------------------(Data Augmentation)------------------
new_data = {}

# 1 : CREATE N RECORD of 'Địa chỉ email' clm
# Tao gmail bang thu vien faker
fake = Faker('vi_VN')

# Tao ra list chu ten nam, nu, sau đó kiểm tra tên xem nó có nằm trong gmail không để xác định giới
# tính cho gmail
# Tạo số lượng lớn tên giả để phân tích
male_names = [fake.first_name_male() for _ in range(1000)]
female_names = [fake.first_name_female() for _ in range(1000)]

# Lấy 50 từ phổ biến nhất
male_keywords = Counter([name.lower() for name in male_names]).most_common(50)
female_keywords = Counter([name.lower() for name in female_names]).most_common(50)

# Lấy danh sách từ khóa chỉ chứa tên
male_keywords = [item[0] for item in male_keywords]
female_keywords = [item[0] for item in female_keywords]

# Sử dụng từ khóa để dự đoán giới tính
def predict_gender_from_gmail(gmail):
    name_part = gmail.split('@')[0]  # Lấy phần trước dấu @ trong email
    name_part = name_part.lower()  # Chuyển tên thành chữ thường để so sánh

    # Kiểm tra xem tên chứa từ khóa nữ
    for keyword in female_keywords:
        if keyword in name_part:
            return 'Nữ'

    # Kiểm tra xem tên chứa từ khóa nam
    for keyword in male_keywords:
        if keyword in name_part:
            return 'Nam'

    # Nếu không dự đoán được, chọn ngẫu nhiên giới tính
    return random.choice(['Nam', 'Nữ'])

# 2 : CREATE N RECORD of '1. Giới tính của bạn:'

new_emails = []
new_genders = []
existing_emails = df['Địa chỉ email'].values.tolist()

# Tạo Gmail và dự đoán giới tính dựa trên tên
N = 300
for _ in range(N):
    # tao gmail
    new_email = fake.email()
    # tao ra gmail den khi nao khong trung voi email cu thi thoi : RAT LAU :V
    while new_email in existing_emails:
        new_email = fake.email()

    # Tao gio tinh
    new_gender = predict_gender_from_gmail(new_email)

    new_emails.append(new_email)
    new_genders.append(new_gender)
    existing_emails.append(new_email)

#Them vao dictionary du lieu moi
new_data['Địa chỉ email'] = new_emails
new_data['1. Giới tính của bạn:'] = new_genders
# 3 : CREATE N RECORD of rest columns with normalize
for column_name, column_data in df.items():
    # Lấy tỷ lệ xuất hiện của từng giá trị unique trong cột
    value_proportion = column_data.value_counts(normalize=True)
    # Tạo 600 giá trị mới dựa trên tỷ lệ của dữ liệu cũ
    new_data[column_name] = random.choices(value_proportion.index, weights=value_proportion.values, k=N)

print('====================== COMPARE DATA ==================')
for (colum_name), (new_data_key, _) in zip(df.columns, new_data.items()):
    print(f'{column_name.strip() == new_data_key.strip()} == {colum_name} -- {new_data_key}')
    # print(type(column_name), type(new_data_key))
    print(len(column_name), len(new_data_key))

# NOTE : TÊN CỦA DF COLUMN CÓ THỂ SẼ KHÁC KHI TẠO NHƯNG HIỂN THỊ VẪN THẾ

# ============== LƯU FILE ===================
import os
# Tên file Excel
# Lấy phần đường dẫn trước tên tệp
directory_path = os.path.dirname(df_path)
file_name = '{}/new_data_of_{}'.format(directory_path, df_path.split('/')[-1])
# Xóa file cũ nếu nó tồn tại
if os.path.exists(file_name):
    os.remove(file_name)

# Chuyển dictionary thành DataFrame
df = pd.DataFrame(new_data)

# Lưu DataFrame thành file Excel
df.to_csv(file_name, index=False)
print(f"File {file_name} đã được tạo lại với dữ liệu mới.")
