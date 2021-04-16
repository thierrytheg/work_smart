import altair as alt
import pandas as pd
import streamlit as st
import base64
import os
import matplotlib.pyplot as plt
import numpy as np
import requests
import json
import streamlit.components.v1 as components
from PIL import Image

image=Image.open('linkedin.png')
st.image(image)



def download_link_csv(object_to_download, download_filename, download_link_text):
    if isinstance(object_to_download,pd.DataFrame):
        object_to_download = object_to_download.to_csv(index=False)

    b64 = base64.b64encode(object_to_download.encode()).decode()
    return f'<a href="data:file/txt;base64,{b64}" download="{download_filename}">{download_link_text}</a>'

option=st.sidebar.selectbox("options",("Choose one of the options below","GL Outliers","Intercompany"))

#linkedin='<script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script><div class="badge-base LI-profile-badge" data-locale="en_US" data-size="medium" data-theme="dark" data-type="HORIZONTAL" data-vanity="thierry-haddad" data-version="v1"><a class="badge-base__link LI-simple-link" href="https://ca.linkedin.com/in/thierry-haddad?trk=profile-badge">Thierry Haddad</a></div>'
linkedin='<script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script><div class="badge-base LI-profile-badge" data-locale="en_US" data-size="medium" data-theme="dark" data-type="HORIZONTAL" data-vanity="thierry-haddad" data-version="v1"><a class="badge-base__link LI-simple-link" href="https://ca.linkedin.com/in/thierry-haddad?trk=profile-badge"></a></div>'

if option=="Choose one of the options below":
    components.html(linkedin,height=1000)
if option=="Intercompany":
    matrix = [
    [0, 5, 6, 4, 7, 4],
    [5, 0, 5, 4, 6, 5],
    [6, 5, 0, 4, 5, 5],
    [4, 4, 4, 0, 5, 5],
    [7, 6, 5, 5, 0, 4],
    [4, 5, 5, 5, 4, 0],
]

    names = ["Action", "Adventure", "Comedy", "Drama", "Fantasy", "Thriller"]
    

    url = "https://api.shahin.dev/chord"
    payload={'names': names, 'matrix':matrix,'width': 500,'title':'Intercompany Balances','verb':' ','padding':0.5}


    

    user=st.secrets["user"]
    key=st.secrets["key"]

    result = requests.post(url, json=payload, auth=(user, key))


    c=result.content.decode("utf-8")



    #  4 collapse example
    components.html(
        c,
        height=1000
    ) 
if option=="GL Outliers":





    uploaded_file = st.file_uploader("Choose a file")

    try:
        if uploaded_file is not None:
            try:
                df=pd.read_excel(uploaded_file)

            except:
                try:
                    df=pd.read_csv(uploaded_file)

                except:
                    pass

        else:
            df=pd.read_excel('sample_data.xlsx')
            st.error("You are currently viewing a sample dataset. Upload your own file to view your data.")
    except:
        pass

    add_slidebar1= st.slider('Sensitivity', 0, 100, 50,help='Drag the slider to the right to increase the sensitivity which will result in more outliers detected. Drag to the slider to the left to decrease the sensitivity and reduce the number of outliers. ')


    try:

        for n in range(len(df.columns)):
            if ('acc' or 'account') in (df.columns[n]).lower():
                df['Account']=df[df.columns[n]]

                add_selectbox = st.selectbox(
                "Select an account from the list below",
                sorted(list(df.Account.unique())))   

        #Detect column with dollar values
        for n in range(len(df.columns)):
            if ('am' or 'amount') in (df.columns[n]).lower():
                df['Amount']=df[df.columns[n]]


        new_columns=['Account','Amount']
        for column in new_columns:
            if column in df.columns:
                pass
            else:
                st.write("Unable to detect your %s column. Please rename the appropriate column '%s' and re-upload the file" %(column,column))
    except:
        pass



    q1_sensitivity=add_slidebar1/100
    q3_sensitivity=1-q1_sensitivity

    def render(account):
      selected=df[df.Account==account]

      outlierq3=(selected[selected.columns].loc[selected['Amount']>(np.quantile(selected['Amount'],q3_sensitivity))])
      outlierq1=(selected[selected.columns].loc[selected['Amount']<(np.quantile(selected['Amount'],q1_sensitivity))])



      quant=[]
      quant.append([abs(np.quantile(selected['Amount'],q3_sensitivity)),abs(np.quantile(selected['Amount'],q1_sensitivity))])

      if (len(outlierq1) and len(outlierq3)) == 0:
        st.write("No outliers were detected for this account")

      else:

        df_final=pd.concat([outlierq1,outlierq3])
        df_final=df_final.drop_duplicates()

        st.write("Outliers Detected: **%s**" %df_final.shape[0])

        st.write(df_final)

        tmp_download_link_csv = download_link_csv(df_final, 'your_outliers.csv', 'Download you file here.')
        st.markdown(tmp_download_link_csv, unsafe_allow_html=True)

        return alt.Chart(selected).mark_boxplot().encode(y='Amount',).properties(width=300,height=500).configure_boxplot(extent=1-(add_slidebar1/100))


    try:    

        st.altair_chart(render(add_selectbox),use_container_width=True)

    except Exception as e:
        pass




#https://github.com/shahinrostami/chord/blob/master/chord/__init__.py
