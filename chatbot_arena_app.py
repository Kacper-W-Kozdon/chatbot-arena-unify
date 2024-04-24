import streamlit as st
import numpy as np
import pandas as pd
import os
import time
from unify import Unify

# api_key = "TAw34N+waKrjQ053e+3vSsdjNJVC+MyHs5CF3NdBufQ="

models_not_selected = True

keys = ["model1_selectbox", "model2_selectbox", "response1",
        "response2", "user_prompt", "models_not_selected",
        "response_allowed", "api_key",
        "unify_model1", "unify_model2"]

for key in keys:
    if key not in st.session_state.keys():
        st.session_state[key] = None

st.session_state.models_not_selected = models_not_selected if \
    st.session_state.models_not_selected is None \
    else st.session_state.models_not_selected

col1, col2 = st.columns(2)

def form_callback(api_key=st.session_state.api_key):
    st.session_state.unify_model1 = Unify(
        api_key=api_key,
        endpoint=st.session_state.model1_selectbox,
        )

    st.session_state.unify_model2 = Unify(
        api_key=api_key,
        endpoint=st.session_state.model2_selectbox,
        )
    st.session_state.models_not_selected = False

def prompt_callback(response_allowed=st.session_state.response_allowed):
    global response1, response2
    unify_model1 = st.session_state.unify_model1
    unify_model2 = st.session_state.unify_model2
    col1, col2 = st.columns(2)
    response1 = '' if not response_allowed else unify_model1.generate(user_prompt=st.session_state['user_prompt'])
    response2 = '' if not response_allowed else unify_model2.generate(user_prompt=st.session_state['user_prompt'])
    model1 = st.session_state.model1_selectbox
    model2 = st.session_state.model2_selectbox

    with col1:
        st.text_area(f'{model1}', f'{response1}', disabled=True, key="response1_out")

    with col2:
        st.text_area(f'{model2}', f'{response2}', disabled=True, key="response2_out")

with st.sidebar:
    st.session_state.api_key = st.text_input("Unify API key", type="password")

def set_models(api_key=st.session_state.api_key):
    disabled = not bool(api_key)
    with st.form(key='my_form'):
        with col1:
            st.selectbox('Select the second LLM model:',
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
            st.selectbox('Select the second LLM model:',
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
        st.form_submit_button(label='Initialize', disabled=disabled,
                                            on_click=lambda: form_callback(api_key))

def get_user_prompt(disabled=st.session_state.models_not_selected):
    st.session_state.user_prompt = st.text_input('User prompt', '', placeholder="Hello, introduce yourself.",
                                                    disabled=disabled,
                                                    on_change=lambda: st.session_state.__setattr__("response_allowed", True))


set_models(st.session_state.api_key)
get_user_prompt(st.session_state.models_not_selected)
prompt_callback(st.session_state.response_allowed)
