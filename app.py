import streamlit as st
import gspread
from datetime import datetime
import time # 시간을 세기 위한 도구 추가

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

# 성공 메시지와 지도가 나타날 자리를 미리 만들어둡니다.
success_message = st.empty()
map_area = st.empty()

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
                    
                # --- 성공 효과 (귀여운 지도 깜짝 등장!) ---
                # 1. 성공 메시지 표시
                success_message.success(f"✅ {student_name} 학생, 제출 완료!")
                
                # 2. 귀여운 세계지도 이미지 표시 (무료 일러스트 사용)
                map_area.image(
                    "https://cdn.pixabay.com/photo/2018/01/31/09/57/world-map-3120397_1280.png",
                    caption="넓은 세상으로! 🚀",
                    use_column_width=True
                )
                
                # 3. 3초 동안 보여주고 사라지기
                time.sleep(3) # 3초 기다림
                success_message.empty() # 메시지 지우기
                map_area.empty() # 지도 지우기
                
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
