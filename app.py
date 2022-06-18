from collections import Counter
import time  # to simulate a real time data, time loop
import numpy as np  # np mean, np random
import pandas as pd  # read csv, df manipulation
import plotly.express as px  # interactive charts
import streamlit as st  # 🎈 data web app development

from plotly.graph_objs import *

first_time_load = 1

st.set_page_config(
    page_title="Fault Detection in Distribution Line Project Data Dashboard ⚡",
    page_icon="⚡",
    layout="wide",
)

# read csv from a Thinspeak.com channel
dataset_url = "https://thingspeak.com/channels/1770839/feed.csv"

# cutting off "UTC" part of date time object
def slicee(s):
    return s[:-3]

# @st.experimental_memo
def get_data() -> pd.DataFrame:
    df = pd.read_csv(dataset_url)
    df.columns = ["created_at", "entry_id", "Area_id",
                  "temperature", "humidity", "CO_gas_level", "Fault"]
    df.created_at = df.created_at.apply(slicee)
    df = df.drop('entry_id', axis=1)
    df.created_at = pd.to_datetime(
        df['created_at'], format='%Y-%m-%d %H:%M:%S')
    return df


df = get_data()

# dashboard title
st.title("Fault Detection in Distribution Line Project Data Dashboard ⚡")

click = st.button("Refresh")

fig_col1, fig_col2 = st.columns(2)

with fig_col1:
    st.markdown("### List of Monitoring Areas")
    st.markdown("->Area 1")
    st.markdown("->Area 2")

with fig_col2:
    st.markdown("### Most Fault Occured Area")
    most_fault_area = df[df['Fault'] == 1].groupby('Area_id').count()['Fault'].to_dict()
    hightest = [0, -999]
    for i, j in most_fault_area.items():
        if j > hightest[1]:
            hightest[1] = j
            hightest[0] = i

    st.metric(
        label="Area : ",
        value=hightest[0] #Hightest Fault Occured Area
        )

# creating a single-element container
placeholder = st.empty()



while True:
    if first_time_load:
        click=1
    if click:
        with placeholder.container():
            df = get_data()
 
            st.markdown("")
            st.markdown("## Temperture Level Charts")
            # create two columns for charts
            fig_col3, fig_col3_1 = st.columns(2)
            with fig_col3:
                st.markdown("##### Area 1")
                fig=px.line(
                    df[df['Area_id'] == 1], x="created_at", y="temperature"
                )
                fig = Figure(fig)
                st.write(fig)
            
            with fig_col3_1:
                st.markdown("##### Area 2")
                fig=px.line(
                    df[df['Area_id']==2], x="created_at", y="temperature"
                )
                st.write(fig)

            
            st.markdown("## Humidity Level Charts")
            fig_col4, fig_col4_1 = st.columns(2)
            with fig_col4:
                st.markdown("#####  Area 1")
                fig2 = px.line(
                    data_frame=df[df['Area_id'] == 1], x="created_at", y="humidity")
                st.write(fig2)
            with fig_col4_1:
                st.markdown("##### Area 2")
                fig2 = px.line(
                    data_frame=df[df['Area_id'] == 2], x="created_at", y="humidity")
                st.write(fig2)
                

            st.markdown("### CO Gas Level Charts")
            fig_col5, fig_col5_1 = st.columns(2)
            with fig_col5:
                st.markdown("##### Area 1")
                fig3 = px.line(
                    data_frame=df[df['Area_id'] == 1], x="created_at", y="CO_gas_level")
                st.write(fig3)
            with fig_col5_1:
                st.markdown("##### Area 2")
                fig3 = px.line(
                    data_frame=df[df['Area_id'] == 2], x="created_at", y="CO_gas_level")
                st.write(fig3)

            st.markdown("### Detailed Data View")
            st.write(df)

            
            time.sleep(1)