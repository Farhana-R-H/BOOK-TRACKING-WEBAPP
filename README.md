# 📚 MyBookJournal

**Type:** Personal Reading Journal Web App  
**Tech Stack:** Django (Backend), HTML, CSS, JavaScript (Frontend)  
**Role:** Full Stack Developer (Solo Project)

---

## 📝 Overview

**MyBookJournal** is a web-based application designed to help readers log books, track reading sessions, and journal their thoughts. Built with Django, it offers an intuitive interface and a feature-rich dashboard to manage your reading journey.

This project is free and open to all readers looking to cultivate better habits and document their reading experiences.

---

## 🚀 Features

### 🌐 Homepage (Public Interface)

- **Carousel Walkthrough** — Step-by-step guide on using the site
- **Sections** — About Us, FAQ, Reviews, Contact Us
- **Social Footer** — Social media links for engagement
- **Call to Action** — Encourages free signup

---

### 👤 User Dashboard (Post Signup/Login)

Once logged in, users access a personalized dashboard with 5 major sections:

#### 1. 📚 Add Book
- Input: title, author, genre, pages, dates, and cover image
- Set status: "Reading", "Completed", etc.
- Add personal review and rating

#### 2. 📖 Book Logs
- Displays all added books
- Options: Edit / Delete
- Auto-updated progress bar
- Completion detection based on page count

#### 3. ⏱️ Reading Sessions
- Shows only currently reading books
- Click to log reading session
- Track pages read with date
- Progress updates automatically

#### 4. ❌ Dropped / Incomplete Books
- Shows abandoned books
- Includes a search bar

#### 5. 📊 Reading Statistics
- **Monthly Stats:** Top 3 reviewed books
- **Yearly Goals:** Reading goals tracker
- **Graphs:** Visual insights on reading performance
- Metrics like:
  - Total completed books
  - Total pages read
  - Fastest and longest books

---

## 👤 Profile Page

Accessible via navbar:

### Sidebar Info:
- Profile picture
- Username
- Full name
- Short bio

### Subsections:

- **Edit Profile:** Add/update photo, DOB, email, name, gender
- **Wishlist:** Track dreams/goals; mark as completed
- **Notepad:** Notes/reminders with full edit/save flow
- **Review Section:** Share feedback about the platform
- **Weekly Prompt:** Fun question to engage the user (answer + history view)

---

## 🛠️ Setup Instructions (Local)

```bash
git clone https://github.com/Farhana-R-H/BOOK-TRACKING-WEBAPP.git
cd BOOK-TRACKING-WEBAPP
python -m venv venv
source venv/bin/activate  # For Linux/macOS
venv\Scripts\activate     # For Windows
pip install -r requirements.txt
python manage.py runserver

