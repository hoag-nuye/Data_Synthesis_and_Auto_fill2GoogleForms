from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


# ================= PART 1 : GET DATA OF EXCEL ===================
csv_path = "data/new_data_of_khaosat_hieubietkinhte_ydinhkhoinghiep.csv"
df = pd.read_csv(csv_path)
csv_data = df.to_dict(orient='records')
print(csv_data[0].keys())
print(len(csv_data[0].keys()))

# ================= PART 2 : FILL DATA TO GOOGLE FORM ===================
# Khởi tạo trình duyệt
chromedriver_path = 'F:/Application_Installed/CODE/Python/chromedriver-win64/chromedriver-win64/chromedriver.exe'
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service)
url = "https://docs.google.com/forms/d/e/1FAIpQLSdlKpCMMLRj0tA7D45bN8bvTRYYbQzPgsmNNqA0o7AHPd0Aqw/viewform?usp=sf_link"
driver.get(url)
# --------------- CLICK SUBMIT and NEXT BUTTON and submit other response -----------------


def click_next_button(classNameButton):
    buttons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, classNameButton)))
    try:
        for button in buttons:
            button_text = button.find_element(By.XPATH, './/span[1]').text
            if button_text in ['Next', 'Tiếp']:
                button.click()
                return
    except Exception as e:
        print(f"Error clicking button: {e}")

def click_submit_button(classNameButton):
    buttons = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, classNameButton)))
    for button in buttons:
        button_text = button.find_element(By.XPATH, './/span[1]').text

        if button_text.lower() in [item.lower() for item in ['Submit', 'Gửi']]:
            button.click()
            return


def click_submit_another_response_button(classNameButton):
    # Tìm tất cả các thẻ div với class 'c2gzEf'

    divs = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, classNameButton)))

    for div in divs:
        # Tìm thẻ a thứ hai trong thẻ div
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(div)
        )
        try:
            button_sub_again = div.find_element(By.XPATH, './/a[2]')

            button_sub_again.click()
            return    # Dừng lại sau khi nhấp vào thẻ <a> thứ hai đầu tiên
        except Exception as e:
            print(f"Lỗi khi nhấp vào thẻ <a> thứ hai: {e}")

# Đợi trang hoàn toàn tải xong
def wait_for_page_load(driver=driver, timeout=10):
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
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

import unicodedata
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
            question_text = unicodedata.normalize('NFC', question_text)
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
import difflib
import re
# Fill a record value from dataframe to a question of Radio in a section
def fill_to_radio_question(ansRadio, QuesRadio): #ansRadio : the answer of question in question ; valuesRadio : the choices of question
    for ques_key, ques_value in QuesRadio.items():
        # Tìm tên columns tương tự nhất trong ansRadio
        close_matches = difflib.get_close_matches(ques_key, ansRadio.keys(), n=1, cutoff=0.5) # giống 70%

        #ques_value là một danh sách các radio buttons, ta sẽ tìm button đúng
        if close_matches: # Nếu tìm thấy match tương tự
            # print(re.sub(r'\[.*?\]', '', ques_key), ':::::', ansRadio.keys())

            for radio_button in ques_value:
                # Nếu câu trả lời của ans_value khớp với lựa chọn của radio_button
                ans_value = ansRadio[close_matches[0]]
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable(radio_button)
                )
                if radio_button.get_attribute('data-value') == ans_value:
                    radio_button.click()  # Nhấn vào radio button đúng
                    # print(f"Đã chọn {ans_value}")
                    # print(f"Đã chọn {ans_value} cho câu hỏi {ques_key}")
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
            print(type(text_input))
            # Điền giá trị ans_value vào ô input
            # Đợi phần tử sẵn sàng trước khi clear
            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable(text_input)
            )
            text_input.clear()  # Xóa nội dung hiện tại nếu có
            text_input.send_keys(ans_value)  # Điền câu trả lời mới
            # print(f"Đã điền {ans_value}")
            # print(f"Đã điền {ans_value} cho câu hỏi {ques_key}")

# =============================== PART 3 : MAIN RUN ======================================
# ----------------- Find the questions in the google form ----------
# NOTE TỔNG 35 câu hỏi
# ISSUE : CHƯA TỰ ĐỘNG ĐẾM ĐƯỢC CÓ BAO NHIÊU CÂU HỎI TRONG 1 TRANG hoặc tụ động điền câu hỏi tương ứng mà vẫn cần đếm
# vì phải check bằng mắt, fit column dict của data với column dict của câu hỏi trong form khi tìm
# SETUP CLASS NAME
classNameButton_next = 'l4V7wb'
classNameButton_submit = 'l4V7wb'
classNameButton_subAgain = 'c2gzEf'

