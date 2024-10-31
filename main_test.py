from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


# ================= PART 1 : GET DATA OF EXCEL ===================
csv_path = "data/test_data2.csv"
df = pd.read_csv(csv_path)
df = df.drop(columns=['Timestamp'])
csv_data = df.to_dict(orient='records')

# ================= PART 2 : FILL DATA TO GOOGLE FORM ===================
# Khởi tạo trình duyệt
chromedriver_path = 'F:/Application_Installed/CODE/Python/chromedriver-win64/chromedriver-win64/chromedriver.exe'
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service)
url = "https://docs.google.com/forms/d/e/1FAIpQLSe4ja9qHPm0hLobDY1hXqEm05cK1cNkIqcbS8h5drt5ZD7T9g/viewform?usp=sf_link"
driver.get(url)
# --------------- CLICK SUBMIT and NEXT BUTTON and Submit another response -----------------
def click_next_button(classNameButton):
    buttons = driver.find_elements(By.CLASS_NAME, classNameButton)
    for button in buttons:
        button_text = button.find_element(By.XPATH, './/span[1]').text
        if button_text in ['Next', 'Tiếp']:
            button.click()
            # Thêm thời gian chờ cho đến khi một phần tử mới xuất hiện
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'l4V7wb')))
            break
def click_submit_button(classNameButton):
    buttons = driver.find_elements(By.CLASS_NAME, classNameButton)
    for button in buttons:
        button_text = button.find_element(By.XPATH, './/span[1]').text
        if button_text in ['submit', 'Gửi']:
            button.click()
            break
def click_submit_another_response_button(classNameButton):
    buttons = driver.find_elements(By.CLASS_NAME, classNameButton)
    button = buttons.find_element(By.XPATH, './/a[2]')
    button.click()
# --------------- GET DATA OF TEXT QUESTION IN FORM ----------------
def get_all_ques_of_text(classNameQuest, classNameAnswer):
    # Tạo một list để lưu trữ dữ liệu
    form_data = {}
    # Tìm tất cả các câu hỏi trong block này
    # questions = driver.find_elements(By.CLASS_NAME, classNameQuest)
    questions = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, classNameQuest)))

    # Lặp qua từng câu hỏi
    for question in questions:
        # Tìm các text điền câu hỏi
        text_value = question.find_elements(By.CLASS_NAME, classNameAnswer)
        if len(text_value) > 0:
            question_text = question.find_element(By.XPATH, './/span[1]').text
            form_data[question_text] = text_value
    return form_data
# --------------- GET DATA OF RADIO QUESTION INFORM ---------------
def get_all_ques_of_radio(classNameQuest, classNameRow, classNameColumn):
    # Tạo một list để lưu trữ dữ liệu
    form_data = {}
    # Tìm tất cả các câu hỏi trong block này
    # questions = driver.find_elements(By.CLASS_NAME, classNameQuest)
    questions = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, classNameQuest)))

    # Lặp qua từng câu hỏi
    for question in questions:
        try:
            # Lấy văn bản của câu hỏi là thẻ span đầu tiên
            question_text = question.find_element(By.XPATH, './/span[1]').text

            # Tìm các row của câu hỏi, mỗi row là một câu hỏi nhỏ khác
            rows_question = question.find_elements(By.CLASS_NAME, classNameRow)

            # Tìm các radio button chỉ liên quan đến câu hỏi này
            # Giả sử các radio button có thể là các sibling của câu hỏi(row của question) đó
            for row_question in rows_question:
                rows_question_text = row_question.find_element(By.XPATH, './/div[1]').text

                radio_values = row_question.find_elements(By.CLASS_NAME, classNameColumn)

                # # Lưu giá trị của các radio button (ở đây có thể là thuộc tính value hoặc text)
                # radio_values = tuple(rb.text for rb in radio_buttons)
                # Thêm câu hỏi và các radio button vào dictionary
                form_data[f"{question_text} [{rows_question_text}]"] = radio_values
        except Exception as e:
            print()
    return form_data


# --------------- FILL RADIO QUESTION ---------------
# Fill a record value from dataframe to a question of Radio in a section
def fill_to_radio_question(ansRadio, QuesRadio): #ansRadio : the answer of question in question ; valuesRadio : the choices of question
    for (ans_key, ans_value), (ques_key, ques_value) in zip(ansRadio.items(), QuesRadio.items()):

        #ques_value là một danh sách các radio buttons, ta sẽ tìm button đúng
        for radio_button in ques_value:
            # Nếu câu trả lời của ans_value khớp với lựa chọn của radio_button
            if radio_button.get_attribute('data-value') == ans_value:
                radio_button.click()  # Nhấn vào radio button đúng
                print(f"Đã chọn {ans_value} cho câu hỏi {ques_key}")
                break
            # else:
            #     print(f"Không tìm thấy câu trả lời phù hợp cho câu hỏi: {ques_key}: {radio_button.get_attribute('class')} : {ans_value}")
    return 0

# --------------- FILL TEXT QUESTION ---------------
def fill_to_text_question(ansText, QuesText):
    # Lặp qua cả hai dict cùng lúc bằng zip()
    for (ans_key, ans_value), (ques_key, ques_value) in zip(ansText.items(), QuesText.items()):

        # Giả sử ques_value là một list các ô input văn bản
        for text_input in ques_value:
            # Điền giá trị ans_value vào ô input
            text_input.clear()  # Xóa nội dung hiện tại nếu có
            text_input.send_keys(ans_value)  # Điền câu trả lời mới
            print(f"Đã điền {ans_value} cho câu hỏi {ques_key}")
# ================= PART 3 : MAIN RUN ===================
# ----------------- Find the questions in the google form -----------
click_next_button(classNameButton='l4V7wb')

form_data_radio = get_all_ques_of_radio(classNameQuest='Qr7Oae',
                                        classNameRow='H2Gmcc',
                                        classNameColumn='Od2TWd')

form_data_text = get_all_ques_of_text(classNameQuest='Qr7Oae',
                                      classNameAnswer='whsOnd')

# In kết quả để kiểm tra
# click_submit_button(classNameButton='l4V7wb')
print(csv_data[0].keys())
print(form_data_radio.keys())
print(form_data_text.keys())

# ----------------- Fill form -----------------------
# ----------------- Splitting the Data ---------------
# -----------------
ansRadio = dict(list(csv_data[0].items())[:-1])
QuesRadio = form_data_radio
#
fill_to_radio_question(ansRadio, QuesRadio)
ansText = dict([list(csv_data[0].items())[-1]])
QuesText = form_data_text
fill_to_text_question(ansText, QuesText)

# Đóng trình duyệt khi hoàn tất
driver.quit()