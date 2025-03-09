import streamlit as st
import json
import os

# STEP 1: make a file path
FILE_PATH = 'session_data.json'

# STEP 2: make a function that loads session info
def load_session_data():
    if os.path.exists(FILE_PATH): # check
        with open(FILE_PATH, "r") as f: # "r" ensures we only read the file
            return json.load(f) # load session - like loading my Tony Hawk game
    return {} # idk, just go with it

# STEP 3: make a function that saves the data
def save_session_data(data):
    with open(FILE_PATH, "w") as f:
        json.dump(data, f)

# STEP 4: load the saved data; this also initializes the `input_data` key in the st.sessions_state (a dict-like object)
session_data = load_session_data()
st.session_state.input_data_key = session_data.get('input_data_key', '')

# STEP 5: begin making app
st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

# STEP 6: create the data
input_data_value = st.text_input('Enter information, if you dare:', st.session_state.input_data_key)

# STEP 7: store the data
if input_data_value != st.session_state.input_data_key:
    st.session_state.input_data_key = input_data_value
    save_session_data({'input_data_key': input_data_value})

# TEST
st.write(st.session_state.input_data_key)

# SUCCESS!
                                             
