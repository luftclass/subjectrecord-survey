import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="학생 기초 조사", page_icon="📝")

# --- 구글 시트 연결 설정 ---
def get_google_sheet():
    # Streamlit 시크릿에서 인증 정보 가져오기
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_dict(st.secrets["gcp_service_account"], scope)
    client = gspread.authorize(creds)
    
    # ⚠️ 중요: 선생님이 만든 스프레드시트 제목을 정확히 적어야 합니다!
    sh = client.open("2025_학생기초조사") 
    return sh.sheet1

# --- 화면 구성 ---
st.title("📝 학생 기초 조사")
st.write("내용을 입력하고 제출 버튼을 눌러주세요.")

with st.form("survey_form", clear_on_submit=True):
    # 반, 번호, 이름 입력 받기
    student_class = st.selectbox("반", [f"{i}반" for i in range(1, 11)])
    student_number = st.number_input("번호", min_value=1, max_value=50, step=1)
    student_name = st.text_input("이름")
    
    submitted = st.form_submit_button("제출하기")

    if submitted:
        if not student_name:
            st.error("이름을 꼭 입력해주세요!")
        else:
            try:
                with st.spinner('제출 중...'):
                    sheet = get_google_sheet()
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    # 시트에 한 줄 추가
                    sheet.append_row([now, student_class, int(student_number), student_name])
                    
                st.success(f"✅ {student_name} 학생, 제출 완료!")
                st.balloons()
            except Exception as e:
                st.error(f"오류 발생: {e}")
