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
             "Provide a reason for the rating and also suggest an action plan for the recruiter for self  improvement.\n\n" + \
             "\n".join([f"Feedback {i+1}: {fb}" for i, fb in enumerate(feedbacks)]) + "\n\n" \
             "Provide the response in the following format:\n\n\n\n" \
             "------------------------------------" \
             "Rating: [Very Good / Good / Neutral / Bad / Very Bad]\n\n" \
             "Reason:\n[Explanation for the rating]\n\n" \
             "Action Plan for self-improvement:\n[Steps for the recruiter to improve]"

    messages = [
        SystemMessage(content="You are a helpful HR Head."),
        HumanMessage(content=prompt)
    ]
    
    response = chat.invoke(messages)
    return response.content.strip()

# Streamlit UI
st.set_page_config(layout="wide")
#st.title("Reliance Jio - Recruiter Feedback Performance System")
#t.markdown("<h1 style='text-align: center;'> Reliance Jio - Recruiter Feedback Performance System</h1>", unsafe_allow_html=True)

st.markdown(
    """
    <div style="display: flex; align-items: center; justify-content: center;">
        <img src="https://e7.pngegg.com/pngimages/33/16/png-clipart-jio-logo-jio-reliance-digital-business-logo-mobile-phones-business-blue-text.png" width="100">
        <h1>Reliance Jio - Recruiter Feedback Performance System</h1>
    </div>
    """, 
    unsafe_allow_html=True
)


# Create layout with two columns
col1, col2 = st.columns([1, 2])

with col1:
    #st.header("Enter Candidate Feedback")
    #feedbacks = [st.text_area(f"Candidate Feedback {i+1}", "") for i in range(5)]
    feedbacks = [st.text_area(f"Candidate Feedback 1", "He answered all my queries"),
                 st.text_area(f"Candidate Feedback 2", "He was very helpful"),
                 st.text_area(f"Candidate Feedback 3", "Good experience"),
                 st.text_area(f"Candidate Feedback 4", "He explained all the process and gave my offer letter on time"),
                 st.text_area(f"Candidate Feedback 5", "He took time to release and not answered my queries"),
                 ]
    submit = st.button("Get Rating")

with col2:
    #st.header("Recruiter Feedback Report Card")
    if submit:
        if all(f.strip() for f in feedbacks):
            rating = get_feedback_rating(feedbacks)
            #st.subheader(f"LLM Rating: {rating}/10")
            var1, var2 = rating.split('</think>', 1) if '</think>' in rating else (rating, '')
            var1 = var1.replace('<think>', '').replace('</think>', '')
            st.write(var2)

            with st.expander("Thoughts of LLM"):
                st.write(var1)  # Display first part in collapsible box
        else:
            st.warning("Please provide feedback in all fields before submitting.")