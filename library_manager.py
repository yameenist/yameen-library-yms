import streamlit as st
import pandas as pd
import json
from datetime import datetime
import plotly.express as px # type: ignore
from streamlit_lottie import st_lottie # type: ignore
import requests

# ---------------------- Utility Functions ----------------------

def load_data():
    try:
        with open("library.json", "r") as file:
            return pd.read_json(file)
    except FileNotFoundError:
        return pd.DataFrame(columns=["Title", "Author", "Genre", "Publication year", "Read status", "Added date"])

def save_data(df):
    df.to_json("library.json", orient="records", indent=2)

def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# ---------------------- Page Config ----------------------

st.set_page_config(page_title="📚 Personal Library", page_icon="📘", layout="wide")
st.title("📚 Personal Library Manager")
st.markdown("Track your favorite books and visualize your reading journey!")

# ---------------------- Load Animation ----------------------

lottie = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_touohxv0.json")

# ---------------------- Sidebar Form ----------------------

st.sidebar.header("📖 Add a New Book")

with st.sidebar.form("add_book"):
    title = st.text_input("Book Title")
    author = st.text_input("Author")
    genre = st.text_input("Genre")
    year = st.number_input("Publication Year", min_value=1800, max_value=datetime.now().year, step=1)
    read = st.checkbox("Read?", value=False)
    submitted = st.form_submit_button("➕ Add Book")

# ---------------------- Load/Update Data ----------------------

df = load_data()

if submitted and title and author and genre:
    new_book = {
        "Title": title,
        "Author": author,
        "Genre": genre,
        "Publication year": year,
        "Read status": read,
        "Added date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    df = pd.concat([df, pd.DataFrame([new_book])], ignore_index=True)
    save_data(df)
    st.success(f"✅ '{title}' by {author} added!")

# ---------------------- Filter + Display ----------------------

st.subheader("📚 Library Overview")

filter_genre = st.multiselect("Filter by Genre", df["Genre"].unique())
filter_read = st.radio("Filter by Read Status", ["All", "Read", "Unread"])

filtered_df = df.copy()
if filter_genre:
    filtered_df = filtered_df[filtered_df["Genre"].isin(filter_genre)]
if filter_read == "Read":
    filtered_df = filtered_df[filtered_df["Read status"] == True]
elif filter_read == "Unread":
    filtered_df = filtered_df[filtered_df["Read status"] == False]

st.dataframe(filtered_df, use_container_width=True)

# ---------------------- Visualizations ----------------------

st.subheader("📊 Library Statistics")

col1, col2 = st.columns(2)

with col1:
    genre_chart = df["Genre"].value_counts().reset_index()
    genre_chart.columns = ["Genre", "Count"]
    fig1 = px.pie(genre_chart, names="Genre", values="Count", title="Books by Genre")
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    read_chart = df["Read status"].value_counts().reset_index()
    read_chart.columns = ["Read Status", "Count"]
    read_chart["Read Status"] = read_chart["Read Status"].map({True: "Read", False: "Unread"})
    fig2 = px.bar(read_chart, x="Read Status", y="Count", title="Read vs Unread")
    st.plotly_chart(fig2, use_container_width=True)

# ---------------------- Animation ----------------------

st.markdown("### 📘 Keep Reading and Growing!")
if lottie:
    st_lottie(lottie, height=200, key="reader")
else:
    st.info("⚠️ Animation failed to load.")

# ---------------------- Footer ----------------------

st.markdown("---")
st.caption("📘 Created by [Muhammad Yameen](https://github.com/yameenist)")

