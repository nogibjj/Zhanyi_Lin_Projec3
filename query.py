import pandas as pd
import sqlite3
import loaddb
import streamlit as st

def query_from_sqlie(likes = 0, topic = "news_&_social_concern"):
    query = "SELECT * FROM Tweets WHERE Likes > {l} and Topic = '{t}';".format(l = likes, t = topic) 
    con = loaddb.create_connection(r"./db/database.db")
    cursor = con.cursor()
    df = pd.read_sql_query(query, con)
    print("Datafame established successfully")
    df_sub = df["Cleaned_Tweets"].copy()
    df_sub.rename({"Cleaned_Tweets": "Elon's Tweets about {a}".format(a = topic)})
    print("Making tha table")
    st.table(df_sub)
    return 1
if __name__ == "__main__":
    query_from_sqlie(0,"diaries_&_daily_life")
    