# Online Forum Application

A simple online forum application built with Flask and MongoDB. This application allows users to create, read, update, and delete posts and comments.

## Features

- Create new posts
- Edit and delete existing posts
- Add comments to posts
- Delete comments

## Prerequisites

- Python 3.11 or later
- MongoDB (local or Atlas)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/ez4mz/Flask-MongoDB-Online-Forum
    ```

2. Create a virtual environment (optional but recommended):

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file based on the `.env.example` file and set your environment variables:

    ```plaintext
    MONGO_URI=mongodb+srv://<username>:<password>@<cluster-url>/<dbname>?retryWrites=true&w=majority
    FLASK_ENV=development
    ```

5. Run the application:

    ```bash
    python app.py
    ```

6. Open your browser and navigate to `http://127.0.0.1:5000` to see the application.
