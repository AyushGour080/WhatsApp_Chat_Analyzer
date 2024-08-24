import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
import emoji

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    # Fetch unique user
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0, "Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user, df)

        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1])  # Adjusted column widths for proper alignment

        with col1:
            st.markdown("<h3 style='text-align: center;'>Total Messages</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:24px; text-align: center;'>{num_messages}</p>", unsafe_allow_html=True)

        with col2:
            st.markdown("<h3 style='text-align: center;'>Total Words</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:24px; text-align: center;'>{words}</p>", unsafe_allow_html=True)

        with col3:
            st.markdown("<h3 style='text-align: center;'>Media Shared</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:24px; text-align: center;'>{num_media_messages}</p>", unsafe_allow_html=True)

        with col4:
            st.markdown("<h3 style='text-align: center;'>Link Shared</h3>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size:24px; text-align: center;'>{num_links}</p>", unsafe_allow_html=True)

        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Finding the busy user in the group
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)

        # Wordcloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        st.title("Most Top Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(most_common_df[0], most_common_df[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title('User Distribution')
        user_distribution = df['user'].value_counts()
        fig_user_dist, ax_user_dist = plt.subplots()
        ax_user_dist.pie(user_distribution, labels=user_distribution.index, autopct='%1.1f%%', startangle=90)
        ax_user_dist.set(aspect="equal")  # Equal aspect ratio ensures that pie is drawn as a circle
        st.pyplot(fig_user_dist)
