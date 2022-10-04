#This program runs the streamlit application for Tim's Wedding bets

#import nescessary libraries
import pandas as pd 
import streamlit as st
import datetime
from google.oauth2 import service_account
from gspread_pandas import Spread,Client

#Google credential scripts

#Create a google authenitfication connection object
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = service_account.Credentials.from_service_account_info(
                st.secrets["gcp_service_account"], scopes = scope)

client = Client(scope=scope,creds=credentials)
spreadsheetname = "tims_bets"
spread = Spread(spreadsheetname,client = client)

sh = client.open(spreadsheetname)

# Check the connection( It Worked! )
#st.write(spread.url)

# Get the sheet as a dataframe
def load_the_spreadsheet(spreadsheetname):
    worksheet = sh.worksheet(spreadsheetname)
    df = pd.DataFrame(worksheet.get_all_records())
    return df

# Update to Sheet
def update_the_spreadsheet(spreadsheetname,dataframe):
    cols = ['Participant','bet_1','bet_2','bet_3','bet_4','bet_5','bet_6','bet_7','bet_8','bet_9','bet_10']
    spread.df_to_sheet(dataframe[cols],sheet = spreadsheetname,index = False)
    

def score_df(df):
    score_list = []
    for index, row in df.iterrows():
        score = 0
        #TBA
        if row['bet_1'] == 'Yes':
            score += 1
        #TBA
        if row['bet_2'] == 'Yes':
            score += 1
        #ANSWERED
        if row['bet_3'] == 'No':
            score += 1
        #ANSWERED
        if row['bet_4'] == 'Yes':
            score += 1
        #TBA
        if row['bet_5'] == 'Yes':
            score += 1
        #ANSWERED
        if row['bet_6'] == 'No':
            score += 1
        #ANSWERED
        if row['bet_7'] == 'Matthew':
            score += 1
        #ANSWERED
        if row['bet_8'] == 'Yes':
            score += 1
        #ANSWERED
        if row['bet_9'] == 'Yes':
            score += 1
        #TBA
        if row['bet_10'] == 'Over':
            score += 1
        score_list.append(score)

    df['score'] = score_list    
    
    df = df.sort_values(by = ['score'], ascending = False)

    return df

# def score_check(df, name = 'default'):
#     if name == 'default':
#         value = ''
#     if name != 'default':
#         value = 'Score: ' + str(df.loc[df['Participant'] == name_check, 'score'].iloc[0])
#     return value
#BETS
#Will Adeline enter the church before or after 12:00pm?
#Will Tim cry?
#Will Adeline wear a veil?
#Will Genesis be one of the readings?
#Will the Gospel be Matthew, Mark, Luke, or John?
#Will Fr. James mention wrestling/WWE during the Homily?
#Will Tim do the 'Randy Orton' pose inside Our Lady of the Assumption (church)?
#Will Adeline kneel during the Mass?
#Will Tim & Adeline sign the documents inside the church?
#Will the wedding Mass be Over/Under 50:00 min?

y_n_answers = ['Yes','No']
gospel_answers = ['Matthew','Mark','Luke','John']
b_a_answers = ['Before','After']
o_u_answers = ['Over','Under']



st.title("Welcome to Tim and Adeline's Wedding Bets!")

time = datetime.datetime.now().time()

crux = datetime.time(11,56,0)

mass_end = datetime.time(13,00,0)



