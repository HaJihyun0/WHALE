import streamlit as st

# 제목 및 설명
st.set_page_config(page_title="🐋 MBTI 진로 추천기", page_icon="🐋")
st.title("🐳 MBTI 진로 추천 웹앱")
st.write("당신의 **MBTI 유형**에 따라 어울리는 **직업**을 추천해줄게요!")
st.write("고래 친구들이 함께 도와줄 거예요 🐋💙")

# MBTI 선택
mbti_types = [
    "INTJ", "INTP", "ENTJ", "ENTP",
    "INFJ", "INFP", "ENFJ", "ENFP",
    "ISTJ", "ISFJ", "ESTJ", "ESFJ",
    "ISTP", "ISFP", "ESTP", "ESFP"
]

mbti = st.selectbox("당신의 MBTI 유형을 선택해주세요!", mbti_types)

# MBTI별 직업 추천 딕셔너리
career_recommendations = {
    "INTJ": ["전략 컨설턴트", "데이터 과학자", "정책 분석가"],
    "INFP": ["작가", "예술가", "심리상담사"],
    "ESFP": ["이벤트 기획자", "연예인", "여행 가이드"],
    "ENFP": ["광고 기획자", "창업가", "브랜드 디자이너"],
    "ENTJ": ["경영자", "프로젝트 매니저", "기업 전략가", "마케팅 디렉터"],
    # 나머지 MBTI도 추가 가능
}

# 추천 결과
if mbti in career_recommendations:
    st.subheader("🐋 어울리는 직업 추천!")
    for job in career_recommendations[mbti]:
        st.write(f"✅ {job}")
else:
    st.write("직업 추천 준비 중이에요. 곧 추가될 거예요! 🛠️")


# 푸터
st.markdown("---")
st.markdown("제작: 고래와 함께하는 진로 탐험팀 🐋")

