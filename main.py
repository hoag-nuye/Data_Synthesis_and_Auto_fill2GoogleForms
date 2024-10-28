from selenium import webdriver
from selenium.webdriver.common.by import By

# Khởi tạo trình duyệt
driver = webdriver.Chrome("F:/Application_Installed/CODE/Python/chromedriver-win64")
url = "https://docs.google.com/forms/d/1fGeRJ59x5r8lsbyBe-hR7A75yU288yxKtS7JmsGdkBM/edit"
driver.get(url)

# Tạo một dictionary để lưu trữ dữ liệu
form_data = {}

# =============== Question of Multiple Choice Gird ===========#
classNameQuestionRadio_MTC = "Mf1JDc.PuUvkc.OIC90c" 
classNameQuestionTxt_MTC = "adad"
classNameAnswerRadio_MTC = 'RDPZE'


# Tìm tất cả các câu hỏi trong block này
questions = driver.find_elements(By.CLASS_NAME, classNameQuestionRadio_MTC)

# Lặp qua từng câu hỏi
for question in questions:
    # Lấy văn bản của câu hỏi
    question_text = question.text

    # Tìm các radio button chỉ liên quan đến câu hỏi này
    # Giả sử các radio button có thể là các sibling của câu hỏi đó
    radio_buttons_container = question.find_element(By.XPATH,
                                                    './following-sibling::div[contains(@class, "{}")]'.format(classNameQuestionRadio_MTC))
    radio_buttons = radio_buttons_container.find_elements(By.CLASS_NAME, classNameAnswerRadio_MTC)

    # # Lưu giá trị của các radio button (ở đây có thể là thuộc tính value hoặc text)
    # radio_values = tuple(rb.text for rb in radio_buttons)
    # Lưu giá trị của radio_buttons - là tập câu trả lời
    radio_values = radio_buttons

    # Thêm câu hỏi và các radio button vào dictionary
    form_data[question_text] = radio_values

# In kết quả để kiểm tra
print(form_data)
print(type(questions))
# Đóng trình duyệt khi hoàn tất
driver.quit()