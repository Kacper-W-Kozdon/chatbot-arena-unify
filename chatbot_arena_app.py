import streamlit as st
import numpy as np
import pandas as pd
import os
from unify import Unify

api_key = "TAw34N+waKrjQ053e+3vSsdjNJVC+MyHs5CF3NdBufQ="



def form_callback():
    global unify_model1, unify_model2
    st.session_state['model1_selectbox'] = ''
    st.session_state['model2_selectbox'] = ''
    unify_model1 = Unify(
        api_key=api_key,
        endpoint=st.session_state.model1_selectbox,
        )

    unify_model2 = Unify(
        api_key=api_key,
        endpoint=st.session_state.model2_selectbox,
        )   
    user_prompt = st.text_input('User prompt', '')
    st.session_state['user_prompt'] = user_prompt

def prompt_callback():
    global response1, response2 
    response1 = unify_model1.generate(user_prompt=st.session_state['user_prompt'])
    response2 = unify_model2.generate(user_prompt=st.session_state['user_prompt'])

col1, col2 = st.columns(2)

with st.form(key='my_form'):
    with col1:
        model1_selectbox = st.selectbox('Select the first LLM model:',
                                        ('mixtral-8x7b-instruct-v0.1@fireworks-ai',
                                         'llama-2-13b-chat@fireworks-ai',
                                         'llama-2-7b-chat@fireworks-ai',
                                         'gemma-7b-it@fireworks-ai',
                                         'mixtral-8x22b-instruct-v0.1@fireworks-ai',
                                         'codellama-7b-instruct@together-ai',
                                         'llama-3-8b-chat@fireworks-ai',
                                         'gpt-4@openai',
                                         'gpt-3.5-turbo@openai',
                                         'llama-2-70b-chat@fireworks-ai',
                                         'llama-2-13b-chat@fireworks-ai',
                                         'gpt-4-turbo@openai'),
                                        key="model1_selectbox")
    with col2:
        model2_selectbox = st.selectbox('Select the second LLM model:',
                                        ('mixtral-8x7b-instruct-v0.1@fireworks-ai',
                                         'llama-2-13b-chat@fireworks-ai',
                                         'llama-2-7b-chat@fireworks-ai',
                                         'gemma-7b-it@fireworks-ai',
                                         'mixtral-8x22b-instruct-v0.1@fireworks-ai',
                                         'codellama-7b-instruct@together-ai',
                                         'llama-3-8b-chat@fireworks-ai',
                                         'gpt-4@openai',
                                         'gpt-3.5-turbo@openai',
                                         'llama-2-70b-chat@fireworks-ai',
                                         'llama-2-13b-chat@fireworks-ai',
                                         'gpt-4-turbo@openai'),
                                        key="model2_slectbox")
    submit_button = st.form_submit_button(label='Submit', on_click=form_callback)
