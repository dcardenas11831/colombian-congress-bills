import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd

def main():
    st.set_page_config(page_title="Topic Modeling Insights", layout="wide")
    
    # Initialize session state for tracking slides and responses
    if 'slide' not in st.session_state:
        st.session_state.slide = 0
    if 'responses' not in st.session_state:
        st.session_state.responses = {}
    
    # Slide content
    slides = [
        slide_introduction,
        slide_project_overview,
        slide_sample_tweet,
        slide_interactive_questions,
        slide_results
    ]
    
    # Navigation buttons
    col1, col2 = st.columns([3, 1])
    
    with col2:
        if st.session_state.slide > 0:
            if st.button("Previous"):
                st.session_state.slide = max(0, st.session_state.slide - 1)
        
        if st.session_state.slide < len(slides) - 1:
            if st.button("Next"):
                st.session_state.slide = min(len(slides) - 1, st.session_state.slide + 1)
    
    # Render current slide
    slides[st.session_state.slide]()

def slide_introduction():
    st.title("Topic Modeling in Social Media")
    st.write("""
    ## Exploring Insights from Twitter Data
    
    This interactive presentation will walk you through:
    - The basics of topic modeling
    - A real-world tweet analysis
    - Interactive insights gathering
    """)
    st.image("bills_positions.png", caption="Topic Modeling Visualization")

def slide_project_overview():
    st.title("Project Overview")
    st.write("""
    ### Methodology
    
    #### Topic Modeling Approach
    - Used Latent Dirichlet Allocation (LDA)
    - Processed 10,000 tweets
    - Identified key thematic clusters
    
    #### Key Findings
    1. Identified 5 primary discussion topics
    2. Analyzed sentiment and engagement
    3. Extracted key insights from social media discourse
    """)
    
    # Create a sample topic distribution chart
    topics = ['Technology', 'Politics', 'Entertainment', 'Sports', 'Science']
    distribution = [0.25, 0.20, 0.18, 0.20, 0.17]
    
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(topics, distribution)
    ax.set_title('Topic Distribution')
    ax.set_ylabel('Proportion')
    ax.set_ylim(0, 0.3)
    
    st.pyplot(fig)

def slide_sample_tweet():
    st.title("Sample Tweet Analysis")
    
    # Mock tweet
    tweet = """
    "Just attended an incredible AI conference! The future of machine learning 
    looks so promising. Can't wait to see how these innovations will transform 
    industries. #AI #Technology #Innovation"
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

def slide_interactive_questions():
    st.title("Interactive Insights Gathering")
    
    # Sample questions about the tweet
    questions = {
        "sentiment": "What sentiment do you perceive in this tweet?",
        "topic_relevance": "How relevant is this tweet to the technology topic?",
        "engagement_potential": "How likely would you be to engage with this tweet?"
    }
    
    for key, question in questions.items():
        st.write(f"### {question}")
        
        if key == "sentiment":
            response = st.select_slider(
                "Rate the sentiment",
                options=['Very Negative', 'Negative', 'Neutral', 'Positive', 'Very Positive']
            )
        elif key == "topic_relevance":
            response = st.slider(
                "Rate topic relevance", 
                min_value=0, 
                max_value=10, 
                value=5
            )
        else:
            response = st.radio(
                "Engagement Likelihood",
                ['Not Likely', 'Somewhat Likely', 'Very Likely']
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