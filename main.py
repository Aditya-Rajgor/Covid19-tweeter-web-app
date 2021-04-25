import streamlit as st
import os
import pandas as pd
from datetime import date
from datetime import timedelta


col1, col2, col3, col4 = st.beta_columns([0.3, 12, 1, 4])
with col1:
    st.write("")

with col2:
    st.write("")
    st.markdown('<h1>Live Covid-19 patients/helpers information From Tweeter</h1>', unsafe_allow_html=True)

with col3:
    st.write('')
with col4:
    st.image('Static/tweeter_black-removebg-preview.png', width=150)

st.write('''
## Select your city and help them NOW!
''')

IS_HELPER = st.radio("What's your Status?", ("I'm recovered and/or I have equipments", "Me/My acquaintance is/are positive and needs help to fight against covid-19"))
if IS_HELPER == "I'm recovered and/or I have equipments":
    test_list = st.multiselect('I can provide...', ['vantilator', 'oxygen', 'remdesvir', 'plazma', 'bed'],
                               default='oxygen')
else:
    test_list = st.multiselect("I need...", ['vantilator', 'oxygen', 'remdesvir', 'plazma', 'bed'],
                               default='oxygen')

st.sidebar.title('Filters')

if len(test_list) == 1:
    test_string = '"' + test_list[0] + '"'
elif len(test_list) == 2:
    test_string = '("' + test_list[0] + '"' + ' OR ' + '"' + test_list[1] + '")'
elif len(test_list) == 3:
    test_string = '("' + test_list[0] + '"' + ' OR ' + '"' + test_list[1] + '"' + ' OR ' + '"' + test_list[0] + '")'
elif len(test_list) == 4:
    test_string = '("' + test_list[0] + '"' + ' OR ' + '"' + test_list[1] + '"' + ' OR ' + '"' + test_list[
        2] + '"' + ' OR ' + '"' + test_list[3] + '")'
else:
    st.write('please select your needs')

start_date_input = st.sidebar.date_input('From Date', date.today() - timedelta(days=2))
end_date_input = st.sidebar.date_input('To Date', date.today())


def Scraper(city, start_date, end_date, test_string, is_helper):
    sd = start_date.strftime("%Y-%m-%d")
    ed = end_date.strftime("%Y-%m-%d")
    if is_helper == "I'm recovered and/or I have equipments":
        query = 'snscrape --jsonl --max-results 10000 twitter-search "(("covid" OR "corona" OR "coronavirus" OR "positive" OR "ve") AND ' + '"{}"'.format(city) + ') AND ((("need" OR "help" OR "required" OR "require" OR "want") AND ' + test_string + ') AND ("contact" OR "mobile" OR "call" OR "number" OR "91" OR "message" OR "phone" OR "num" OR "tel")) -Bhumi -Available since:' + sd + " until:" + ed + '" > COVID_data.json'
        os.system(query)

    elif is_helper == 'Me/My acquaintance is/are positive and needs help to fight against covid-19':
        query = 'snscrape --jsonl --max-results 10000 twitter-search "(("covid" OR "corona" OR "coronavirus" OR "positive" OR "ve") AND ' + '"{}"'.format(city) + ') AND (("Available" AND ' + test_string + ') AND ("contact" OR "mobile" OR "call" OR "number" OR "91" OR "message" OR "phone" OR "num" OR "tel")) since:' + sd + " until:" + ed + '" > COVID_data.json'
        os.system(query)

    else:
        st.write('please select one radio button argument')

    df = pd.read_json('COVID_data.json', lines=True)
    df = df.drop_duplicates('content')
    df = df.reset_index(drop=False)

    if df.shape[0] == 0:
        st.write('''
            No result found,
            - Check the internet connection
            - Please check the spelling of the your city
            - Include more days from the filter menu to see the earlier results
            ''')
    else:
        st.write('Total Number of people with needs of', test_string, 'in', city, "is", len(df['content']))
        iterator = st.sidebar.slider("Visible tweets", 1, len(df) - 1, (1, min(10, len(df)-1)), 1)
        df['Date'] = pd.to_datetime(df['date'], utc=False).dt.date

        st.markdown('---')
        st.write(
            '--------------------------------------------------Tweets--------------------------------------------------')

        for i in range(iterator[0], iterator[1] +1):
            st.markdown('<hr style="solid black"> </hr>', unsafe_allow_html=True)
            st.write(i, 'Posted On: ', df.loc[i, 'date'], '  [ Go to the tweet](', df.loc[i, 'url'], ')')
            st.write(df.loc[i, 'content'])

        st.markdown(
            '<h4>To see more tweets slide the visible tweets slider<br>Or change the Dates accordingly from the filter menu(left side)</h4><br><br>',
            unsafe_allow_html=True)

        st.markdown('**Below** chart is just to get the idea of the spread of the **above** tweets')
        st.line_chart(data=df.groupby('Date')[['replyCount', 'retweetCount', 'likeCount']].sum())


user_input = st.text_input("I'm from...", 'Ahmedabad')

Scraper(user_input, start_date_input, end_date_input, test_string, IS_HELPER)

st.markdown('<div style="padding: 10px; border: 1px solid transparent; border-color: transparent; margin-bottom: 20px; border-radius: 10px; color: #00ab05; background-color:#9cff9f; border-color: #47fc4c;">Spread the information and keep your close ones safe #StayHomeStaySafe</div>', unsafe_allow_html=True)

st.markdown('''
## Contact Me for any bug report or feedback
- [LinkedIn](https://www.linkedin.com/in/aditya-rajgor/)
- [Mail](https://mail.google.com/mail/u/0/?ogbl&sw=2&token=%5B%22cftp%22,%22e820988a7e%22,%22gmail_fe_200226.09_p3%22,%22ZyMrc6cBAw-rFZnvtXyj5A%5Cu003d%5Cu003d%22,%227016,7607,6821,7465,7414,6984,7591,6792,7158,7418,7416,6807,7634,7189,6929,7150,7642,7618,7443,7018,7728,7495,7711,7546,7278,7068,7569,7156,7433,7584,7565,7467,7708,7655,7113,6999,7027,7636,7393,7236,7332,7424,7407,7609,7030,7348,7164,7172,7403,7500,6969,7137,7645,7272,6804,7419,7468%22,1%5D&dilte=0&mme=0&gme=1&sme=0#inbox?compose=GTvVlcRzBlSNxrvPZxDXMtlnZfSQMHHcTZWkgFWdDQQdddVhkfdqqtCkhlwcgNJVHKbQKSjRtrPld) 
- [GitHub](https://github.com/Aditya-Rajgor) (Source code will be updated soon)
''', unsafe_allow_html=False)