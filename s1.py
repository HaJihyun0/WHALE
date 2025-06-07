import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def growth_rate(temp, humidity, pH):
    temp_score = max(0, 1 - abs(temp - 25) / 15)
    humidity_score = max(0, 1 - abs(humidity - 80) / 40)
    pH_score = max(0, 1 - abs(pH - 5.5) / 3)
    return (temp_score + humidity_score + pH_score) / 3

st.title("푸른곰팡이 생장 조건 시뮬레이션")

# 입력값 받기
temp = st.slider("온도 (°C)", min_value=0, max_value=40, value=25)
humidity = st.slider("습도 (%)", min_value=0, max_value=100, value=80)
pH = st.slider("pH", min_value=0.0, max_value=14.0, value=5.5, step=0.1)

# 시간 설정
time_days = st.slider("관찰 기간 (일)", min_value=1, max_value=30, value=10)

# 성장률 계산
rate = growth_rate(temp, humidity, pH)

# 생장량 계산 (간단히 지수 성장 가정)
time = np.arange(0, time_days + 1)
growth = np.exp(rate * time / time_days)  # 상대적 성장량

# 그래프 그리기
fig, ax = plt.subplots()
ax.plot(time, growth, label="성장량")
ax.set_xlabel("시간 (일)")
ax.set_ylabel("상대적 성장량")
ax.set_title("푸른곰팡이 성장 시뮬레이션")
ax.legend()
st.pyplot(fig)

# 최적 성장률 정보
st.write(f"예상 성장률: {rate:.2f} (0~1 스케일)")
