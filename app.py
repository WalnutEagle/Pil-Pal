import streamlit as st
from PIL import Image
import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv()
st.set_page_config(page_title="Pill-Pal: Medication Identification Agent", layout="wide")
st.title("💊 Pill-Pal: Multi-Modal Medication Identification Agent")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
llm_vision = ChatGoogleGenerativeAI(model="gemini-pro-vision", temperature=0.1)

llm_agent = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)
search_tool = TavilySearchResults(max_results=2)
tools = [search_tool]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant that finds information about medications based on a description. Use the search tool to find accurate medical information."),
    ("placeholder", "{chat_history}"),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm_agent, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

col1, col2 = st.columns(2)

with col1:
    st.header("1. Upload a Pill Image")
    uploaded_file = st.file_uploader("Choose an image of the pill...", type=["jpg", "png", "jpeg"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Pill Image.', use_column_width=True)

        if st.button("Identify Pill from Image"):
            with st.spinner("Analyzing image... This may take a moment."):
                user_message = HumanMessage(
                    content=[
                        {
                            "type": "text",
                            "text": "Identify the pill in this image. Describe its appearance (color, shape, markings) in detail. Based on the markings, what is the likely medication name?",
                        },
                        {"type": "image_url", "image_url": image},
                    ]
                )
                
                response = llm_vision.invoke([user_message])
                pill_description = response.content
                
                st.session_state.pill_description = pill_description
                st.session_state.chat_history.append(HumanMessage(content="User uploaded an image."))
                st.session_state.chat_history.append(AIMessage(content=pill_description))

with col2:
    st.header("2. Chat with the Agent")

    for message in st.session_state.chat_history:
        if isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)
        else:
            with st.chat_message("AI"):
                st.markdown(message.content)

    if "pill_description" in st.session_state:
        user_question = st.chat_input("Ask about this medication (e.g., 'What is it used for?')")

        if user_question:
            st.session_state.chat_history.append(HumanMessage(content=user_question))
            with st.chat_message("Human"):
                st.markdown(user_question)

            with st.spinner("Finding information..."):
                agent_input = f"The user is asking about a medication described as: '{st.session_state.pill_description}'. The user's specific question is: '{user_question}'"
                
                response = agent_executor.invoke({
                    "input": agent_input,
                    "chat_history": st.session_state.chat_history
                })

                ai_response = response['output']
                st.session_state.chat_history.append(AIMessage(content=ai_response))
                with st.chat_message("AI"):
                    st.markdown(ai_response)
