"""

Use sqlite3 to load data and cardiffnlp/tweet-topic-21-multi from hugging face to analyze the topic and store it as a new table

"""

import sqlite3
import pandas as pd
from sqlite3 import Error

def load_orginal_dataset(source = "")

