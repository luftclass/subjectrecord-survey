import streamlit as st
import gspread
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="학생 기초 조사", page_icon="📝")

# --- 구글 시트 연결 설정 (최신 방식) ---
def get_google_sheet():
    # Streamlit 시크릿에 있는 정보를 바로 사용하여 연결
    # scopes 설정도 자동으로 처리됩니다.
    gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    
    # ⚠️ 선생님의 스프레드시트 제목을 여기에 정확히 적어주세요!
    sh = gc.open("2025_학생기초조사") 
    return sh.sheet1

# --- 화면 구성 ---
st.title("📝 학생 기초 조사")
st.write("반, 번호, 이름을 정확하게 입력하고 제출 버튼을 눌러주세요.")

with st.form("survey_form", clear_on_submit=True):
    student_class = st.selectbox("반을 선택하세요", [f"{i}반" for i in range(1, 11)])
    student_number = st.number_input("번호를 입력하세요", min_value=1, max_value=50, step=1)
    student_name = st.text_input("이름을 입력하세요")
    
    submitted = st.form_submit_button("제출하기")

    if submitted:
        if not student_name:
            st.error("이름을 입력해야 합니다!")
        else:
            try:
                with st.spinner('제출 중입니다...'):
                    sheet = get_google_sheet()
                    submit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    # 데이터 추가
                    sheet.append_row([submit_time, student_class, int(student_number), student_name])
                    
                st.success(f"✅ {student_name} 학생, 제출이 완료되었습니다!")
                st.balloons()
                
            except Exception as e:
                # 에러가 진짜 에러인지 확인
                st.error(f"오류가 발생했습니다: {e}")
