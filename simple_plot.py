from os import cpu_count
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from traitlets.traitlets import default

st.title("Data viewer")

upload_file = st.file_uploader("choose csv file")

if upload_file is not None:
    st.header("table head")
    df = pd.read_csv(upload_file, encoding="shift-jis")
else:
    st.header("use sample data")
    df = pd.read_csv("./data/hakusan1_new2.csv", encoding="shift-jis")
    st.header("plot")

col1, col2 = st.beta_columns(2)
x_column = col1.selectbox("select x data", df.columns)
y_columns = col2.multiselect("select y data", df.columns)

# secondary
num = [[False, "markers"] for _ in range(len(y_columns))]

cols = st.beta_columns(len(y_columns))
for i, name in enumerate(y_columns):
    num[i][0] = cols[i].radio(f"{name} secondary", [True, False])
    num[i][1] = cols[i].radio(f"{name} mode", ["markers", "lines", "lines+markers"])

fig = make_subplots(specs=[[{"secondary_y": True}]])
for index, y in enumerate(y_columns):
    fig.add_trace(go.Scatter(x=df[x_column], y=df[y], name=y, mode=num[index][1]),
        secondary_y=num[index][0])
fig.update_xaxes(showgrid=False)
fig.update_yaxes(showgrid=False)
st.plotly_chart(fig, use_container_width=True)