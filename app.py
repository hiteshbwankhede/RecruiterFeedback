import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain.schema import SystemMessage, HumanMessage
from dotenv import load_dotenv

load_dotenv()


# Load Groq API Key from environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    st.error("Groq API key not found. Please set the GROQ_API_KEY environment variable.")
    st.stop()

# Initialize LangChain ChatGroq model
chat = ChatGroq(model_name="deepseek-r1-distill-llama-70b", groq_api_key=GROQ_API_KEY, temperature=0)

# Function to get rating from Groq LLM
def get_feedback_rating(feedbacks):
    prompt = "You are HR Head. You will be provided with feedbacks given by candidates for the recruiter. " \
             "Analyze them and give a rating whose values can be Very Good, Good, Neutral, Bad, or Very Bad. " \
             "Provide a reason for the rating and also suggest an action plan for the recruiter to improve.\n\n" + \
             "\n".join([f"Feedback {i+1}: {fb}" for i, fb in enumerate(feedbacks)]) + "\n\n" \
             "Provide the response in the following format:\n\n\n\n" \
             "------------------------------------" \
             "Rating: [Very Good / Good / Neutral / Bad / Very Bad]\n\n" \
             "Reason:\n[Explanation for the rating]\n\n" \
             "Action Plan:\n[Steps for the recruiter to improve]"

    messages = [
        SystemMessage(content="You are a helpful HR Head."),
        HumanMessage(content=prompt)
    ]
    
    response = chat.invoke(messages)
    return response.content.strip()

# Streamlit UI
st.set_page_config(layout="wide")
st.title("Candidate Feedback Rating App")

# Create layout with two columns
col1, col2 = st.columns([1, 2])

with col1:
    #st.header("Enter Candidate Feedback")
    feedbacks = [st.text_area(f"Feedback {i+1}", "") for i in range(5)]
    submit = st.button("Get Rating")

with col2:
    st.header("LLM Rating Output")
    if submit:
        if all(f.strip() for f in feedbacks):
            rating = get_feedback_rating(feedbacks)
            #st.subheader(f"LLM Rating: {rating}/10")
            var1, var2 = rating.split('</think>', 1) if '</think>' in rating else (rating, '')

            st.write(var2)

            with st.expander("Thoughts of LLM"):
                st.write(var1)  # Display first part in collapsible box
        else:
            st.warning("Please provide feedback in all fields before submitting.")