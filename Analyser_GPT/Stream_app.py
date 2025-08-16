import streamlit as st
import asyncio
import os

from teams.analyzer_gpt import getDataAnalyzerTeam
from models.openai_model_client import get_model_client
from config.docker_util import getDockerCommandLineExecutor,start_docker_container,stop_docker_container
from autogen_agentchat.messages import TextMessage

from autogen_agentchat.base import TaskResult #---> used in message.content to print output properly
st.title("Analyser GPT-Digital Data Analyst")

uploaded_file=st.file_uploader("Upload a CSV File",type=["csv"])
task=st.chat_input("Enter your task here...")

# making two boxes here one for streamlit convo load and one for team convo load
if 'messages' not in st.session_state:
    st.session_state.messages=[]
if 'autogen_team_state' not in st.session_state:
    st.session_state.autogen_team_state=None
if('images_shown') in st.session_state:
    st.session_state.images_shown=[]

async def run_analyser_gpt(docker,openai_model,task):
    try:
        await start_docker_container(docker)
        team=getDataAnalyzerTeam(docker,openai_model)

        if st.session_state.autogen_team_state is not None:
            await team.load_state(st.session_state.autogen_team_state) #--->now team will have context

        async for message in team.run_stream(task=task):
            # print(message)
            if isinstance(message,TextMessage):
                if message.source.startswith('user'):
                    with st.chat_message('user',avatar='👤'):
                        st.markdown(message.content)
                if message.source.startswith('Data_Analyzer_Agent'):
                    with st.chat_message('Data Analyzer',avatar='🕵🏼‍♀️'):
                        st.markdown(message.content)
                if message.source.startswith('Python_Code_Executor_Agent'):
                    with st.chat_message('Code Executor',avatar='👨‍💻'):
                        st.markdown(message.content)
                st.session_state.messages.append(message.content)
            # To show output in streamlit we need to:
                # st.markdown(f"**{message.content}")
            elif isinstance(message,TaskResult):
                st.markdown(f"Stop Reason:{message.stop_reason}")
                st.session_state.messages.append(message.stop_reason)

        st.session_state.autogen_team_state=await team.save_state() #-->saving the convo each time to load for next convo 
        return None
    except Exception as e:
        st.error(f"Error: {e}")
        return e
    finally:
        await stop_docker_container(docker)

# Solving the issue of loading prev convo
if st.session_state.messages:
    for msg in st.session_state.messages:
        st.markdown(msg)

if task:
    if uploaded_file is not None:
        
        if not os.path.exists('temp',):
            os.makedirs('temp',exist_ok=True)
        with open('temp/data.csv','wb') as f:
            f.write(uploaded_file.getbuffer())
        
        openai_model_client=get_model_client()
        docker=getDockerCommandLineExecutor()

        error=asyncio.run(run_analyser_gpt(docker,openai_model_client,task))

        if error:
            st.error(f"An error occured: {error}")

        if os.path.exists('/temp/output.png'):
            # if('output.png' not in st.session_state.images_shown):
            #     st.session_state.images_shown.append('output.png')

            st.image('/temp/output.png',caption='Output Image')

    else:
        st.warning("Please upload the file and provide the task.")
else:
    st.warning("Please provide the task")