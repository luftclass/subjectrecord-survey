import streamlit as st
import gspread
from datetime import datetime

# 페이지 설정 (아이콘도 지구본으로 변경)
st.set_page_config(page_title="세계지리 세특 조사", page_icon="🌏")

# --- 구글 시트 연결 설정 (최신 방식) ---
def get_google_sheet():
    # Streamlit 시크릿에 있는 키 정보를 바로 사용
    gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    
    # 선생님의 스프레드시트 제목
    sh = gc.open("2025 2학기 세계지리 교과세특 응답 수집") 
    return sh.sheet1

# --- 화면 구성 ---
st.title("🌏 2025 2학기 세계지리")
st.subheader("교과세특 기초자료 수집")
st.write("반, 번호, 이름을 정확하게 입력하고 제출 버튼을 눌러주세요.")

with st.form("survey_form", clear_on_submit=True):
    # 1. 반 선택
    student_class = st.selectbox("반을 선택하세요", [f"{i}반" for i in range(1, 11)])
    
    # 2. 번호 입력
    student_number = st.number_input("번호를 입력하세요", min_value=1, max_value=50, step=1)
    
    # 3. 이름 입력
    student_name = st.text_input("이름을 입력하세요")

    # 제출 버튼
    submitted = st.form_submit_button("제출하기")

    if submitted:
        if not student_name:
            st.warning("이름을 입력해야 합니다!")
        else:
            try:
                with st.spinner('제출 중입니다...'):
                    sheet = get_google_sheet()
                    submit_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    
                    # 엑셀에 데이터 한 줄 추가
                    sheet.append_row([submit_time, student_class, int(student_number), student_name])
                    
                # --- 성공 메시지 및 세계지도 표시 ---
                st.success(f"✅ {student_name} 학생, 제출 완료!")
                
                # 풍선(st.balloons) 대신 세계지도 이미지 표시!
                # (무료 공개 이미지 URL을 사용했습니다)
                st.image(
                    "https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/World_map_-_low_resolution.svg/1200px-World_map_-_low_resolution.svg.png",
                    caption="제출 성공! 세계로 뻗어나가세요! 🌏",
                    use_column_width=True
                )
                
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
