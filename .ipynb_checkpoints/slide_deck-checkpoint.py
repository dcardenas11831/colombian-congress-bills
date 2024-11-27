import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

def main():
    st.set_page_config(page_title="Colombian Congress Analysis", layout="wide", page_icon="./Images/colombian_flag.png")
    
    # Initialize session state for tracking slides and responses
    if 'slide' not in st.session_state:
        st.session_state.slide = 0
    if 'responses' not in st.session_state:
        st.session_state.responses = {}
    
    # Slide content
    slides = [
        slide_introduction,
        slide_context_1,
        slide_context_2,
        slide_context_3,
        slide_game_intro,
        slide_tweets,
        slide_interactive_questions,
        slide_results
    ]
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        if st.session_state.slide > 0:
            if st.button("Previous"):
                st.session_state.slide = max(0, st.session_state.slide - 1)

    with col3:        
        if st.session_state.slide < len(slides) - 1:
            if st.button("  Next  "):
                st.session_state.slide = min(len(slides) - 1, st.session_state.slide + 1)
    
    # Render current slide
    slides[st.session_state.slide]()

def slide_introduction():
    st.title("Analysing Party Positions in the Colombian Congress Bills")
    st.image("./Images/colombian_flag.png", width=50)
    st.write("""
    ### This project aims to discover the effect of the Opposition Statute (2018) on the bills presented to Congress between 2022 and 2024.
    
    - The analysis was done over 725 bills presented to the Senate. Each one was webscrapped for its metadata and its text was collected through OCR.
    - Based on the authors party's position each bill was assigned a value of how much in favor of the goverment, independent or opposition is the proposal.
    - An LDA Topic Modeling was done to see the main topics of the corpus and see the relation they have to the positions of the bills.
    """)

def slide_context_1():
    st.title("Context: The Opposition Statute")
    st.write("""
    It is a bill that requires politial parties to declare as Opposition, Independent or as part of the Government Coalition.
    """)
    remark = "This should strengthen parties and make congresspeople pursue the party's policy preferences."

    st.html(f'<strong>{remark}<strong>')
    
    st.write("""
    - If a congressperson does not follow party lines, they might get sanctioned.
    - However, they can author a bill with people from any other party.
    - Then, the idea is to see if the different positions can be diferentiated in the topics of the bills.
    
    """)
    st.image("./Images/party_positions.png", "The government coalition have most of their support in smaller parties. The independents are key to have majorities.")


def slide_context_2():
    st.title("Context: The Authors of the Bills")
    st.write("""
    There is no limit in the number of authors or sponsors that a bill can have. Also, they can be from any combination of parties.
    """)
    remark = """
    This makes it hard to define a single position of a bill. However, if the Opposition Statute has had an effect on the parties we would expect to see clear differences in the topics pursued by congresspeople since they will be more attached to party lines. Therefore, the topics should be aligned with the positions of the majority of sponsors.
    """

    st.html(f'<strong>{remark}<strong>')
    
    st.image("./Images/bills_authors.png", "30% of the bills have only one author. There are some bills that have an enormous number of sponsors, more than 100!")
    

def slide_context_3():
    st.title("Context: The Position metric")
    st.write("""
    A bill can have one or multiple authors. To measure the position of each one, each party position was assigned a number:
    - -1 for the oposition parties
    - 0 for the independents
    - 1 for the government coalition
    """)
    remark = "Then, an average of the party position of each author was taken as the metric of the bill position."
    st.html(f'<strong>{remark}<strong>')
    st.image("./Images/bills_positions.png", "Bills closer to -1 have more opposition authors, 1 the government coalition and 0 more independents or equal amounts of opposition and pro-government.")

def slide_game_intro():
    st.title("Let's play a game")
    st.write("""
    You are going to guess the position that a topic has based on a couple of tweets from the president.
    The idea is to see how similar your classification is compared to the actual average position of the topic.
    """)

def slide_cards():
    # Mock tweet
    tweet = """
    "Just attended an incredible AI conference! The future of machine learning looks so promising. 
    Can't wait to see how these innovations will transform  industries. #AI #Technology #Innovation"
    """
    
    st.write("### Example Tweet")
    st.markdown(f'> {tweet}')
    
    # Tweet analysis metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Sentiment", "Positive")
    
    with col2:
        st.metric("Topic", "Technology")
    
    with col3:
        st.metric("Engagement", "5.2k likes")

def slide_tweets():
    st.title("Just to give you a flavor...")
    st.write("This two tweets show some of the main concerns of the government.")

    col1, col2 = st.columns(2)
        
    with col1:
        st.image("./Images/petro_tweet_1.png", "December 21, 2022")
        
    with col2:
        st.image("./Images/petro_tweet_2.png", "August 7, 2024")

    

def slide_interactive_questions():
    st.title("Interactive Topic Classification")
    st.write("""
    #### Topic 1:
    """)

    topic = """
    ### education health development protection social educational half access 
    right training guarantee life age system prevention violence comprehensive object frame service
    """
    st.markdown(f'> {topic}')
    
    # Sample questions about the tweet
    questions = {
        "topic1_position": "What is the position that you percieve in this topic?",
        "topic1_saliency": "How many bills do you feel this topic covers?",
    }
    
    for key, question in questions.items():
        st.write(f"### {question}")
        
        if key == "topic1_position":
            response = st.select_slider(
                "Rate the position of the topic",
                options=['-1 Opposition', '-0.5 Somewhat opposition', '0 Independent', '0.5 Somewhat pro-goverment', '1 Pro-government'],
                value='0 Independent'
            )
        else:
            response = st.slider(
                "Rate the saliency (percentage of the total number of bills) related to this topic", 
                min_value=0, 
                max_value=100, 
                value=50,
                format='%d%%'
            )
        
        st.session_state.responses[key] = response

def slide_results():
    st.title("Audience Insights")
    
    if st.session_state.responses:
        # Create visualizations for responses
        sentiment_data = {
            'Category': ['Very Negative', 'Negative', 'Neutral', 'Positive', 'Very Positive'],
            'Count': [
                list(st.session_state.responses.values()).count('Very Negative'),
                list(st.session_state.responses.values()).count('Negative'),
                list(st.session_state.responses.values()).count('Neutral'),
                list(st.session_state.responses.values()).count('Positive'),
                list(st.session_state.responses.values()).count('Very Positive')
            ]
        }
        
        df = pd.DataFrame(sentiment_data)
        
        fig = px.bar(
            df, 
            x='Category', 
            y='Count', 
            title='Sentiment Distribution'
        )
        
        st.plotly_chart(fig)
        
        # Show raw responses
        st.write("### Your Responses")
        for key, value in st.session_state.responses.items():
            st.write(f"{key.replace('_', ' ').title()}: {value}")
    else:
        st.write("No responses collected yet.")

if __name__ == "__main__":
    main()