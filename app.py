import streamlit as st
import pandas as pd
import pandas.io.sql as sqlio
import altair as alt
import folium
from streamlit_folium import st_folium
from db import conn_str
from dotenv import load_dotenv

load_dotenv() 
st.write(conn_str)


df = sqlio.read_sql_query("SELECT * FROM events", conn_str)
st.write(df)

st.title("Seattle Events")

# Chart 1: Most common event categories
st.header("Most Common Event Categories")
category_counts = df['category'].value_counts()
st.bar_chart(category_counts)

# Chart 2: Events count by month
st.header("Events Count by Month")
df['date'] = pd.to_datetime(df['date'])
df['month'] = df['date'].dt.month
month_counts = df['month'].value_counts().sort_index()
st.line_chart(month_counts)

# Chart 3: Events count by day of the week
st.header("Events Count by Day of the Week")
df['weekday'] = df['date'].dt.day_name()
weekday_counts = df['weekday'].value_counts()
st.bar_chart(weekday_counts)

# Map: Events locations
st.header("Events Locations on Map")

# Filter out rows with missing latitude or longitude values
df = df.dropna(subset=['latitude', 'longitude'])

m = folium.Map(location=[47.6062, -122.3321], zoom_start=12)
for index, event in df.iterrows():
    folium.Marker([event['latitude'], event['longitude']], popup=event['venue']).add_to(m)
st_folium(m, width=1200, height=600)

st.sidebar.header("Data Filters")

# Dropdown to filter category
selected_category = st.sidebar.selectbox("Select Event Category", df['category'].unique())
filtered_df = df[df['category'] == selected_category]

# Date range selector for event date
date_range = st.sidebar.date_input("Select Date Range", [df['date'].min(), df['date'].max()])
date_range = [pd.to_datetime(date, utc=True) for date in date_range]  # Convert to UTC Timestamp objects
filtered_df = filtered_df[(filtered_df['date'] >= date_range[0]) & (filtered_df['date'] <= date_range[1])]

# Filter location
selected_location = st.sidebar.selectbox("Select Event Location", df['location'].unique())
filtered_df = filtered_df[filtered_df['location'] == selected_location]

# Filter weather
selected_weather = st.sidebar.selectbox("Select Weather Condition", df['weather_condition'].unique())
filtered_df = filtered_df[filtered_df['weather_condition'] == selected_weather]

# Display filtered data
st.subheader("Filtered Events Data")
st.write(filtered_df)

# # 提取月份和星期
# df['event_date'] = pd.to_datetime(df['event_date'])  # 确保event_date是日期格式
# df['month'] = df['event_date'].dt.month
# df['weekday'] = df['event_date'].dt.day_name()

# # 类别筛选
# category = st.selectbox("Select a category", df['category'].unique())

# # 地点筛选（假设你的数据表中有location列）
# location = st.selectbox("Select a location", df['location'].unique())

# # 根据类别和地点过滤数据
# df_filtered = df[(df['category'] == category) & (df['location'] == location)]

# # 绘制类别统计图
# st.altair_chart(
#     alt.Chart(df).mark_bar().encode(
#         x="count():Q",
#         y=alt.Y("category:N", sort='-x'),
#         tooltip=['category', 'count()']
#     ).properties(title="Events by Category").interactive(),
#     use_container_width=True,
# )

# # 绘制月份统计图
# st.altair_chart(
#     alt.Chart(df).mark_bar().encode(
#         x=alt.X('month:O', title='Month'),
#         y=alt.Y('count():Q', title='Number of Events'),
#         tooltip=['month', 'count()']
#     ).properties(title="Number of Events per Month").interactive(),
#     use_container_width=True,
# )

# # 绘制星期统计图
# st.altair_chart(
#     alt.Chart(df).mark_bar().encode(
#         x='weekday:O',
#         y='count():Q',
#         tooltip=['weekday', 'count()']
#     ).properties(title="Number of Events by Day of the Week").interactive(),
#     use_container_width=True,
# )

# # 显示筛选后的活动列表
# st.write(df_filtered)

# # 地图展示（假设你的数据表中有latitude和longitude列）
# m = folium.Map(location=[47.6062, -122.3321], zoom_start=12)
# for index, row in df_filtered.iterrows():
#     folium.Marker([row['latitude'], row['longitude']], popup=row['name']).add_to(m)  # 假设有name列作为活动名称

# st_folium(m, width=1200, height=600)
