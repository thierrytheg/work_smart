matrix = [
    [0, 5, 6, 4, 7, 4],
    [5, 0, 5, 4, 6, 5],
    [6, 5, 0, 4, 5, 5],
    [4, 4, 4, 0, 5, 5],
    [7, 6, 5, 5, 0, 4],
    [4, 5, 5, 5, 4, 0],
]

names = ["Action", "Adventure", "Comedy", "Drama", "Fantasy", "Thriller"]
import requests

url = "https://api.shahin.dev/chord"
payload={'names': names, 'matrix':matrix,'width': 500,'title':'Intercompany Balances','verb':' '}
     

import streamlit as st

user=st.secrets["user"]
key=st.secrets["key"]

result = requests.post(url, json=payload, auth=(user, key))



import json

c=result.content.decode("utf-8")

import streamlit.components.v1 as components

# bootstrap 4 collapse example
components.html(
    c,
    height=1000
)

#https://github.com/shahinrostami/chord/blob/master/chord/__init__.py
