
# 🍲 Pantry Pal - Backend API

> **Project Overview** > This is the Backend service for the **Pantry Pal** mobile application. It handles the core business logic, database management, and third-party API integrations (such as RapidAPI).  
> 
> 📱 **Frontend Repository:** [Click here to view the Mobile App interface](https://github.com/Joe-Bao/Pantry-Pal-frontEnd)

## 🛠 Tech Stack
* **Framework:** Django (Python)
* **Environment:** Virtualenv
* **External Services:** RapidAPI

## ⚙️ Local Setup Instructions

Follow these steps to get the backend development environment running on your local machine.

### 1. Create and Activate Virtual Environment
```bash
python -m venv env

# On Windows:
env\Scripts\activate.bat

# On macOS/Linux:
source env/bin/activate

```

### 2. Install Dependencies

Navigate into the backend directory and install the required Python packages:

```bash
cd backend
pip install -r requirements.txt

```

### 3. Environment Variables Configuration

For security reasons, sensitive keys are not committed to this repository. You need to create your own environment file.

1. Create a `.env` file in the root directory.
2. You can use the provided `env.template` as a reference. Your `.env` (or setup script) should look like this:

```bash
#!/usr/bin/env bash
export DEBUG=1
export SECRET_KEY='input_your_django_secret_key_here'
export DJANGO_ALLOWED_HOSTS="* localhost 127.0.0.1 [::1]"
export RAPIDAPI_KEY='input_your_rapidapi_key_here'

```

*(Make sure to source this script or load these variables into your environment before running the server).*

### 4. Database Setup & Run Server

Run the migrations to set up your database schema, then start the development server:

```bash
python manage.py migrate
python manage.py runserver

```

The API will be available at `http://127.0.0.1:8000/`.
