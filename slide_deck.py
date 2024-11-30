import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objs as go
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
        slide_network,
        slide_results,
        slide_explore_topics
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
                
        elif st.session_state.slide == len(slides) - 1:
            if st.button("  Restart  "):
                st.session_state.slide = 0
    
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
    st.write("Classify this three topics by how likely they are going to be attached to the government.")

    topic_1 = """Topic 1:
    higher education | constitutional court | cultural heritage | social protection | animal welfare | social security | health protection | medium term | public health | public service | mental health | public credit | credit finance | animal abuse | medium tax | service provision | animal protection | tourism industry | commerce industry | constitutional ruling
    """
    topic_2 = """Topic 2:
    constitutional court | development environment | rural development | armed conflict | popular election | final agreement | constitutional ruling | cauca valley | climate change | agricultural development | justice administration | international law | administrative litigation | peace construction | public administration | special protection | email | criminal process | criminal coder | peace agreement
    """

    topic_3 = """Topic 3:
    public force | professional experience | mixed economy | industry superintendence | industry commerce | regulatory decree | public order | citizen coexistence | coexistence security | special administrative | administrative unit | executive branch | public administration | Colombian territory | scientific technician | unique exclusively | head government | service provision | public transport | public order
    """

    position_question = "What is the position that you percieve in this topic?"
    saliency_question ="How many bills do you feel this topic covers?"
    
    # Sample questions about the tweet
    questions = {
        "topic1": topic_1,
        "topic1_position": position_question,
        "topic1_saliency": saliency_question,
        "topic2": topic_2,
        "topic2_position": position_question,
        "topic2_saliency": saliency_question,
        "topic3": topic_3,
        "topic3_position": position_question,
        "topic3_saliency": saliency_question,
    }
    
    for key, question in questions.items():
        
        if "position" in key:
            response = st.select_slider(
                "Rate the position of the topic",
                options=['-1 Opposition', '-0.5 Somewhat opposition', '0 Independent', '0.5 Somewhat pro-goverment', '1 Pro-government'],
                value='0 Independent',
                key=key
            )
        elif "saliency" in key:
            response = st.slider(
                "Rate the saliency (percentage of the total number of bills) related to this topic", 
                min_value=0, 
                max_value=100, 
                value=50,
                format='%d%%',
                key=key
            )
        else:
            st.write(f"##### {question}")
            response = ""
        
        st.session_state.responses[key] = response


def slide_network():
    st.title("Before your results: who sponsors with whom?")
    st.write("""
    The network has each party as a node and the edges are the connections due to authorships.
    The thicker the edge, the more bills member of those parties presented together. The bigger parties are the ones with more connections (degree).
    - The government party (Pacto Histórico) sponsors mostly with other members of the coalition.
    - The main independent parties (Partido de la U, Liberal and Conservador) have strong ties with both pro-government and opposition.
    - The connections of the opposition (Centro Democrático and Cambio Radical) are less than the ones from the other groups, but tighter with independents.
    """)
    st.image("./Images/parties_authors.gif", "The independent parties have strong ties with both ends of the spectrum.")

def slide_results():
    # Loading the results
    topic_positions = pd.read_csv('bills_topic_positions.csv')
    topic_saliency = {'topic1_saliency':63.1,
                        'topic2_saliency':32.2,
                        'topic3_saliency':4.7}
    
    st.title("How well did you do?")
    st.write("Explore the topics in the next slide")
    
    if st.session_state.responses:
        # Convert position responses to numerical values
        position_mapping = {
            '-1 Opposition': -1,
            '-0.5 Somewhat opposition': -0.5,
            '0 Independent': 0,
            '0.5 Somewhat pro-goverment': 0.5,
            '1 Pro-government': 1
        }
        
        # Prepare data for visualization
        user_position_data = {
            'Topic 1': [],
            'Topic 2': [],
            'Topic 3': []
        }
        
        # Collect user responses
        for topic in ['topic1', 'topic2', 'topic3']:
            topic_upd = topic.replace('t', 'T').replace('c', 'c ')
            position_key = f'{topic}_position'
            if position_key in st.session_state.responses:
                response = st.session_state.responses[position_key]
                if response in position_mapping:
                    user_position_data[topic_upd].append(position_mapping[response])
        
        # Prepare true positions data
        true_positions = {
            'Topic 1': topic_positions['topic_1_positions'].values,
            'Topic 2': topic_positions['topic_2_positions'].values,
            'Topic 3': topic_positions['topic_3_positions'].values
        }
        
        # Create box plot
        fig = go.Figure()
        
        # Colors for user and true positions
        user_color = '#FF6B6B'
        true_color = '#45B7D1'
        
        # Add boxplots for each topic
        topics = ['Topic 1', 'Topic 2', 'Topic 3']
        for i, topic in enumerate(topics):
            # User responses boxplot
            fig.add_trace(go.Box(
                y=user_position_data[topic], 
                x=[f'{topic} (Users)' for _ in user_position_data[topic]],
                boxmean=True,
                marker_color=user_color,
                name=f'{topic} (Users)',
                offsetgroup=2*i,
                showlegend=False
            ))
            
            # True positions boxplot
            fig.add_trace(go.Box(
                y=true_positions[topic], 
                x=[f'{topic} (True)' for _ in true_positions[topic]],
                boxmean=True,
                marker_color=true_color,
                name=f'{topic} (True)',
                offsetgroup=2*i+1,
                showlegend=False
            ))
        
        fig.update_layout(
            title='Distribution of the Topic Position Responses',
            yaxis_title='Position\n(-1: Opposition, 1: Pro-government)',
            boxmode='group',
            showlegend=False
        )
        
        st.plotly_chart(fig)
        
        # Show raw responses
        col1, col2 = st.columns(2)
        with col1:
            st.write("### Your Responses")
            for key, value in st.session_state.responses.items():
                if 'saliency' in key:
                    st.metric("Saliency", str(value) + "%", round(topic_saliency[key]-value, 1))
                    st.divider()
                elif 'position' in key:
                    tp = round(float(np.mean(true_positions[key.replace('c', 'c ').replace('_position', '').title()])), 1)
                    st.metric("Position", value.split()[0], round(tp-float(value.split()[0]), 1))
                else:
                    st.write(f"#### {key.replace('_', ' ').title()}:")
        with col2:
            st.write("### True data")
            for key, value in st.session_state.responses.items():
                if 'saliency' in key:
                    st.metric("Saliency", str(topic_saliency[key])+"%", round(value - topic_saliency[key], 1))
                    st.divider()
                elif 'position' in key:
                    tp = round(float(np.mean(true_positions[key.replace('c', 'c ').replace('_position', '').title()])), 3)
                    st.metric("Avg. Position", tp, round(float(value.split()[0])-tp, 1))
                else:
                    st.write(f"#### {key.replace('_', ' ').title()}:")
 
    else:
        st.write("No responses collected yet.")

def slide_explore_topics():
    st.title("Interact with the topics")
    with open('LDAvis.html','r') as f: 
        html_data = f.read()
    components.html(html_data, scrolling=True, height=1000)



if __name__ == "__main__":
    main()