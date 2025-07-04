# ReadingTracker

This application was inspired by a personal need to track daily reading progress, be it comics, manhwa, manhua, or books. Often readers forget where they last read—so this application is here as a simple yet functional solution to record, update, and manage their reading lists. With a clean interface and a dark theme that is easy on the eyes, this application also supports exporting data to CSV format so that progress can be backed up or published.

## ✨ Key Features

- 🔐 **Login and Register** users with SHA256 encryption
- ➕ Add new reading entries
- 📖 update reading progress
- 📊 Filter and sort entries by type and progress
- 📤 Export data to CSV
- 🌙 Custom dark theme with CSS

---

How to Use the Application on Streamlit
1. Login / Register

- Enter Username and Password.
- Select "Login" if you already have an account, or "Register" if it's your first time.
- Click the Proceed button.

2. Menu Navigation (Sidebar)

- After logging in, you will see 3 main menus:
  - ➕ Add Reading: to add new reading.
  - 📋 View & Update: to view, filter, sort, and update reading progress.
  - 📤 Export CSV: to download your reading list.

3. Adding Reading

- Enter the title of the reading.
- Select the type of reading (comic, manhwa, manhua, book).
- Enter the total number of parts (optional, can be left blank if ongoing).
- Click Add Entry.

4. View & Update Progress

- Use the filters and sorting at the top to filter entries.
- Select the entry you want to update, then enter the latest progress.
- Click Save Update.

5. Export Data

- Open the Export CSV menu.
- Click the Download as CSV button to download your reading file.

6. Logout

- Click the 🚪 Logout button in the sidebar to log out of your account.



## 🚀 How to Line Application

### 1. Environment Preparation

Make sure you have Python and pip installed. It is recommended to use a virtual environment.

```bash
python -m venv venv
source venv/bin/enable # Mac/Linux
venv\Scripts\enable # Windows

Demo: https://youtu.be/GiI6xKB859A

