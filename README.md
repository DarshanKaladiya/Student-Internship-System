# Integrated Student Internship Portal 🎓

[](https://www.python.org/)
[](https://www.djangoproject.com/)

An **Integrated Student Internship Portal** designed to automate and streamline the application workflow for students, coordinators, and industry partners. This system replaces manual tracking with a centralized platform for internship management, application tracking, and automated status updates.

-----

## 🚀 Core Features

  * **Automated Application Workflow:** Real-time tracking of application status from submission to approval.
  * **Role-Based Dashboards:** Specialized interfaces for **Students** (Apply/Track), **Coordinators** (Verify/Manage), and **Industry Partners** (Post/Review).
  * **Document Management:** Secure upload and storage of resumes, recommendation letters, and internship completion certificates.
  * **Email Notifications:** Automated alerts for application milestones and status changes.
  * **Analytics & Reporting:** Built-in reporting for coordinators to track student placement statistics.

-----

## 🛠️ Tech Stack

  * **Backend:** Python, Django
  * **Frontend:** HTML5, CSS3, JavaScript, Bootstrap 5
  * **Database:** SQLite (Structured relational data for student/company records)
  * **Auth:** Django Built-in Authentication System

-----

## ⚙️ Installation & Setup

### Prerequisites

  * Python 3.x
  * Django

### Local Development

1.  **Clone the Repository**

    ```bash
    git clone https://github.com/DarshanKaladiya/Student-Internship-System.git
    cd Student-Internship-System
    ```

2.  **Install Requirements**
    *(No virtual environment used as per project preference)*

    ```bash
    pip install -r requirements.txt
    ```

3.  **Migrations & Superuser**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    python manage.py createsuperuser
    ```

4.  **Run Application**

    ```bash
    python manage.py runserver
    ```

-----

## 📂 Project Structure

  * `internship_portal/` - Core project settings and configurations.
  * `applications/` - Logic for internship postings and student applications.
  * `users/` - Custom user models and profile management.
  * `templates/` - Global and app-specific UI components.
  * `static/` - Managed CSS, JS, and image assets.

-----

## 👤 Contact

**Darshan Kaladiya** \* **LinkedIn:** www.linkedin.com/in/darshan-kaladiya-968093346

  * **Project Link:** [Student-Internship-System](https://www.google.com/search?q=https://github.com/DarshanKaladiya/Student-Internship-System)
