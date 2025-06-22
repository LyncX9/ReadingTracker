import streamlit as st
import sqlite3
import pandas as pd
from typing import Optional
import hashlib

DB_FILE = "reading_tracker.db"
conn = sqlite3.connect(DB_FILE, check_same_thread=False)
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL
)''')

c.execute('''
CREATE TABLE IF NOT EXISTS readings (
    username TEXT,
    title TEXT,
    type TEXT,
    total_parts INTEGER,
    current_part INTEGER,
    PRIMARY KEY (username, title)
)''')
conn.commit()

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_user(username: str, password: str) -> bool:
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    return row and row[0] == hash_password(password)

def create_user(username: str, password: str) -> bool:
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def load_readings(username: str):
    c.execute("SELECT title, type, total_parts, current_part FROM readings WHERE username = ?", (username,))
    rows = c.fetchall()
    return [ReadingEntry(title=row[0], type=row[1], total_parts=row[2], current_part=row[3]) for row in rows]

def save_reading(username: str, entry):
    c.execute("""
    INSERT INTO readings (username, title, type, total_parts, current_part)
    VALUES (?, ?, ?, ?, ?)
    ON CONFLICT(username, title) DO UPDATE SET
        type=excluded.type,
        total_parts=excluded.total_parts,
        current_part=excluded.current_part
    """, (username, entry.title, entry.type, entry.total_parts, entry.current_part))
    conn.commit()

class ReadingEntry:
    def __init__(self, title: str, type: str, total_parts: Optional[int] = None, current_part: int = 0):
        self.title = title
        self.type = type
        self.total_parts = total_parts
        self.current_part = current_part

    def get_status(self):
        if self.total_parts is None:
            return f"{self.current_part} (Ongoing)"
        return f"{self.current_part}/{self.total_parts}"

st.set_page_config(page_title="Reading Tracker", layout="wide")
st.markdown("""
    <style>
        .main {
            background-color: #121212;
            color: #FFFFFF;
        }
        .block-container {
            padding: 2rem;
        }
        .stButton > button {
            background-color: #333333;
            color: white;
            border-radius: 0.5rem;
        }
        .stTextInput input, .stSelectbox div {
            background-color: #1e1e1e;
            color: white;
        }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("📚 Reading Tracker")
st.sidebar.caption("Track your readings smartly")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

if not st.session_state.logged_in:
    st.sidebar.subheader("🔐 Login or Register")
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    auth_action = st.sidebar.radio("Action", ["Login", "Register"])

    if st.sidebar.button("Submit"):
        if auth_action == "Login":
            if verify_user(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Logged in successfully!")
            else:
                st.error("Incorrect username or password.")
        else:
            if create_user(username, password):
                st.success("Account created. Please log in.")
            else:
                st.error("Username already exists.")
    st.stop()

page = st.sidebar.selectbox("Navigate", ["Add New Reading", "View & Update", "Export to CSV"])
reading_list = load_readings(st.session_state.username)

if page == "Add New Reading":
    st.header("➕ Add New Reading")
    with st.form("add_form"):
        title = st.text_input("Title")
        type_ = st.selectbox("Type", ["comic", "manhwa", "manhua", "book"])
        total_input = st.text_input("Total parts (leave blank if ongoing)")
        submitted = st.form_submit_button("Add")
        if submitted and title:
            total_parts = int(total_input) if total_input.strip() else None
            entry = ReadingEntry(title=title, type=type_, total_parts=total_parts)
            save_reading(st.session_state.username, entry)
            st.success("Added successfully!")
            st.experimental_rerun()

elif page == "View & Update":
    st.header("📂 View, Filter & Update Progress")
    filter_type = st.selectbox("Filter by type", ["All", "comic", "manhwa", "manhua", "book"])
    sort_by = st.selectbox("Sort by", ["Title", "Type", "Progress"])

    filtered_list = reading_list
    if filter_type != "All":
        filtered_list = [r for r in filtered_list if r.type == filter_type]

    if sort_by == "Title":
        filtered_list.sort(key=lambda x: x.title.lower())
    elif sort_by == "Type":
        filtered_list.sort(key=lambda x: x.type.lower())
    else:
        filtered_list.sort(key=lambda x: (x.current_part / (x.total_parts or 1)), reverse=True)

    if filtered_list:
        selected = st.selectbox("Select to update:", filtered_list, format_func=lambda r: f"{r.title} ({r.type})")
        new_progress = st.number_input("New progress", value=selected.current_part, min_value=0)
        if st.button("Update"):
            selected.current_part = new_progress
            save_reading(st.session_state.username, selected)
            st.success("Updated.")
            st.experimental_rerun()

    st.subheader("📋 Reading List")
    if filtered_list:
        for entry in filtered_list:
            st.markdown(f"**{entry.title}** [{entry.type}] — `{entry.get_status()}`")
    else:
        st.warning("No data to display.")

elif page == "Export to CSV":
    st.header("📤 Export Reading List")
    if reading_list:
        df = pd.DataFrame([vars(e) for e in reading_list])
        st.download_button(
            label="Download as CSV",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name="reading_list.csv",
            mime="text/csv"
        )
    else:
        st.warning("Your list is empty. Nothing to export.")