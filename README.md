# Setup

Use the following steps to get the project setup:

1. Set up a virtual environment:
`python -m venv env`

2. Activate the virtual environment:
```
# On Windows, use:
env\Scripts\activate.bat

# For all other platforms, use:
source env/bin/activate
```

3. Navigate into the backend directory:
`cd backend`

4. Install packages:
`pip install -r requirements.txt`

5. Setup the database:
`python manage.py migrate`

6. Run the server:
`python manage.py runserver`

