import os
import shutil
import streamlit as st
from pathlib import Path
import matplotlib.pyplot as plt
from collections import Counter

# --- CONFIG ---
PASSWORD = "Ankit@8278"  # Change this to your desired password

# --- PAGE SETTINGS ---
st.set_page_config(page_title="Secure File Manager", layout="centered")
st.title("🔒 Secure File Management Dashboard")

# --- PASSWORD PROTECTION ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    entered_pw = st.text_input("Enter password", type="password")
    if st.button("Login"):
        if entered_pw == PASSWORD:
            st.session_state.authenticated = True
            st.success("Access granted.")
        else:
            st.error("Incorrect password. Try again.")
    st.stop()

# --- DIRECTORY SELECTION ---
directory = st.text_input("📂 Enter the directory path:")

if directory and os.path.exists(directory):

    st.markdown("### 📜 Files & Folders")
    search_query = st.text_input("🔍 Search")
    directory = r'C:\Users\ankit\Documents'
    files = os.listdir(directory)
    files = sorted(files)
    filtered_files = [f for f in files if search_query.lower() in f.lower()]

    file_types = []

    if not filtered_files:
        st.info("No matching files.")
    else:
        for f in filtered_files:
            full_path = os.path.join(directory, f)
            file_type = "📁 Folder" if os.path.isdir(full_path) else f"📄 File ({Path(f).suffix})"
            size = os.path.getsize(full_path) / 1024  # KB
            st.write(f"*{f}* — {file_type} — {size:.2f} KB")
            if os.path.isfile(full_path):
                with open(full_path, "rb") as file:
                    st.download_button("⬇️ Download", data=file, file_name=f)
                file_types.append(Path(f).suffix)

    # --- FILE TYPE CHART ---
    st.markdown("### 📊 File Type Distribution")
    if file_types:
        type_counts = Counter(file_types)
        fig, ax = plt.subplots()
        ax.pie(type_counts.values(), labels=type_counts.keys(), autopct='%1.1f%%')
        ax.axis('equal')
        st.pyplot(fig)
    else:
        st.info("No files to visualize.")

    st.markdown("---")

    # --- UPLOAD ---
    st.subheader("📤 Upload File")
    uploaded_file = st.file_uploader("Choose a file to upload")
    if uploaded_file:
        save_path = os.path.join(directory, uploaded_file.name)
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Uploaded '{uploaded_file.name}' successfully.")

    st.markdown("---")

    # --- RENAME ---
    st.subheader("✏️ Rename File/Folder")
    old_name = st.text_input("Old name")
    new_name = st.text_input("New name")
    if st.button("Rename"):
        try:
            os.rename(os.path.join(directory, old_name), os.path.join(directory, new_name))
            st.success("Renamed successfully.")
        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown("---")

    # --- DELETE ---
    st.subheader("🗑️ Delete File or Directory")
    delete_name = st.text_input("Name to delete")
    if st.button("Delete"):
        try:
            path = os.path.join(directory, delete_name)
            if os.path.isfile(path):
                os.remove(path)
                st.success("File deleted.")
            elif os.path.isdir(path):
                shutil.rmtree(path)
                st.success("Directory deleted.")
            else:
                st.warning("Not found.")
        except Exception as e:
            st.error(f"Error: {e}")

    st.markdown("---")

    # --- CREATE FOLDER ---
    st.subheader("📦 Create New Folder")
    folder_name = st.text_input("New folder name")
    if st.button("Create Directory"):
        try:
            os.makedirs(os.path.join(directory, folder_name), exist_ok=True)
            st.success("Folder created.")
        except Exception as e:
            st.error(f"Error: {e}")

else:
    if directory:
        st.error("Invalid directory path.")