import streamlit as st
from langchain.agents import initialize_agent, Tool,AgentExecutor
from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv

load_dotenv()




# Initialize chat history
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# Initialize LangChain agent with Tavily web search tool
def initialize_langchain_agent():
    # Define the LLM (Language Model)
    llm = ChatGroq(temperature = .4)


    search_tool = TavilySearchResults(
    max_results=5,
    search_depth="advanced" )

    tools = [search_tool]

    # Initialize the agent with the tools
    agent = initialize_agent(tools, llm, agent_type="conversational-react-description")
    return agent




st.title("Chat Interface with LangChain and Tavily")

# Initialize the LangChain agent
agent = initialize_langchain_agent()

# Function to get agent response
def get_agent_response(user_message):
    return agent.invoke(user_message)['output']

# Display chat history
for chat in st.session_state['chat_history']:
    with st.chat_message(chat["role"]):
        st.write(chat["message"])

# Handle user input
user_input = st.chat_input("Enter message:")

if user_input:
    # Append user's message to chat history
    st.session_state['chat_history'].append({"role": "user", "message": user_input})
    
    # Generate and append agent's response
    agent_reply = get_agent_response(user_input)
    st.session_state['chat_history'].append({"role": "assistant", "message": agent_reply})
    
    # Display the updated chat history
    for chat in st.session_state['chat_history']:
        with st.chat_message(chat["role"]):
            st.write(chat["message"])




