import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

df = pd.read_csv("final.csv")

def main_graph(top):
    fig = px.bar(top, x="Country/Economy", y=["GDP (millions of $)", "Agriculture GDP", "Industry", "Services"],
                 title="Top 10 Countries with highest GDP")
    return fig

def pie_chart(df):
    melted_df = pd.melt(df.head(1), id_vars=['Country/Economy'], var_name='Type', value_name='GDP')
    fig = px.pie(melted_df, values='GDP', names='Type',color_discrete_sequence=px.colors.qualitative.Dark24)
    fig.update_layout(width=600, height=400)
    return fig

def choropleth(type):
    df["log"] = np.log(df[type])
    fig = px.choropleth(df, locations='Country/Economy', locationmode='country names',
                        color=df["log"],
                        color_continuous_scale='Blues', range_color=[df["log"].min(), df["log"].max()])
    fig.update_layout(title=type)
    fig.update_layout(width = 1400,height = 600)
    return fig


top = df.sort_values(by = "GDP (millions of $)",ascending=False).head(10)
gdp = ["Country/Economy","GDP (millions of $)","Agriculture GDP","Industry","Services"]


fig = main_graph(top)

st.set_page_config(page_title="GDP Alok Chaudhary",layout="wide")


hide_img_fs = '''
<style>
button[title="View fullscreen"]{
    visibility: hidden;}
</style>
'''


col1,col2,col3 = st.columns([3,1,3])

with col1:
    st.plotly_chart(fig, use_container_width=False,config={"displayModeBar":False})
    option = st.selectbox(
        'Select Type of GDP',
        gdp[1:])
    map = choropleth(option)
    st.plotly_chart(map, use_container_width=False,config={"displayModeBar":False})

with col3:
    text = st.text_input(label="Search Country", value="japan")
    val = df[df["Country/Economy"].str.contains(text)][gdp]
    country = val.values[0][0]
    pie = pie_chart(val)
    st.metric(label="Country",value=country)
    st.text("   ")
    st.plotly_chart(pie, use_container_width=False, config={"displayModeBar": False})
