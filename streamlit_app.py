import os
import json
import streamlit as st

# STEP 1: make file paths
FILE_PATH = 'session_data.json'  # Stores single text input data
APPENDED_PATH = 'session_data1.json'  # Stores appended data (list of entries)

# STEP 2-A: make a function that loads single entry
def load_single_entry():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}  # Return empty dictionary if corrupted
    return {}

# STEP 2-B: make a function that saves the single entry
def save_single_entry():
    with open(FILE_PATH, "w") as f:
        json.dump({'input_data_key': st.session_state.input_data_key}, f)

# STEP 3-A: make a function that loads single entry (list)
def load_appended_data():
    if os.path.exists(APPENDED_PATH):
        with open(APPENDED_PATH, "r") as f:
            try:
                data = json.load(f)
                return data if isinstance(data, list) else []
            except json.JSONDecodeError:
                return []  # If file is empty or corrupted, return empty list
    return []

# STEP 3-B: Function to save and append new session data
def save_appended_data():
    data = load_appended_data()
    new_entry = st.session_state.appending_key
    if new_entry and new_entry not in data:  # Avoid duplicates
        data.append(new_entry)
        with open(APPENDED_PATH, "w") as f:
            json.dump(data, f, indent=4)

# STEP 4: Load single entry session data; initializes `input_data_key`
session_data = load_single_entry()
st.session_state.setdefault('input_data_key', session_data.get('input_data_key', ''))

# STEP 5: Load appended session data; initializes `appending_key`
session_data1 = load_appended_data()
st.session_state.setdefault('appending_key', '')

# USER INTERFACE
st.title("🎈 My new app")
st.write("Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/).")

# STEP 6: Collect single value on UI
st.text_input('Enter information, if you dare:', key='input_data_key', on_change=save_single_entry) # note the key, on_change arguments
    # output
st.write("Stored Value:", st.session_state.input_data_key)

# STEP 7: Collect appending values on UI
st.text_input('Append new entry:', key='appending_key', on_change=save_appended_data)

# STEP 8: allow individual
st.write("Stored List:")
for idx, item in enumerate(session_data1):
    col1, col2 = st.columns([4, 1])
    col1.write(item)
    if col2.button(':x:', key=f'delete_{idx}'):
        session_data1.pop(idx)
        with open(APPENDED_PATH, "w") as f:
            json.dump(session_data1, f, indent=4)
        st.rerun()
