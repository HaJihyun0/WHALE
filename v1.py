# epidemic_simulation_app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# -----------------------
# Sidebar Settings
# -----------------------
st.sidebar.title("🦠 감염병 시뮬레이션 설정")
initial_infected = st.sidebar.number_input("초기 감염자 수", min_value=1, value=10)
infection_rate = st.sidebar.slider("감염 속도 (0~1)", 0.0, 1.0, 0.3)
lethality_rate = st.sidebar.slider("치명률 (0~1)", 0.0, 1.0, 0.05)
simulation_days = st.sidebar.slider("시뮬레이션 기간 (일)", 1, 60, 30)
population_size = st.sidebar.number_input("총 인구 수", min_value=1000, value=10000)

# -----------------------
# Initialize Population
# -----------------------
def initialize_population(size, initial_infected):
    df = pd.DataFrame({
        'lat': np.random.uniform(-60, 80, size),
        'lon': np.random.uniform(-180, 180, size),
        'status': 'healthy',
        'day_infected': -1
    })
    infected_idx = np.random.choice(df.index, initial_infected, replace=False)
    df.loc[infected_idx, 'status'] = 'infected'
    df.loc[infected_idx, 'day_infected'] = 0
    return df

# -----------------------
# Simulation Logic
# -----------------------
def simulate_spread(df, days, infection_rate, lethality_rate):
    daily_snapshots = []
    for day in range(1, days + 1):
        new_df = df.copy()
        infected = new_df[new_df['status'] == 'infected']

        for idx, row in infected.iterrows():
            close_people = new_df[(new_df['status'] == 'healthy') &
                                  (np.abs(new_df['lat'] - row['lat']) < 5) &
                                  (np.abs(new_df['lon'] - row['lon']) < 5)]
            to_infect = close_people.sample(frac=infection_rate)
            new_df.loc[to_infect.index, 'status'] = 'infected'
            new_df.loc[to_infect.index, 'day_infected'] = day

        infected_duration = day - new_df['day_infected']
        will_die = (new_df['status'] == 'infected') & (infected_duration > 5)
        death_mask = will_die & (np.random.rand(len(new_df)) < lethality_rate)
        new_df.loc[death_mask, 'status'] = 'dead'

        new_df = new_df.copy()
        daily_snapshots.append(new_df)
        df = new_df
    return daily_snapshots

# -----------------------
# Run Simulation
# -----------------------
st.title("🧬 감염병 확산 시뮬레이션")
population = initialize_population(population_size, initial_infected)
snapshots = simulate_spread(population, simulation_days, infection_rate, lethality_rate)

# -----------------------
# Visualization
# -----------------------
day = st.slider("📅 일 선택", 0, simulation_days, 0)
current = snapshots[day]
fig = px.scatter_geo(current, lat='lat', lon='lon', color='status',
                     color_discrete_map={
                         'healthy': 'green',
                         'infected': 'red',
                         'dead': 'black'
                     },
                     title=f"Day {day} 감염 현황", height=600)
st.plotly_chart(fig)

# -----------------------
# Summary
# -----------------------
final = snapshots[-1]
total_infected = (final['status'] == 'infected').sum() + (final['status'] == 'dead').sum()
total_dead = (final['status'] == 'dead').sum()
total_healthy = (final['status'] == 'healthy').sum()

st.subheader("📊 최종 요약")
st.write(f"- 감염자 수: {total_infected}")
st.write(f"- 사망자 수: {total_dead}")
st.write(f"- 생존자 수: {total_healthy}")
