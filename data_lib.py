# PHẦN XỬ LÝ TIỀN DỮ LIỆU NÊN LÀM TRÊN jupyter notebook hay colab
# The pre-processing of data should be done at jupyter or colab

import pandas as pd
from faker import Faker
import unidecode

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
print(df.columns.shape)
# ---------------------(Handling Outliers) ----------------

# XỬ LÝ OUTLIERS

# ---------------------(Data Augmentation)------------------
new_data = {}

# 1 : CREATE N RECORD of 'Địa chỉ email' clm
# Tao gmail bang thu vien faker
fake = Faker('vi_VN')

# # Nếu không dự đoán được, chọn ngẫu nhiên giới tính
# return random.choice(['Nam', 'Nữ'])

# 2 : CREATE N RECORD of '1. Giới tính của bạn:'
# Tạo danh sách các tên miền với tỉ lệ `@gmail.com` chiếm 90%
domains = ["@gmail.com"] * 90 + ["@hvnh.edu.vn"] *10 +["@icloud.com"]

# Hàm để tạo tên không có dấu
def remove_accents(text):
    return unidecode.unidecode(text)
def generate_realistic_email(gender):

    first_name = fake.first_name_male().lower() if gender == 'male' \
        else random.choice([fake.first_name_female().lower(), fake.first_name_male().lower()])
    middle_name = fake.middle_name().lower() # if fake.random_int(0, 1) else ""  # Có thể có hoặc không có tên giữa
    last_name = fake.last_name().lower()

    # Xóa dấu và trả về tên
    first_name = remove_accents(first_name).replace(" ", "")
    middle_name = remove_accents(middle_name).replace(" ", "")
    last_name = remove_accents(last_name).replace(" ", "")

    # Ngẫu nhiên tạo ngày, tháng, và năm sinh trong khoảng 2002-2005
    day = f"{random.randint(1, 28):02}"  # Ngày từ 01 đến 28
    month = f"{random.randint(1, 12):02}"  # Tháng từ 01 đến 12
    year = random.randint(2002, 2006)  # Năm sinh từ 2002 đến 2005
    year = str(year)

    email_formats = [
        f"{first_name}{last_name}_{day}",
        f"{first_name}{last_name}{day}",
        f"{first_name[0]}{last_name[0]}{day}",
        f"{first_name[0]}{last_name[0]}{day}{year[-2:]}",
        f"{first_name}.{last_name}{year[-2:]}",
        f"{first_name}{random.randint(1, 999)}",
        f"{last_name}{first_name}{day}{month}{year}",
        f"{last_name}{middle_name}{first_name}{day}{year[-2:]}",
        f"{first_name}_{last_name}{day}{month}",
        f"{first_name}{middle_name}{last_name}{random.randint(1, 999)}",
        f"{first_name}{last_name}{middle_name}{day}{month}{year[-2:]}",
    ]

    email = random.choice(email_formats) + random.choice(domains)
    return email

new_emails = []
new_genders = []
existing_emails = df['Địa chỉ email'].values.tolist()

# Tạo Gmail và dự đoán giới tính dựa trên tên
N = 150

new_data['Địa chỉ email'] = new_emails
# 3 : CREATE N RECORD of rest columns with normalize
df_temp = df.drop(columns=['Địa chỉ email'])
for column_name, column_data in df_temp.items():
    # Lấy tỷ lệ xuất hiện của từng giá trị unique trong cột
    value_proportion = column_data.value_counts(normalize=True)
    # Tạo 300 giá trị mới dựa trên tỷ lệ của dữ liệu cũ
    new_data[column_name] = random.choices(value_proportion.index, weights=value_proportion.values, k=N)

# Tạo ra gmail
for gender in new_data['1. Giới tính của bạn:']:
    # tao gmail
    gender = 'male' if gender == 'Nam' else 'Nữ'
    new_email = generate_realistic_email(gender)
    # tao ra gmail den khi nao khong trung voi email cu thi thoi : RAT LAU :V
    while new_email in existing_emails:
        new_email = generate_realistic_email(gender)


    new_emails.append(new_email)
    existing_emails.append(new_email)


new_data['Địa chỉ email'] = new_emails

# Thay đổi cột 'Bạn nhận phiếu khảo sát này từ ai?' có toàn giá trị là Minh Trang
new_data['Bạn nhận phiếu khảo sát này từ ai?'] = ['Minh Trang'] * len(new_data['Bạn nhận phiếu khảo sát này từ ai?'])
print('====================== COMPARE DATA ==================')
for (colum_name), (new_data_key, _) in zip(df.columns, new_data.items()):
    print(f'{column_name.strip() == new_data_key.strip()} == {colum_name} -- {new_data_key}')
    # print(type(column_name), type(new_data_key))
    print(len(column_name), len(new_data_key))

# print(new_data['Bạn nhận phiếu khảo sát này từ ai?'], len(new_data['Bạn nhận phiếu khảo sát này từ ai?']))
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
