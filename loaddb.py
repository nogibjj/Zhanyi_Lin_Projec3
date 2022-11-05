"""

Use sqlite3 to load data and cardiffnlp/tweet-topic-21-multi from hugging face to analyze the topic and store it as a new table

"""

import sqlite3
from sqlite3 import Error
import pandas as pd
import numpy as np
from transformers import AutoModelForSequenceClassification, TFAutoModelForSequenceClassification
from transformers import AutoTokenizer
from scipy.special import expit

MODEL = f"cardiffnlp/tweet-topic-21-multi"
tokenizer = AutoTokenizer.from_pretrained(MODEL)
    # PT
model = AutoModelForSequenceClassification.from_pretrained(MODEL)
class_mapping = model.config.id2label


def load_orginal_dataset(source = "cleandata.csv"): # default path is cleandata.csv which stores Elon's Tweets data. It can be changed to others
    df = pd.read_csv(source)
    # subset
    df = df[["Retweets", "Likes","Date","Cleaned_Tweets"]]
    return df

    
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("database successfully connected")
    except Error as e:
        print(e)
    return conn


def create_table(c, create_table_sql):
    try:
        c.execute(create_table_sql)
    except Error as e:
        print(e)

# use this method to add the topic for each tweet
def analyze_topic(text = "What a good word"):
    tokens = tokenizer(text, return_tensors='pt')
    output = model(**tokens)

    scores = output[0][0].detach().numpy()
    scores = expit(scores)
    return class_mapping[np.argmax(scores)]

def build_df(df):
    df["Topic"] = df.Cleaned_Tweets.apply(analyze_topic)
    print(df.head())
    return df
if __name__ == "__main__":
    # make connnection
    con = create_connection(r"./db/database.db")
    cursor = con.cursor()
    
    # create table 
    create_table(
    cursor,
        """CREATE TABLE IF NOT EXISTS Tweets (
                                ["Retweets", "Likes","Date","Cleaned_Tweets"]
                                Cleaned_Tweets TEXT PRIMARY KEY, 
                                Retweets INTEGER, 
                                Likes INTEGER,
                                Date DATETIME,
                                Topic TEXT);""",
    )
    df = load_orginal_dataset()
    df = build_df(df)
    df.to_sql("Tweets", con, if_exists='replace', index=False) # writes to file
    con.commit()
    con.close()
    
    