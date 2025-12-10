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

# --- 세션 상태 초기화 (페이지 이동 및 데이터 임시 저장을 위해 필요) ---
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'student_info' not in st.session_state:
    st.session_state.student_info = {}
if 'stage2_data' not in st.session_state:
    st.session_state.stage2_data = {}

# --- 화면 구성 ---
st.title("🌏 2025 2학기 세계지리")
st.subheader("교과세특 기초자료 수집")

# 성공 메시지 공간 확보
result_area = st.empty()

# ==========================================
# [1단계] 반, 번호, 이름 입력
# ==========================================
if st.session_state.step == 1:
    st.info("👋 [1/3단계] 본인의 정보를 정확히 입력하세요.")
    
    with st.form("step1_form"):
        student_class = st.selectbox("반을 선택하세요", [f"{i}반" for i in range(1, 11)])
        student_number = st.number_input("번호를 입력하세요", min_value=1, max_value=50, step=1)
        student_name = st.text_input("이름을 입력하세요")
        
        goto_step2 = st.form_submit_button("다음 단계로 (교과 학습) ➡️")
        
        if goto_step2:
            if not student_name:
                st.warning("이름을 입력해야 다음으로 넘어갈 수 있습니다!")
            else:
                st.session_state.student_info = {
                    "class": student_class,
                    "number": student_number,
                    "name": student_name
                }
                st.session_state.step = 2
                st.rerun()

# ==========================================
# [2단계] 교과 학습 태도 및 노력
# ==========================================
elif st.session_state.step == 2:
    info = st.session_state.student_info
    st.success(f"학번: {info['class']} {info['number']}번 {info['name']}")
    st.info("📝 [2/3단계] 평소 학습 태도에 대해 서술하세요.")
    
    with st.form("step2_form"):
        q1 = st.text_area(
            "1. 자신의 수업 태도 자세와 교과목 성적 향상을 위한 노력", 
            height=100,
            placeholder="수업 시간 집중 노력, 수행평가 준비 과정 등을 구체적으로 서술"
        )
        
        q2 = st.text_area(
            "2. 세계지리 교과의 성적 향상을 위해 자신만의 학습 방법과 과정에 대해 서술하시오.", 
            height=100,
            placeholder="나만의 암기법, 노트 필기 방식, 문제 풀이 전략 등"
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
             # 뒤로 가기 기능 (버튼은 폼 밖에 두는 게 안전하지만 여기서는 로직상 폼 제출로 처리)
            back_to_step1 = st.form_submit_button("⬅️ 정보 수정하기")
        with col2:
            goto_step3 = st.form_submit_button("다음 단계로 (실험 탐구) ➡️")
        
        if back_to_step1:
            st.session_state.step = 1
            st.rerun()
            
        if goto_step3:
            if not q1 or not q2:
                st.warning("내용을 모두 작성해주세요!")
            else:
                # 2단계 답변 임시 저장
                st.session_state.stage2_data = {"q1": q1, "q2": q2}
                st.session_state.step = 3
                st.rerun()

# ==========================================
# [3단계] 카르스트 지형 형성 실험
# ==========================================
elif st.session_state.step == 3:
    info = st.session_state.student_info
    st.success(f"작성자: {info['name']} 학생 (마지막 단계입니다! 힘내세요 💪)")
    st.info("⚗️ [3/3단계] 카르스트 지형 형성 실험 보고서")
    
    with st.form("step3_form"):
        # 질문들이 많으므로 구분을 위해 마크다운 사용
        st.markdown("##### 1. 실험 원리 및 토양 특성")
        k1 = st.text_area(
            "Q1. 이번 실험에서 모래 황토를 혼합물에 넣은 목적을 테라로사의 형성 원리와 연관 지어 설명하시오.",
            height=80
        )
        k2 = st.text_area(
            "Q2. 테라로사의 붉은색이 나타나는 주된 원인 물질은 무엇인지 설명하고, 이 토양이 농업에 유리한 이유를 두 가지 측면에서 서술하시오.",
            height=80
        )
        
        st.markdown("---")
        st.markdown("##### 2. 용식 반응과 실험 설계")
        k3 = st.text_area(
            "Q3. 용식 반응 속도에 영향을 미치는 자연적 요인 두 가지를 제시하고, 그 이유를 화학적/지리적 측면에서 간략히 설명하시오.",
            height=80
        )
        k4 = st.text_area(
            "Q4. 위에서 제시한 요인 중 한 가지를 이용하여, 학생 실험에서 용식 속도를 변화시키기 위한 구체적인 실험 설계 방안을 서술하시오.",
            height=80
        )
        
        st.markdown("---")
        st.markdown("##### 3. 심화 탐구 및 소감")
        k5 = st.text_area(
            "Q5. 실제 자연의 카르스트 지형 형성 과정을 더욱 정교하게 모방하도록 재구성한다면, 어떤 요소를 추가하거나 변경하고 싶은지 구체적인 이유와 함께 서술하시오.",
            height=80
        )
        k6 = st.text_area(
            "Q6. 활동 소감문",
            height=80,
            placeholder="실험을 통해 배운 점, 느낀 점, 아쉬운 점 등을 자유롭게 서술"
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            back_to_step2 = st.form_submit_button("⬅️ 이전 단계로")
        with col2:
            final_submit = st.form_submit_button("최종 제출하기 ✅")
            
        if back_to_step2:
            st.session_state.step = 2
            st.rerun()
            
        if final_submit:
            # 필수 답변 체크 (너무 빡빡하면 학생들 힘들 수 있으니 중요 질문만 체크하거나 뺄 수도 있음)
            if not k1 or not k2 or not k6: 
                st.warning("성실한 작성을 위해 빈칸을 채워주세요! (최소한 1,2번과 소감문은 필수입니다)")
            else:
                try:
                    with st.spinner('전체 데이터를 저장 중입니다...'):
                        sheet = get_google_sheet()
                        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        # 1단계, 2단계, 3단계 모든 데이터 합치기
                        row_data = [
                            now,
                            info['class'],
                            int(info['number']),
                            info['name'],
                            st.session_state.stage2_data['q1'], # 수업태도
                            st.session_state.stage2_data['q2'], # 학습방법
                            k1, # 카르스트 Q1
                            k2, # 카르스트 Q2
                            k3, # 카르스트 Q3
                            k4, # 카르스트 Q4
                            k5, # 카르스트 Q5
                            k6  # 소감문
                        ]
                        
                        sheet.append_row(row_data)
                    
                    # 성공 효과
                    st.balloons()
                    result_area.success(f"✅ {info['name']} 학생, 모든 과제 제출 완료! 수고 많았습니다.")
                    time.sleep(3)
                    
                    # 상태 초기화 (처음으로)
                    for key in ['step', 'student_info', 'stage2_data']:
                        del st.session_state[key]
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"저장 중 오류가 발생했습니다: {e}")