classNameQuest_radio = 'Qr7Oae'
classNameRow_radio = 'H2Gmcc'
classNameColumn_radio = 'Od2TWd'

classNameQuest_text = 'o3Dpx'
classNameAnswer_text = 'whsOnd'

form_data_text_page_1 = None
form_data_radio_page_2 = None
form_data_radio_page_3 = None
form_data_radio_page_4 = None

for csv_data_record in csv_data:
    # SETUP CLASS NAME
    # *********************** PAGE 1 of 4 ****************************
    # 1. GET TAGS OF WEB (không có radio)
    # click_next_button(classNameButton=classNameButton_next)
    # click_submit_button(classNameButton=classNameButton_submit)
    # click_submit_another_response_button(classNameButton=classNameButton_subAgain)
    wait_for_page_load()
    print('PAGE 1')

    form_data_text_page_1 = get_all_ques_of_text(classNameQuest=classNameQuest_text,
                                          classNameAnswer=classNameAnswer_text)
    # 2. FILL
    # Điền gmail (ô đầu tiên)
    ansText = dict([list(csv_data_record.items())[0]])  # Get data of email column
    QuesText = form_data_text_page_1
    print(QuesText.keys())
    fill_to_text_question(ansText, QuesText)
    # 3. Chuyển trang
    click_next_button(classNameButton=classNameButton_next)

    # *********************** PAGE 2 of 4 ****************************
    wait_for_page_load()
    print('PAGE 2')
    # 1. GET TAGS OF WEB (không có text)

    form_data_radio_page_2 = get_all_ques_of_radio(classNameQuest=classNameQuest_radio,
                                            classNameRow=classNameRow_radio,
                                            classNameColumn=classNameColumn_radio)

    # 2. FILL
    # Điền 6 ô tiếp theo (đều là radio)
    QuesRadio = form_data_radio_page_2
    # Bỏ nội dung trong [] vì không cần thiết
    # Tạo bản sao của từ điển để tránh thay đổi kích thước trong khi lặp
    new_QuesRadio = {}
    for key, value in QuesRadio.items():
        # Chuẩn hóa văn bản
        normalized_key = unicodedata.normalize('NFC', key)
        # Xóa nội dung trong dấu ngoặc vuông bao gồm cả ký tự xuống dòng
        cleaned_key = re.sub(r'\[.*?\]', '', key,  flags=re.DOTALL).strip()  # Thay đổi giá trị trong từ điển
        # Gán giá trị đã làm sạch vào từ điển mới với key chuẩn hóa
        new_QuesRadio[cleaned_key] = value
    # Gán lại từ điển mới vào QuesRadio
    QuesRadio = new_QuesRadio

    fill_to_radio_question(csv_data_record, QuesRadio)

    # 3. Chuyển trang
    click_next_button(classNameButton=classNameButton_next)
    # *********************** PAGE 3 of 4 ****************************
    wait_for_page_load()
    print('PAGE 3')
    # 1. GET TAGS OF WEB (không có text)

    form_data_radio_page_3 = get_all_ques_of_radio(classNameQuest=classNameQuest_radio,
                                            classNameRow=classNameRow_radio,
                                            classNameColumn=classNameColumn_radio)
    # 2. FILL
    # Điền 27 ô tiếp theo (đều là radio)
    QuesRadio = form_data_radio_page_3
    fill_to_radio_question(csv_data_record, QuesRadio)
    # 3. Chuyển trang
    click_next_button(classNameButton=classNameButton_next)
    # *********************** PAGE 4 of 4 ****************************
    wait_for_page_load()
    print('PAGE 4')
    # 1. GET TAGS OF WEB (không có text)
    
    form_data_radio_page_4 = get_all_ques_of_radio(classNameQuest=classNameQuest_radio,
                                            classNameRow=classNameRow_radio,
                                            classNameColumn=classNameColumn_radio)
    # 2. FILL
    # Điền 1 ô cuối cùng  (đều là radio) -> tổng 1 + 6 +27 +1 = 35 (OK)
    QuesRadio = form_data_radio_page_4
    fill_to_radio_question(csv_data_record, QuesRadio)
    # 3. Submit
    click_submit_button(classNameButton=classNameButton_submit)

    # *********************** PAGE 5 of 4 (PAGE  Submit other response) ****************************
    wait_for_page_load()
    # 4. Submit other response
    click_submit_another_response_button(classNameButton=classNameButton_subAgain)


# Đóng trình duyệt khi hoàn tất
driver.quit()