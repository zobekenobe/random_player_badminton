import streamlit as st
import numpy as np
import pandas as pd
import time 
from st_btn_select import st_btn_select

st.set_page_config('UCD Badminton Socials')
st.title('UCD Badminton Socials')
st.title('Random Player Selector')
st.sidebar.subheader('About')
st.sidebar.write(f'1. Create you list of players in a GOOGLE SHEET')
st.sidebar.write(f'2. Enter the available courts for the day and the time alotted for each session')
st.sidebar.write(f'3. Press start and session runs for upto 1 hour before auto reset')

num_of_courts = st.sidebar.number_input(label = 'Enter the number of courts available',min_value = 1, max_value = 6, step = 1)
session_time  = st.sidebar.number_input(label = 'Enter the time for each session', min_value = 5, max_value = 25, step = 1)

num_of_sessions = int(60/session_time)
wait_time = int(60 * session_time/100)


sheetlink = st.sidebar.text_input(label = 'Enter the link to the Google Spreadsheet')
col1, col2 = st.sidebar.columns([0.25,1])
with col1:
    if not st.button('Start'):
        st.stop()
with col2:
    if st.button('Stop'):
        st.stop()

newlink   = sheetlink.split('/')[-2]
filename  = 'https://docs.google.com/spreadsheets/d/' +  newlink + '/gviz/tq?tqx=out:csv'			    
			    
# filename = st.sidebar.file_uploader(label = 'Enter a .csv file with names of players')
# if filename is not None:
df = pd.read_csv(filename)
df.columns = ['Players']
players = df.copy()


progress_bar = st.sidebar.progress(0)
status_text = st.sidebar.empty()

if(len(df) < num_of_courts*4):
    st.write(f'Insufficient players for {num_of_courts}')
else:
#     while(len(players) > 4):
    for session in range(num_of_sessions):
        old_people = []
        st.subheader(f'Session : {session+1}')
        st.write('************************************')
        if len(players) < 4:
            num_of_required_people = 4 - len(players)
            if len(old_people) == 0:
                st.write('Insufficient Number of players to play doubles')
            else:
                extra_players = np.random.choice(old_people, num_of_required_people, replace = False)
                players = pd.concat([players, pd.DataFrame({'Players' : extra_players})],ignore_index = True)
                st.write(f'Court Number {court%num_of_courts + 1}')
                st.table(pd.DataFrame(np.random.choice(players.Players.values, 4, replace = False).tolist(), columns = ['Players']))
                players = df.copy()
                np.random.shuffle(players.Players.values)
        for court in range(num_of_courts):
            st.write(f'Court Number {court+1}')
            new_people = np.random.choice(players.Players.values, 4, replace = False ).tolist()
            players = players[~players.Players.isin(new_people)]
            st.table(pd.DataFrame(new_people, columns = ['Players']))
            old_people += new_people
        
        
        for i in range(1, 101):
            status_text.text(f'{i}% Session {session+1} Complete')
            time.sleep(wait_time)
            progress_bar.progress(i)
        
        progress_bar.empty()
       
        players = df.copy()
        np.random.shuffle(players.Players.values)

    
    st.write('\n')
	
