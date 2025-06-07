import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.title("🦠 바이러스 확산 시뮬레이션")

# 사이드바 설정
st.sidebar.header("시뮬레이션 설정")
population = st.sidebar.number_input("총 인구 수", min_value=100, value=1000)
initial_infected = st.sidebar.number_input("초기 감염자 수", min_value=1, max_value=population, value=10)
infection_rate = st.sidebar.slider("감염 속도 (확률)", 0.0, 1.0, 0.2, 0.01)
mortality_rate = st.sidebar.slider("사망률 (확률)", 0.0, 1.0, 0.05, 0.01)
days = st.sidebar.slider("시뮬레이션 기간 (일)", 1, 100, 30)

if st.button("📊 시뮬레이션 실행"):

    # 상태 초기화
    healthy = population - initial_infected
    infected = initial_infected
    dead = 0

    history = {
        "Day": [],
        "Healthy": [],
        "Infected": [],
        "Dead": []
    }

    for day in range(days + 1):
        history["Day"].append(day)
        history["Healthy"].append(healthy)
        history["Infected"].append(infected)
        history["Dead"].append(dead)

        # 감염 확산
        new_infections = min(np.random.binomial(healthy, infection_rate * infected / population), healthy)
        new_deaths = np.random.binomial(infected, mortality_rate)

        healthy -= new_infections
        infected = infected + new_infections - new_deaths
        dead += new_deaths

        if infected <= 0:
            infected = 0
            break

    # 데이터프레임으로 정리
    df = pd.DataFrame(history)

    # 그래프 출력
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Day"], y=df["Healthy"], name="Healthy", line=dict(color="green")))
    fig.add_trace(go.Scatter(x=df["Day"], y=df["Infected"], name="Infected", line=dict(color="red")))
    fig.add_trace(go.Scatter(x=df["Day"], y=df["Dead"], name="Dead", line=dict(color="gray")))
    fig.update_layout(title="📈 감염병 확산 추이", xaxis_title="일", yaxis_title="사람 수")

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("📋 최종 결과 요약")
    st.markdown(f"- 생존자 (Healthy): `{healthy}`명")
    st.markdown(f"- 감염자 (Infected): `{infected}`명")
    st.markdown(f"- 사망자 (Dead): `{dead}`명")
