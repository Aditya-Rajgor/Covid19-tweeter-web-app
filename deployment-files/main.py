import streamlit as st
import tweepy
import pandas as pd
from datetime import date
from datetime import timedelta

#Get this by activating tweeter developer account
api_key = 'Your API Key'
api_secret_key = 'Your API Secret Key'
access_token = 'Your token'
access_token_secret = 'Your token secret'

authenticate = tweepy.OAuthHandler(consumer_key=api_key,consumer_secret=api_secret_key)
authenticate.set_access_token(access_token, access_token_secret)
api = tweepy.API(authenticate, wait_on_rate_limit=True)

authenticate = tweepy.OAuthHandler(consumer_key=api_key,consumer_secret=api_secret_key)
authenticate.set_access_token(access_token, access_token_secret)
api = tweepy.API(authenticate, wait_on_rate_limit=True)

col1, col2, col3, col4 = st.beta_columns([0.3, 12, 2, 1])

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
## Select your city and **GET/GIVE** Help NOW!
''')
st.info('Recommend using "desktop site" for better site seeing, open filter menu from the top left arrow(फिल्टर मेनू से फ़िल्टर चुनें)')
IS_HELPER = st.radio("What's your Status?", ("I'm recovered and/or I have equipments(मैं मदद करना चाहता हूँ)", "Me/My acquaintance is/are positive and needs help to fight against covid-19 (मुझे मदद की ज़रूरत है)"))
if IS_HELPER == "I'm recovered and/or I have equipments(मैं मदद करना चाहता हूँ)":
    test_list = st.multiselect('I can provide...(मैं प्रदान कर सकता हूं)', ['vantilator', 'oxygen', 'remdesvir', 'plazma', 'bed'],
                               default='oxygen')
else:
    test_list = st.multiselect("I need...(मुझे जरूरत है)", ['vantilator', 'oxygen', 'remdesvir', 'plazma', 'bed'],
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
elif len(test_list) == 5:
    test_string = '("' + test_list[0] + '"' + ' OR ' + '"' + test_list[1] + '"' + ' OR ' + '"' + test_list[
        2] + '"' + ' OR ' + '"' + test_list[3] + '")'+ ' OR ' + '"' + test_list[4] + '")'
else:
    st.write('''
    ## please select one option from above 
    ''')
    st.stop()

start_date_input = st.sidebar.date_input('From Date', date.today() - timedelta(days=2))
end_date_input = st.sidebar.date_input('To Date', date.today())

def Scraper(city, start_date, end_date, is_helper, test_string):
    sd = start_date.strftime("%Y-%m-%d")
    ed = end_date.strftime("%Y-%m-%d")

    retweet_count = []
    tweets = []
    created_at = []
    if is_helper == "I'm recovered and/or I have equipments(मैं मदद करना चाहता हूँ)":
        Tweets = tweepy.Cursor(api.search, tweet_mode="extended",
                               q='(("covid" OR "corona" OR "coronavirus" OR "positive" OR "ve") AND ' + '"{}"'.format(city) + ') AND ((("need" OR "help" OR "required" OR "require" OR "want") AND ' + test_string + ') AND ("contact" OR "mobile" OR "call" OR "number" OR "91" OR "message" OR "phone" OR "num" OR "tel")) -Bhumi -Available' + " -filter:retweets",
                               since=sd,
                               until=ed).items(50)


        for tweet in Tweets:
            tweets.append(tweet.full_text)
            created_at.append(tweet.created_at)
            retweet_count.append(tweet.retweet_count)

        st.write('Total Number of people with needs of', test_string, 'in', city, 'between',start_date,'and',end_date, "is", len(created_at))


    elif is_helper == 'Me/My acquaintance is/are positive and needs help to fight against covid-19 (मुझे मदद की ज़रूरत है)':
        Tweets = tweepy.Cursor(api.search, tweet_mode="extended",
                               q='(("covid" OR "corona" OR "coronavirus" OR "positive" OR "ve") AND ' + '"{}"'.format(city) + ') AND (("Available" AND ' + test_string + ') AND ("contact" OR "mobile" OR "call" OR "number" OR "91" OR "message" OR "phone" OR "num" OR "tel"))' + " -filter:retweets",
                               since=sd,
                               until=ed).items(50)

        for tweet in Tweets:
            tweets.append(tweet.full_text)
            created_at.append(tweet.created_at)
            retweet_count.append(tweet.retweet_count)

        st.write('Total Number of people with availability of', test_string, 'in', city, 'between',start_date,'and',end_date, "is", len(created_at))

    else:
        st.write('please select one radio button argument')

    CREATED_AT = [d.strftime('%Y-%m-%d')
            for d in created_at]

    df = pd.DataFrame({
        'Date':CREATED_AT,
        'content':tweets,
        'retweetCount':retweet_count
    })
    df['Date'] = pd.to_datetime(df['Date'])

    if df.shape[0] == 0:
        st.write('''
            No result found,
            - Check the internet connection
            - Please check the spelling of the your city
            - Include more days from the filter menu to see the earlier results
            ''')
    else:
        iterator = st.sidebar.slider("Visible tweets", 1, len(df) - 1, (1, min(10, len(df)-1)), 1)


        st.markdown('---')
        st.write(
            '--------------------------------------------Tweets(Max-50)---------------------------------------------')

        for i in range(iterator[0], iterator[1] +1):
            st.markdown('<hr style="solid black"> </hr>', unsafe_allow_html=True)
            st.write(i, 'Posted On: ', df.loc[i, 'Date'])
            st.write(df.loc[i, 'content'])

        st.markdown(
            '<h4>To see more tweets slide the visible tweets slider<br>Or change the Dates accordingly from the filter menu(left side)</h4><br><br>',
            unsafe_allow_html=True)

        st.markdown('**Below** chart represents number of retweets against **given** tweets')
        st.line_chart(data=df.groupby('Date')[['retweetCount']].sum())


user_input = st.text_input("I'm from...(मेरा शहर)", 'Ahmedabad')

Scraper(user_input, start_date_input, end_date_input, IS_HELPER, test_string)

st.markdown('<div style="padding: 10px; border: 1px solid transparent; border-color: transparent; margin-bottom: 20px; border-radius: 10px; color: #00ab05; background-color:#9cff9f; border-color: #47fc4c;">Spread the information and keep your close ones safe #StayHomeStaySafe</div>', unsafe_allow_html=True)
st.markdown('<div style="padding: 10px; border: 1px solid transparent; border-color: transparent; margin-bottom: 20px; border-radius: 10px; color: #d61a1a; background-color:#cc6464; border-color: #d10000;">I run query to get the tweets and it"s possible that information might be incorrect, I do not claim that to be true</div>', unsafe_allow_html=True)

st.markdown('''
## Contact Me for any bug report or feedback
- [LinkedIn](https://www.linkedin.com/in/aditya-rajgor/)
- <a href = "mailto:adityarajgor88@gmail.com?subject=Feedback regarding web-app&body=Thanks for considering,...">Mail</a>
- [GitHub](https://github.com/Aditya-Rajgor) (Source code will be updated soon)
- [Working demo](https://www.loom.com/share/3c2d3eda08d04f7c9c9bfae0ab1bdf08)
''', unsafe_allow_html=True)
