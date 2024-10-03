# API for Yatube

## Description

The Yatube API project is a RESTful API designed for a social network-like platform where users can create and interact with posts. It enables users to publish content, comment on posts, follow other users, and manage their groups. The API aims to provide a seamless experience for users to engage with the platform's features, facilitating interaction and community building. 

Key features include:
- User authentication and management
- Post creation, editing, and deletion
- Commenting on posts
- Following and unfollowing users
- Group management for topic-based discussions
- Search functionality in followings

This API serves as the backend for a modern social networking application, focusing on usability and scalability.

## Stack

- Python: 3.9.13
- Django: 3.2
- Django Rest Framework (DRF)
- Authentication: PyJWT 
- Database: SQLite
- Testing: PyTest
- Code Quality: Ruff
- Import Sorting: Isort

## Installation

To set up the project on your local machine, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/RockurDev/api_final_yatube.git

2. Navigate to the project directory:
    ```bash
    cd api_final_yatube

3. Install and activate virtual environment
    ```bash
    python -m venv .venv && . .venv/bin/activate

4. Install the required dependencies:
    ```bash
    pip install -r requirements.txt

5. Run database migrations:
    ```bash
    python manage.py migrate

6. Start the server:
    ```bash
    python manage.py runserver

## Project Specifications

The project specifications are available at the following path:

API Documentation: http://localhost:8000/redoc/

## Usage example

Bellow are some examples of API requests:

### Get All Posts

Request:
```http
GET /api/v1/posts/
```

Response:
```json
[
    {
        "id": 1,
        "title": "First Post",
        "content": "Content of the first post",
        "author": "username"
    },
    {
        "id": 2,
        "title": "Second Post",
        "content": "Content of the second post",
        "author": "username"
    }
]
```
### Create a new posts

Request:
```http
POST /api/v1/posts/
Content-Type: application/json

{
    "title": "New Post",
    "content": "Content of the new post"
}
```

Response:
```json
{
    "id": 1,
    "title": "New Post",
    "content": "Content of the new post",
    "author": "username"
}
```

## Author

[RockurDev](https://github.com/RockurDev)

## Project Link

[API for Yatube](https://github.com/RockurDev/api_final_yatube/blob/master/README.md)