if time < crux:

    
    st.text("Simply input your name! Select your bets from the drop down menus! Then hit submit!")
    st.text('You will only be able to enter your answers until 11:55am!')
    st.text("Then after the wedding mass is finished check back here for the results!")

    st.header('Input your name!')
    st.subheader('First and Last Names Please!')
    name = st.text_input('Your Name!')

    st.subheader('Bet #1')
    st.text('Will Adeline walk down the aisle for Mass before 12:05pm?')
    bet1_answer = st.selectbox('Answer #1',y_n_answers)

    st.subheader('Bet #2')
    st.text('Will Tim cry?')
    bet2_answer = st.selectbox('Answer #2',y_n_answers)

    st.subheader('Bet #3')
    st.text('Will Adeline wear a veil?')
    bet3_answer = st.selectbox('Answer #3',y_n_answers)

    st.subheader('Bet #4')
    st.text('Will one of the readings be from the book of Genesis?')
    bet4_answer = st.selectbox('Answer #4',y_n_answers)

    st.subheader('Bet #5')
    st.text('Will Fr.James mention wrestling/WWE during the homily?')
    bet5_answer = st.selectbox('Answer #5',y_n_answers)

    st.subheader('Bet #6')
    st.text("Will Tim do the 'Randy Orton' pose inside Our Lady of Assumption Church?")
    bet6_answer = st.selectbox('Answer #6',y_n_answers)

    st.subheader('Bet #7')
    st.text('Will thge Gospel be from Matthew, Mark, Luke, or John?')
    bet7_answer = st.selectbox('Answer #7',gospel_answers)

    st.subheader('Bet #8')
    st.text('Will Adeline kneel during the Mass?')
    bet8_answer = st.selectbox('Answer #8',y_n_answers)

    st.subheader('Bet #9')
    st.text('Will Tim and Adeline sign the wedding documents inside the church?')
    bet9_answer = st.selectbox('Answer #9',y_n_answers)

    st.subheader('Bet #10')
    st.text('Will the Wedding Mass be Over/Under 50 minutes long?')
    bet10_answer = st.selectbox('Answer #10',o_u_answers)

    st.text('')
    st.text('Happy with your bets? Hit submit!')
    st.text("Don't leave the page until it says 'Entry Added'")
    
    
    submit = st.button('Submit')


    answers = {'Participant':name,
            'bet_1':bet1_answer,
            'bet_2':bet2_answer,
            'bet_3':bet3_answer,
            'bet_4':bet4_answer,
            'bet_5':bet5_answer,
            'bet_6':bet6_answer,
            'bet_7':bet7_answer,
            'bet_8':bet8_answer,
            'bet_9':bet9_answer,
            'bet_10':bet10_answer}


    if submit:
        submit_df = pd.DataFrame(answers, index = [0])
        df = load_the_spreadsheet('tims_bets')
        new_df = df.append(submit_df,ignore_index=True)
        update_the_spreadsheet('tims_bets',new_df)

        st.subheader('Entry Added!')
        








elif time > crux and time < mass_end:

    st.subheader('The time for betting is over! The bets are placed! Time to witness this beautiful Sacrament of Marriage, head over to the livestream!')
    st.subheader('Livestream Link:')
    st.markdown('https://youtube.com/channel/UCedrWgfNmAzEwN0Knv2zVNg',unsafe_allow_html= True)

else:
    st.subheader('The Wedding is over congratulations to the Tim and Adeline!')
    st.subheader('On another note! Here are the bet results!')

    st.title('Results!')

    results_df = load_the_spreadsheet('tims_bets')

    scored_df = score_df(results_df)

    st.header('1st Place 🥇:   ' + scored_df.iloc[0]['Participant'])
    st.text('Correct Answers: '+ str(scored_df.iloc[0]['score']))
    st.header('2nd Place 🥈:   ' +scored_df.iloc[1]['Participant'])  
    st.text('Correct Answers: '+str(scored_df.iloc[1]['score']))
    st.header('3rd Place 🥉:   ' +scored_df.iloc[2]['Participant'])  
    st.text('Correct Answers: '+str(scored_df.iloc[2]['score']))

    st.text('')
    st.text('')
    st.subheader("Didn't place in the top 3? Enter your name and see your result!")

    list_of_names = scored_df['Participant'].values.tolist()

    if 'name' not in st.session_state:
        st.session_state.name = 'default'
        

    name_search = st.text_input('Enter name')

    if name_search:
        st.session_state.name = name_search

   

        if st.session_state.name != 'default':
            if st.session_state.name in  list_of_names:
                st.subheader('Score: ' + str(scored_df.loc[scored_df['Participant'] == st.session_state.name, 'score'].iloc[0]))
            else:
                st.subheader('That name was not found, try again!')
