
import streamlit as st


#from streamlit_autorefresh import st_autorefresh
import pandas as pd
import matplotlib.pyplot as plt  
import datetime
import time


import matplotlib.pyplot as pyplot
st.set_page_config(layout="wide")

from streamlit_autorefresh import st_autorefresh



def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("styles.css")


def color_cells(val):
    if val <-200:
        return 'background-color: grey '
    elif val <-100:
       return 'background-color: red'
    elif val <5:
       return 'background-color: red'
    elif val <10:
       return 'background-color: yellow'
    elif val < 15:
      return 'background-color: green'
    else:
        return 'background-color: white'


def calculate_countdown(deadline):
    now = datetime.datetime.now()
    countdown = deadline - now
    countdown_minutes = countdown.total_seconds() / 60
    return round(countdown_minutes, 2)

# Add countdown column



 # Function to display countdown timer for each row
def countdown_timer(seconds):
     for i in range(seconds, 0, -1):
         st.write(f"Time remaining: {i} seconds")
         time.sleep(1)
     st.write("Countdown finished!")

 # Display the data table


def getsqlengine(db=0):
    import pyodbc
    import sqlalchemy as sal

    USERNAME = 'c_userv1'
    PASSWORD = 'packets@1'
    SERVER = 'sqlag1'
    # Set your connection credentials
    if db==0:

           
        DATABASE = 'YodelTracking'
           
    else:
           
        DATABASE = 'Vesta'
      

    # Create a connection string using string interpolation

    connectionString = f'DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};MultiSubnetFailover=yes;Encrypt=no;UID={USERNAME};PWD={PASSWORD}'
    engine = sal. create_engine(f"mssql+pyodbc:///?odbc_connect={connectionString}")

# Connect to the SQL database
    # conn = pyodbc.connect(connectionString)
    # return engine

    #  connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};MultiSubnetFailover=yes;Encrypt=no;UID={USERNAME};PWD={PASSWORD}'
    #  engine = sal. create_engine(f"mssql+pyodbc:///?odbc_connect={connectionString}")

# Connect to the SQL database
    conn = pyodbc.connect(connectionString)
    return engine

def fetch_data():

    query="Select * from [JobLogic].V_TimetoAllocate  order by 3 desc"
    # df=pd.read_sql_query(query ,con=md.filemanagement.getsqlengine(1))
    #query = "SELECT * FROM your_table"  # Replace with your SQL query
    df = pd.read_sql(query, getsqlengine(1))
    df['Countdown (minutes)'] = df['localtime'].apply(calculate_countdown)
    dfa=df
    #df[['Supplier', 'Amount']] .groupby('Supplier') .sum().reset_index()
    print(dfa.head(10))
    return dfa.reset_index(drop=True)

st_autorefresh(interval=1000, limit=None, key="refresh")
# Title of the app



st.title('Simple Streamlit App')


df=fetch_data()
# Create a bar chart using matplotlib
#fig, ax = plt.subplots()
#ax.bar(df['Supplier'], df['Amount'])
#ax.set_xlabel('Category', rotation=90)
#ax.set_ylabel('Values')
#ax.set_title('Bar Chart Example')
#ax.tick_params(axis='x', rotation=90)

 # Display the bar chart in Streamlit
#st.pyplot(fig)

styled_a = df.style.applymap(color_cells, subset=['Countdown (minutes)'])#.reset_index(drop=True)
styled_df=styled_a.set_table_styles([{'selector': 'th', 'props': [('font-weight', 'bold')]}, {'selector': 'td', 'props': [('font-size', '2px')]} ])

#st.dataframe(styled_df, use_container_width=True)

st.dataframe(styled_df, use_container_width=True,  hide_index=True, height=600)

 # Create a countdown timer for each row
 #   st.write(f"Item: {df['Amount']}")
#    countdown_timer(15)






#st.write("This page will refresh every 5 minutes.")


# Display the input text

