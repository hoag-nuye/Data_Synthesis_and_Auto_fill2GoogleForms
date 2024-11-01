from faker import Faker
fake = Faker('vi_VN')
unwanted_names = {"jane", "john"}
while True:
    first_name = fake.first_name_male().lower()
    middle_name = fake.middle_name().lower()  # if fake.random_int(0, 1) else ""  # Có thể có hoặc không có tên giữa
    last_name = fake.last_name().lower()

    print("gagaga: ",first_name, fake.locales)
    # Kiểm tra xem tên có nằm trong danh sách không mong muốn không
    if first_name not in unwanted_names:
        break