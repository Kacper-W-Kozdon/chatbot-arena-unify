import streamlit as st
import numpy as np
import pandas as pd
import os
import time
from unify import Unify

# api_key = "TAw34N+waKrjQ053e+3vSsdjNJVC+MyHs5CF3NdBufQ="

unify_model1 = None
unify_model2 = None
response1 = None
response2 = None
models_not_selected = True

keys = ["model1_selectbox", "model2_selectbox", "response1", "response2", "user_prompt", "models_not_selected", "response_allowed", "api_key"]

for key in keys:
    if key not in st.session_state.keys():
        st.session_state[key] = None

st.session_state.models_not_selected = models_not_selected if \
    st.session_state.models_not_selected is None \
    else st.session_state.models_not_selected

col1, col2 = st.columns(2)

def form_callback(api_key=st.session_state.api_key):
    global unify_model1, unify_model2

    st.write(st.session_state.model1_selectbox, st.session_state.model2_selectbox)

    unify_model1 = Unify(
        api_key=api_key,
        endpoint=st.session_state.model1_selectbox,
        )

    unify_model2 = Unify(
        api_key=api_key,
        endpoint=st.session_state.model2_selectbox,
        )
    st.session_state.models_not_selected = False

def prompt_callback():
    global response1, response2
    col1, col2 = st.columns(2)
    st.write(st.session_state['user_prompt'])
    # response1 = unify_model1.generate(user_prompt=st.session_state['user_prompt'])
    # response2 = unify_model2.generate(user_prompt=st.session_state['user_prompt'])
    response1 = "response1"
    response2 = "response2"

    with col1:
        st.text_area(f'{response1}', key="response1_out")

    with col2:
        st.text_area(f'{response2}', key="response2_out")

with st.sidebar:
    st.session_state.api_key = st.text_input("Unify API key", type="password")

@st.experimental_fragment
def set_models(api_key=st.session_state.api_key):
    disabled = not bool(api_key)
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
                                            placeholder='mixtral-8x7b-instruct-v0.1@fireworks-ai',
                                            disabled=disabled,
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
                                            placeholder='mixtral-8x7b-instruct-v0.1@fireworks-ai',
                                            disabled=disabled,
                                            key="model2_selectbox")
        submit_button = st.form_submit_button(label='Initialize', disabled=disabled,
                                            on_click=lambda: form_callback(st.session_state.api_key))
        if not disabled:
            st.rerun()

@st.experimental_fragment
def get_user_prompt(disabled=st.session_state.models_not_selected):
    st.session_state['user_prompt'] = st.text_input('User prompt', '',
                                                    disabled=disabled,
                                                    on_change=lambda: st.session_state.__setattr__("response_allowed", True))
    if disabled:
        time.sleep(1)
        st.rerun()
    if st.session_state.response_allowed:
        get_response()

@st.experimental_fragment
def get_response():
    st.write(st.session_state.user_prompt)


set_models(st.session_state.api_key)
get_user_prompt(st.session_state.models_not_selected)
