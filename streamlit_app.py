import os
import json
import streamlit as st

# STEP 1: make file paths
FILE_PATH = 'session_data.json'  # Stores single text input data
APPENDED_PATH = 'session_data1.json'  # Stores appended data (list of entries)
NUMBER_PATH = 'session_number.json'
PAYCHECK1_INCOME = 'paycheck1_income.json'
PAYCHECK2_INCOME = 'paycheck2_income.json'

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

# STEP 4-A: make a function that loads single entry for number
def load_number():
    if os.path.exists(NUMBER_PATH):
        with open(NUMBER_PATH, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}  # Return default number if corrupted
    return {}  # Default value

# STEP 4-B: make a function that saves the number entry
def save_number():
    with open(NUMBER_PATH, "w") as f:
        json.dump({'number_key': st.session_state.number_key}, f)

# LOAD Paycheck 1 INCOME
def load_paycheck1():
    if os.path.exists(PAYCHECK1_INCOME):
        with open(PAYCHECK1_INCOME, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return{}
    return {}

# SAVE Paycheck 1 INCOME
def save_paycheck1():
    with open(PAYCHECK1_INCOME, 'w') as f:
        json.dump({'paycheck1_key': st.session_state.paycheck1_key}, f)

# LOAD Paycheck 2 INCOME
def load_paycheck2():
    if os.path.exists(PAYCHECK2_INCOME):
        with open(PAYCHECK2_INCOME, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return{}
    return {}

# SAVE Paycheck 2 INCOME
def save_paycheck2():
    with open(PAYCHECK2_INCOME, 'w') as f:
        json.dump({'paycheck2_key': st.session_state.paycheck2_key}, f)


# STEP 5-A: Load single entry session data; initializes `input_data_key`
session_data = load_single_entry()
st.session_state.setdefault('input_data_key', session_data.get('input_data_key', ''))

# STEP 5-B: Load appended session data; initializes `appending_key`
session_data1 = load_appended_data()
st.session_state.setdefault('appending_key', '')

# STEP 6: Collect single value on UI
st.text_input('Enter information, if you dare:', key='input_data_key', on_change=save_single_entry)  # note the key, on_change arguments
st.write("Stored Value:", st.session_state.input_data_key)

# STEP 7: Collect appending values on UI
st.text_input('Append new entry:', key='appending_key', on_change=save_appended_data)

# STEP 8: allow individual deletions
st.write("Stored List:")
for idx, item in enumerate(session_data1):
    col1, col2 = st.columns([4, 1])
    col1.write(item)
    if col2.button(':x:', key=f'delete_{idx}'):
        session_data1.pop(idx)
        with open(APPENDED_PATH, "w") as f:
            json.dump(session_data1, f, indent=4)
        st.rerun()

# NUMBER TOWN
session_number = load_number()  # Load the number data (from NUMBER_PATH)
st.session_state.setdefault('number_key', session_number.get('number_key', 0.0))  # Initialize number_key correctly from NUMBER_PATH

# Use the correct key for number input (do not overwrite)
st.number_input(
    label='Number: ',
    value=0,
    key='number_key',  # Key for the number input field, ensuring no overwrite happens
    on_change=save_number  # Save the number value when changed
)

# Display the stored number from session_state
st.write('Stored Number: ', st.session_state.number_key)

# SIDEBAR
session_pc1 = load_paycheck1() # IMPORTANT STEP
st.session_state.setdefault('paycheck1_key', session_pc1.get('paycheck1_key', 0.0))

session_pc2 = load_paycheck2() # IMPORTANT STEP
st.session_state.setdefault('paycheck2_key', session_pc2.get('paycheck2_key', 0.0))

st.sidebar.number_input(
    "Set Paycheck 1 Income",
    min_value=0.0,
    value=0.0,  # Ensure it's float
    step=100.0,
    key='paycheck1_key',
    on_change=save_paycheck1
)


st.sidebar.number_input(
    "Set Paycheck 2 Income",
    min_value=0.0,
    value=0.0,  # Ensure it's float
    step=100.0,
    key='paycheck2_key',
    on_change=save_paycheck2
)

st.write('Stored Paycheck 1: ', st.session_state.paycheck1_key)
st.write('Stored Paycheck 2: ', st.session_state.paycheck2_key)