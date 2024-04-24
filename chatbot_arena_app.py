import streamlit as st
import numpy as np
import pandas as pd
import os
import time
import json
from unify import Unify
from collections import OrderedDict

models_not_selected = True

keys = ["model1_selectbox", "model2_selectbox", "model1_other",
        "model2_other", "response1", "winner_picked",
        "response2", "user_prompt", "models_not_selected",
        "response_allowed", "api_key", "summary",
        "unify_model1", "unify_model2", "scores"]

for key in keys:
    if key not in st.session_state.keys():
        st.session_state[key] = None

st.session_state.scores = OrderedDict()

with open("scores.json", "r") as infile:
    if infile:
        st.session_state.scores = json.load(infile)


st.session_state.models_not_selected = models_not_selected if \
    st.session_state.models_not_selected is None \
    else st.session_state.models_not_selected

col1, col2 = st.columns(2)

def form_callback(api_key=st.session_state.api_key):
    endpoint1 = st.session_state.model1_selectbox if st.session_state.model1_selectbox != 'other' \
        else st.session_state.model1_other
    endpoint2 = st.session_state.model2_selectbox if st.session_state.model2_selectbox != 'other' \
        else st.session_state.model2_other

    st.session_state.unify_model1 = Unify(
        api_key=api_key,
        endpoint=endpoint1,
        )

    st.session_state.unify_model2 = Unify(
        api_key=api_key,
        endpoint=endpoint2,
        )
    st.session_state.models_not_selected = False

def prompt_callback(response_allowed=st.session_state.response_allowed):
    global response1, response2
    winner = None
    loser = None
    winner_picked = False if st.session_state.winner_picked is None else st.session_state.winner_picked
    unify_model1 = st.session_state.unify_model1 
    unify_model2 = st.session_state.unify_model2
    col1, col2 = st.columns(2)
    response1 = '' if not response_allowed else unify_model1.generate(user_prompt=st.session_state['user_prompt'])
    response2 = '' if not response_allowed else unify_model2.generate(user_prompt=st.session_state['user_prompt'])
    model1 = st.session_state.model1_selectbox if st.session_state.model1_selectbox != 'other' \
        else st.session_state.model1_other
    model2 = st.session_state.model2_selectbox if st.session_state.model2_selectbox != 'other' \
        else st.session_state.model2_other

    with col1:
        st.text_area(f'{model1}', f'{response1}', disabled=True, key="response1_out")
        if response_allowed:
            if st.button("Winner!", disabled=winner_picked,
                         on_click=lambda: (st.session_state.__setattr__("winner_picked", True)), key="winner1"):
                winner = model1
                loser = model2

    with col2:
        st.text_area(f'{model2}', f'{response2}', disabled=True, key="response2_out")
        if response_allowed:
            if st.button("Winner!", disabled=winner_picked,
                         on_click=lambda: (st.session_state.__setattr__("winner_picked", True)), key="winner2"):
                winner = model2
                loser = model1

    if st.session_state.winner_picked is True:
        update_winners(winner, loser)
        winner = None
        loser = None

with st.sidebar:
    st.session_state.api_key = st.text_input("Unify API key", type="password")

def set_models(api_key=st.session_state.api_key):
    disabled = not bool(api_key)
    model1_other_disabled = True
    model2_other_disabled = True
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
                          'gpt-4-turbo@openai',
                          'other'),
                         placeholder='mixtral-8x7b-instruct-v0.1@fireworks-ai',
                         disabled=disabled,
                         key="model1_selectbox")
            if st.session_state.model1_selectbox == 'other':
                model1_other_disabled = False
            st.text_input('Provide model:', placeholder='model@provider',
                          disabled=model1_other_disabled, key='model1_other')

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
                          'gpt-4-turbo@openai', 
                          'other'),
                         placeholder='llama-2-13b-chat@fireworks-ai',
                         disabled=disabled,
                         key="model2_selectbox")
            if st.session_state.model2_selectbox == 'other':
                model2_other_disabled = False
            st.text_input('Provide model:', placeholder='model@provider',
                          disabled=model2_other_disabled, key='model2_other')
        st.form_submit_button(label='Initialize', disabled=disabled,
                                            on_click=lambda: form_callback(api_key))

def get_user_prompt(disabled=st.session_state.models_not_selected):
    st.session_state.user_prompt = st.text_input('User prompt', placeholder="Hello there!",
                                                    disabled=disabled,
                                                    on_change=lambda: (st.session_state.__setattr__("response_allowed", True),
                                                                       st.session_state.__setattr__("winner_picked", False)))
    
    if st.session_state.user_prompt == '':
        st.session_state.response_allowed = False

def update_winners(winner=None, loser=None):
    if winner and loser:
        if winner not in st.session_state.scores.keys():
            st.session_state.scores[f'{winner}'] = {'wins': 0, 'losses': 0}    
        if loser not in st.session_state.scores.keys():
            st.session_state.scores[f'{loser}'] = {'wins': 0, 'losses': 0}

        st.session_state.scores[f'{winner}']['wins'] += 1
        if loser != winner:
            st.session_state.scores[f'{loser}']['losses'] += 1

        with open("scores.json", "w") as outfile:
            json.dump(st.session_state.scores, outfile)

def display_scores():
    scores_text = ''
    for key in st.session_state.scores.keys():
        scores_text += f'{key}: {st.session_state.scores[key]}'
        scores_text += '\n'
    st.text_area("Scores:", scores_text, disabled=True)

set_models(st.session_state.api_key)
get_user_prompt(st.session_state.models_not_selected)
prompt_callback(st.session_state.response_allowed)
display_scores()
