import streamlit as st
import pandas as pd
import pandas.io.sql as sqlio
import altair as alt
import folium
from streamlit_folium import st_folium

from db import conn_str

st.title("Seattle Events")

# 从数据库读取数据
df = sqlio.read_sql_query("SELECT * FROM events", conn_str)

# 提取月份和星期
df['event_date'] = pd.to_datetime(df['event_date'])  # 确保event_date是日期格式
df['month'] = df['event_date'].dt.month
df['weekday'] = df['event_date'].dt.day_name()

# 类别筛选
category = st.selectbox("Select a category", df['category'].unique())

# 地点筛选（假设你的数据表中有location列）
location = st.selectbox("Select a location", df['location'].unique())

# 根据类别和地点过滤数据
df_filtered = df[(df['category'] == category) & (df['location'] == location)]

# 绘制类别统计图
st.altair_chart(
    alt.Chart(df).mark_bar().encode(
        x="count():Q",
        y=alt.Y("category:N", sort='-x'),
        tooltip=['category', 'count()']
    ).properties(title="Events by Category").interactive(),
    use_container_width=True,
)

# 绘制月份统计图
st.altair_chart(
    alt.Chart(df).mark_bar().encode(
        x=alt.X('month:O', title='Month'),
        y=alt.Y('count():Q', title='Number of Events'),
        tooltip=['month', 'count()']
    ).properties(title="Number of Events per Month").interactive(),
    use_container_width=True,
)

# 绘制星期统计图
st.altair_chart(
    alt.Chart(df).mark_bar().encode(
        x='weekday:O',
        y='count():Q',
        tooltip=['weekday', 'count()']
    ).properties(title="Number of Events by Day of the Week").interactive(),
    use_container_width=True,
)

# 显示筛选后的活动列表
st.write(df_filtered)

# 地图展示（假设你的数据表中有latitude和longitude列）
m = folium.Map(location=[47.6062, -122.3321], zoom_start=12)
for index, row in df_filtered.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=row['name']).add_to(m)  # 假设有name列作为活动名称

st_folium(m, width=1200, height=600)
