from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji


def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    if selected_user == 'Overall':
        # number of messages
        num_messages = df.shape[0]

        # number of words
        words = []
        for message in df['message']:
            words.extend(message.split())

        # number of media messages
        num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

        # number of links (assuming links are identified in some way in your data)
        num_links = df[df['message'].str.contains('http')].shape[0]

        return num_messages, len(words), num_media_messages, num_links
    else:
        new_df = df[df['user'] == selected_user]

        # number of messages for the selected user
        num_messages = new_df.shape[0]

        # number of words for the selected user
        words = []
        for message in new_df['message']:
            words.extend(message.split())

        # number of media messages for the selected user
        num_media_messages = new_df[new_df['message'] == '<Media omitted>\n'].shape[0]

        # number of links for the selected user
        num_links = new_df[new_df['message'].str.contains('http')].shape[0]

        return num_messages, len(words), num_media_messages, num_links
#
def most_busy_users(df):
    x = df['user'].value_counts().head()
    df=round (df['user'].value_counts()/df.shape[0] *100,2).reset_index().rename(columns={'count':'Percentage','user':'Name'})
    return  x,df


def create_wordcloud(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=""))
    return df_wc  # Return the WordCloud object, not the image

def most_common_words(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

def monthly_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline


def daily_timeline(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline
