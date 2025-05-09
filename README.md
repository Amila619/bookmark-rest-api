# Bookmark REST API

This is a RESTful API built with Flask for managing bookmarks. It provides robust features such as user authentication using JSON Web Tokens (JWT), CRUD operations for bookmarks, and interactive API documentation.

### API Documentation

The API includes **Swagger UI** for seamless interaction and testing of endpoints. Once the application is running, you can access the Swagger documentation at:

```
http://localhost:5000/api/docs/
```

Swagger UI offers a visually intuitive interface to explore the API, view endpoint details, and test requests directly from the browser. This makes it easier for developers to understand and integrate the API into their applications.

### Available Endpoints

| Method | Endpoint           | Description               |
|--------|--------------------|---------------------------|
| POST   | `/auth/register`   | Register a new user       |
| POST   | `/auth/login`      | Log in and get a token    |
| GET    | `/bookmarks`       | Retrieve all bookmarks    |
| POST   | `/bookmarks`       | Create a new bookmark     |
| GET    | `/bookmarks/<id>`  | Retrieve a specific bookmark |
| PUT    | `/bookmarks/<id>`  | Update a specific bookmark|
| DELETE | `/bookmarks/<id>`  | Delete a specific bookmark|

Each endpoint is secured with token-based authentication, ensuring that only authorized users can access or modify data. The API is designed to be lightweight, easy to extend, and developer-friendly.

## Features

- User authentication with JSON Web Tokens (JWT)
- Create, read, update, and delete bookmarks
- Secure endpoints with token-based authentication
- Lightweight and easy to extend
- Interactive API documentation with Swagger

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/bookmark-rest-api.git
    cd bookmark-rest-api
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    - Create a `.env` file in the project root.
    - Add the following variables:
      ```
      FLASK_APP=app.py
      FLASK_ENV=development
      SECRET_KEY=your_secret_key
      ```

5. Run the application:
    ```bash
    flask run
    ```