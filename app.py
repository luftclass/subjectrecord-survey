import streamlit as st
import gspread
from datetime import datetime
import time 

# 페이지 설정
st.set_page_config(page_title="세계지리 세특 조사", page_icon="🌏")

# --- 구글 시트 연결 설정 ---
def get_google_sheet():
    gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    sh = gc.open("2025 2학기 세계지리 교과세특 응답 수집") 
    return sh.sheet1

# --- 화면 구성 ---
st.title("🌏 2025 2학기 세계지리")
st.subheader("교과세특 기초자료 수집")

# 성공 메시지가 뜰 공간 확보
result_area = st.empty()

st.write("반, 번호, 이름을 정확하게 입력하고 제출 버튼을 눌러주세요.")

with st.form("survey_form", clear_on_submit=True):
    student_class = st.selectbox("반을 선택하세요", [f"{i}반" for i in range(1, 11)])
    student_number = st.number_input("번호를 입력하세요", min_value=1, max_value=50, step=1)
    student_name = st.text_input("이름을 입력하세요")
    
    submitted = st.form_submit_button("제출하기")

    if submitted:
        if not student_name:
            st.warning("이름을 입력해야 합니다!")
        else:
            try:
                with st.spinner('제출 중입니다...'):
                    sheet = get_google_sheet()
                    submit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    sheet.append_row([submit_time, student_class, int(student_number), student_name])
                
                # --- 성공 효과 ---
                # 1. 화면 전체에 풍선 날리기 (가장 확실한 축하!)
                st.balloons()
                
                # 2. 성공 메시지 표시
                result_area.success(f"✅ {student_name} 학생, 제출 완료!")
                
                # 3. 3초 뒤 메시지 지우기 (다음 학생을 위해 깔끔하게)
                time.sleep(3)
                result_area.empty()
                
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
