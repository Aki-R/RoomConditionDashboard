import streamlit as st
import pandas as pd
import pandas.tseries.offsets as offsets
import numpy as np
import plotly.express as px

# initialize
if "timescale" not in st.session_state:
    st.session_state.timescale = "1day"

st.session_state.timescale=st.selectbox("Time Scale", ("1day", "1week"))

dataframe = pd.read_json("./wfirex_sensor.json")

temperature_latest = dataframe.tail(1)["Temperature"].values[0]
humidity_latest = dataframe.tail(1)["Humidity"].values[0]
datetime_latest = dataframe.tail(1)["DateTime"].values[0]
datetime_before = datetime_latest - offsets.Hour(1)
datetime_before_day = datetime_latest - offsets.Day(1)
datetime_before_week = datetime_latest - offsets.Day(7)
temperature_before = dataframe.loc[dataframe["DateTime"]>datetime_before].head(1)["Temperature"].values[0]
humidity_before = dataframe.loc[dataframe["DateTime"]>datetime_before].head(1)["Humidity"].values[0]

col1, col2 = st.columns(2)

with col1:
    st.metric(label="Temperature", value=f"{temperature_latest} °C", delta=f"{(temperature_latest - temperature_before):.1f} °C")

with col2:
    st.metric(label="Humidity", value=f"{humidity_latest} %", delta=f"{(humidity_latest - humidity_before):.1f} %")

# Temperaturue Figure
config = {'scrollZoom': True}
fig_temp = px.line(
    dataframe,
    x="DateTime",
    y=['Temperature', 'Temperature2'],
    title='Temperature'
)
fig_temp.update_layout(dragmode='pan',
                       legend=dict(
                                yanchor="bottom",
                                y=0.01,
                                xanchor="left",
                                x=0.01
                                )
                       )
fig_temp.update_yaxes(title="°C")
fig_temp.update_xaxes(title=None)
if st.session_state.timescale == "1week":
    fig_temp.update_xaxes(range=[pd.Timestamp(datetime_before_week).to_pydatetime(), pd.Timestamp(datetime_latest).to_pydatetime()])
elif st.session_state.timescale == "1day":
    fig_temp.update_xaxes(range=[pd.Timestamp(datetime_before_day).to_pydatetime(), pd.Timestamp(datetime_latest).to_pydatetime()])

st.plotly_chart(fig_temp, theme="streamlit", use_container_width=False, config=config)

# Humidity Figure
fig_humd = px.line(
    dataframe,
    x="DateTime",
    y='Humidity',
    title='Humidity'
)
fig_humd.update_layout(dragmode='pan')
fig_humd.update_yaxes(title='%')
fig_humd.update_xaxes(title=None)
if st.session_state.timescale == "1week":
    fig_humd.update_xaxes(range=[pd.Timestamp(datetime_before_week).to_pydatetime(), pd.Timestamp(datetime_latest).to_pydatetime()])
elif st.session_state.timescale == "1day":
    fig_humd.update_xaxes(range=[pd.Timestamp(datetime_before_day).to_pydatetime(), pd.Timestamp(datetime_latest).to_pydatetime()])
st.plotly_chart(fig_humd, theme="streamlit", use_container_width=False, config=config)

# Illuminace
fig_ilm= px.line(
    dataframe,
    x="DateTime",
    y='Iluminance',
    title='Iluminace'
)
fig_ilm.update_layout(dragmode='pan')
fig_ilm.update_yaxes(title='lx')
fig_ilm.update_xaxes(title=None)
if st.session_state.timescale == "1week":
    fig_ilm.update_xaxes(range=[pd.Timestamp(datetime_before_week).to_pydatetime(), pd.Timestamp(datetime_latest).to_pydatetime()])
elif st.session_state.timescale == "1day":
    fig_ilm.update_xaxes(range=[pd.Timestamp(datetime_before_day).to_pydatetime(), pd.Timestamp(datetime_latest).to_pydatetime()])
st.plotly_chart(fig_ilm, theme="streamlit", use_container_width=False, config=config)

# pandas dataframe view
st.dataframe(dataframe)