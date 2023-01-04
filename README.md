# Movie REST API

This repository contains the source code for a REST API for movies. The API allows users to search for and find information about movies, including search by title, director, actor, and category, and the ability to display descriptions and information about movies from a movie database. The API was built using Python, Flask, and SQLAlchemy, and is accessible via HTTP requests and responses.

## Features

- Search for movies by title, director, actor, or category
- View detailed information about movies, including descriptions, cast and crew, and release date
- Secure authentication and authorization using JSON Web Tokens (JWT)
- Robust security measures to protect sensitive data
- Scalable and performant design, able to handle high volume of requests and responses

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
### Prerequisites
- Python 3.6 or higher
- Flask
- Flask-SQLAlchemy
- Flask-JWT-Extended

The Movie REST API uses Mailgun API to send registration email to new users.
## Installation

1. Clone the repository:
```sh
git clone https://github.com/GhaziBoussida/MOVIE-REST-API.git
```

2. Install the required dependencies:

```sh
pip install -r requirements.txt
```
3. Set the FLASK_APP and FLASK_ENV environment variables:
```sh
export FLASK_APP=app
export FLASK_ENV=development
```
4. Set the MAILGUN_API_KEY and MAILGUN_DOMAIN environment variables in .env file:
```
MAILGUN_API_KEY="Value"
MAILGUN_DOMAIN="Value"
```
5. Run the development server:
```sh
flask run
```
## API Documentation
### User endpoints - Operations on users
#### POST /register
Add new user to the database.
##### Headers
-   'Authorization': JWT token

##### Parameters
- username (required) : Username of the user. 
- password (required) : password of the user.

##### Responses
- 201, Success
```JSON
{
  "message": "User created successfully."
}
```
- 400 , Error
```JSON
{
"message":"A user with that username already exists."
}
```
#### POST /login
Login as a registered user and obtain access and refresh tokens.
##### Parameters
- username (required) : Username of the user. 
- password (required) : password of the user.

##### Responses 
- 200, Succes
```JSON
{
  "access_token": "string",
  "refresh_token": "string"
}
```
- 401 , Error
```JSON
{ 
"message":"Invalid credentials."
}
```
#### POST /logout
Logout of logged user.
##### Headers
-   'Authorization': Bearer access token. 

##### Parameters
- No parameters

##### Responses 
- 200, Success
```JSON
{
	"message": "Successfully logged out"
}
```
#### GET /user/{user_id}
Get a specific user by his ID.
##### Parameters
- user_id (required) : ID of the user to fetch.

##### Responses 
- 200, Success
```JSON
{
  "id": integer,
  "username": "string"
}
```
- 404, Error
```JSON
{
	"message": "User not found"
}
```
#### DELETE /user/{user_id}
Detele specific user by his ID
##### Headers
-   'Authorization': Bearer access token. 
##### Parameters
- user_id (required) : ID of the user to delete.

##### Responses 
- 200, Success
```JSON
{
	"message": "User deleted."
}
```
- 404, Error 
```JSON
{
	"message": "User not found"
}
```
#### POST /refresh
Obtain a fresh access token.
##### Headers
-   'Authorization': Bearer refresh token. 

##### Parameters
- No parameters

##### Responses 
- 200, Success
```JSON
{
	"access_token": "string"
}
```
### Actor endpoints - Operations on actors
#### POST /actor/{name}
Add actor to the database.
##### Headers
-   'Authorization': Bearer access token. 

##### Parameters
- name (required): Name of the actor to create.

##### Responses
- 200, Success
```JSON
{
	"id": integer,
	"movies": [],
	"name": "string"
}
```
- 400, Error
```JSON
{
	"message": "An actor with name {name} already exists."
}
```
- 500, SQLAlchemyError
```JSON
{
	"message": "An error occurred while inserting the actor."
}
```
#### GET /actor/{name}
Get specific actor by name.
##### Headers
-   'Authorization': Bearer access token.

##### Parameters
- name (required): Name of the actor to fetch.

##### Responses 
- 200, Success
```JSON
{
	"id": integer,
	"movies": [],
	"name": "string"
}
```
- 404, Error
```JSON
{
	"message": "Actor not found."
}
```
#### DELETE /actor/{name}
Delete specific actor by name.
##### Headers
-   'Authorization': Bearer access token 

##### Parameters
- name (required): Name of the actor to delete.

##### Responses
- 200, Success
```JSON
{
	"message": "Actor deleted."
}
```
- 404, Error
```JSON
{
	"message": "Actor not found."
}
```
#### GET /actor
Get list of all actors in the database.
##### Headers
-   'Authorization': Bearer access token 

##### Parameters
- No parameters

##### Responses 
- 200, Success
```JSON
[
  {
    "id": integer,
    "name": "string",
    "movies": [
      {
        "id": integer,
        "release_date": "string",
        "description": "string",
        "name": "string"
      }
    ]
  }
]
```
#### POST /movie/{movie_id}/actor/{actor_id}
Link existing specific actor by ID to existing specific movie by ID.
##### Headers
-   'Authorization': Bearer access token 

##### Parameters
- movie_id (required) : ID of the movie to link.
- actor_id (required) : ID of the actor to link.

##### Responses 
- 200, Success
```JSON
  {
    "id": integer,
    "name": "string",
    "movies": [
      {
        "id": integer,
        "release_date": "string",
        "description": "string",
        "name": "string"
      }
    ]
  }
```
- 404, Error 
```JSON
  {
  "status": "Not Found"
  }
```
- 500 , SQLAlchemyError
```JSON
  {
  "message":"An error occurred while inserting the actor."
  }
```
#### DELETE /movie/{movie_id}/actor/{actor_id}
##### Headers
-   'Authorization': Bearer access token 

##### Parameters
- movie_id (required) : ID of the movie to unlink.
- actor_id (required) : ID of the actor to unlink.

##### Responses
- 200, Success
```JSON
{
"message": "Actor removed from Movie"
}
```
- 404, Error
```JSON
  {	
	"message": "Actor not found in movie.",
  }
```
- 401, Error
```JSON
{
"message":"Admin privilege required."
}
```
- 500, SQLAlchemyError
```JSON
{
	"message": "An error occurred while inserting the actor."
}
```
### Director endpoints - Operations on directors
#### POST /director/{name}
Add director to the database.
##### Headers
-   'Authorization': Bearer access token. 

##### Parameters
- name (required): Name of the director to create.

##### Responses
- 200, Success
```JSON
{
	"id": integer,
	"movies": [],
	"name": "string"
}
```
- 400, Error
```JSON
{
	"message": "A director with name {name} already exists."
}
```
- 500, SQLAlchemyError
```JSON
{
	"message": "An error occurred while inserting the director."
}
```
#### GET /director/{name}
Get specific director by name.
##### Headers
-   'Authorization': Bearer access token.

##### Parameters
- name (required): Name of the director to fetch.

##### Responses 
- 200, Success
```JSON
{
	"id": integer,
	"movies": [],
	"name": "string"
}
```
- 404, Error
```JSON
{
	"message": "Director not found."
}
```
#### DELETE /director/{name}
Delete specific director by name.
##### Headers
-   'Authorization': Bearer access token 

##### Parameters
- name (required): Name of the director to delete.

##### Responses
- 200, Success
```JSON
{
	"message": "Director deleted."
}
```
- 404, Error
```JSON
{
	"message": "Director not found."
}
```
- 401, Error
```JSON
{
"message":"Admin privilege required."
}
```
#### GET /director
Get list of all directors in the database.
##### Headers
-   'Authorization': Bearer access token 

##### Parameters
- No parameters

##### Responses 
- 200, Success
```JSON
[
  {
    "id": integer,
    "name": "string",
    "movies": [
      {
        "id": integer,
        "release_date": "string",
        "description": "string",
        "name": "string"
      }
    ]
  }
]
```
### Category endpoints - Operations on categories
#### POST /category/{name}
Add category to the database.
##### Headers
-   'Authorization': Bearer access token. 

##### Parameters
- name (required): Name of the category to create.

##### Responses
- 200, Success
```JSON
{
	"id": integer,
	"movies": [],
	"name": "string"
}
```
- 400, Error
```JSON
{
	"message": "A category with name {name} already exists."
}
```
- 500, SQLAlchemyError
```JSON
{
	"message": "An error occurred while inserting the category."
}
```
#### GET /category/{name}
Get specific category by name.
##### Headers
-   'Authorization': Bearer access token.

##### Parameters
- name (required): Name of the category to fetch.

##### Responses 
- 200, Success
```JSON
{
	"id": integer,
	"movies": [],
	"name": "string"
}
```
- 404, Error
```JSON
{
	"message": "Category not found."
}
```
#### DELETE /category/{name}
Delete specific category by name.
##### Headers
-   'Authorization': Bearer access token 

##### Parameters
- name (required): Name of the category to delete.

##### Responses
- 200, Success
```JSON
{
	"message": "Category deleted."
}
```
- 404, Error
```JSON
{
	"message": "Category not found."
}
```
- 401, Error
```JSON
{
"message":"Admin privilege required."
}
```
#### GET /category
Get list of all categories in the database.
##### Headers
-   'Authorization': Bearer access token 

##### Parameters
- No parameters

##### Responses 
- 200, Success
```JSON
[
  {
    "id": integer,
    "name": "string",
    "movies": [
      {
        "id": integer,
        "release_date": "string",
        "description": "string",
        "name": "string"
      }
    ]
  }
]
```
### Movie endpoints - Operations on movies
#### POST /movie/{name}
Add movie to the database.
##### Parameters
- name (required): Name of the movie to create.
- category_id : ID of the category of the movie to create.
- director_id : ID of the director of the movie to create.
- description : Description of the movie to create.
- release_date : Release date of the movie to create.

##### Responses
- 200, Success
```JSON
{
  "category": {
    "id": integer,
    "name": "string",
    "movies": [
      {
        "release_date": "string",
        "description": "string",
        "id": integer,
        "actors": [
          {
            "id": integer,
            "name": "string"
          }
        ],
        "name": "string"
      }
    ]
  },
  "release_date": "string",
  "description": "string",
  "director": {
    "id": integer,
    "name": "string",
    "movies": [
      {
        "release_date": "string",
        "description": "string",
        "id": integer,
        "actors": [
          {
            "id": integer,
            "name": "string"
          }
        ],
        "name": "string"
      }
    ]
  },
  "director_id": integer,
  "category_id": integer,
  "id": integer,
  "actors": [
    {
      "id": integer,
      "name": "string"
    }
  ],
  "name": "string"
}
```
- 400, Error
```JSON
{
	"message": "A movie with name {name} already exists."
}
```
- 500, SQLAlchemyError
```JSON
{
	"message": "An error occurred while inserting the movie."
}
```
#### GET /movie/{name}
Get specific movie by name.
##### Parameters
- name (required): Name of the movie to fetch.

##### Responses 
- 200, Success
```JSON
{
  "category": {
    "id": integer,
    "name": "string",
    "movies": [
      {
        "release_date": "string",
        "description": "string",
        "id": integer,
        "actors": [
          {
            "id": integer,
            "name": "string"
          }
        ],
        "name": "string"
      }
    ]
  },
  "release_date": "string",
  "description": "string",
  "director": {
    "id": integer,
    "name": "string",
    "movies": [
      {
        "release_date": "string",
        "description": "string",
        "id": integer,
        "actors": [
          {
            "id": integer,
            "name": "string"
          }
        ],
        "name": "string"
      }
    ]
  },
  "director_id": integer,
  "category_id": integer,
  "id": integer,
  "actors": [
    {
      "id": integer,
      "name": "string"
    }
  ],
  "name": "string"
}
```
- 404, Error
```JSON
{
	"message": "Movie not found."
}
```
#### DELETE /movie/{name}
Delete specific movie by name.
##### Headers
-   'Authorization': Bearer access token 

##### Parameters
- name (required): Name of the movie to delete.

##### Responses
- 200, Success
```JSON
{
	"message": "Movie deleted."
}
```
- 404, Error
```JSON
{
	"message": "Movie not found."
}
```
- 401, Error
```JSON
{
"message":"Admin privilege required."
}
```
#### GET /movie
Get list of all movies in the database.
##### Parameters
- No parameters

##### Responses 
- 200, Success
```JSON
[
{
  "category": {
    "id": integer,
    "name": "string",
    "movies": [
      {
        "release_date": "string",
        "description": "string",
        "id": integer,
        "actors": [
          {
            "id": integer,
            "name": "string"
          }
        ],
        "name": "string"
      }
    ]
  },
  "release_date": "string",
  "description": "string",
  "director": {
    "id": integer,
    "name": "string",
    "movies": [
      {
        "release_date": "string",
        "description": "string",
        "id": integer,
        "actors": [
          {
            "id": integer,
            "name": "string"
          }
        ],
        "name": "string"
      }
    ]
  },
  "director_id": integer,
  "category_id": integer,
  "id": integer,
  "actors": [
    {
      "id": integer,
      "name": "string"
    }
  ],
  "name": "string"
}
]
```

## Deployment

#### Local deployment
To run the API locally, follow these steps:

1- Clone the repository:
```sh
git clone https://github.com/GhaziBoussida/MOVIE-REST-API.git
```
2- Install the dependencies:
```sh
pip install -r requirements.txt
```

3- Run the database migrations:
``` sh
flask db upgrade
```
4- Start the API:
``` sh
flask run
```
The API will be available at http://localhost:5000.

#### Online deployment

1- Push Repository to GitHub. Do NOT include the .env file that contains the API key.

2- Create Render.com account.

3- Link Github and Render accounts.

4- Create new WebService Project in Render

5- Link Github repository.

4- Add environment variables or upload .env file to Render.

5- Deploy the API

The API will be available at the domain URL provided by Render.

## Built With
- [Python](https://www.python.org/) - The programming language used
- [Flask](https://flask.palletsprojects.com/en/2.1.x/) - The web framework used
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/) - The ORM used for interacting with the database
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/) - A library for adding JSON Web Token (JWT) support to Flask, including access and refresh tokens, token refreshment, and role-based access control. This library was used to provide secure authentication and authorization for the API.
- [MAILGUN API](https://documentation.mailgun.com/en/latest/) - Email API for Sending. Send, receive, and track emails with Mailgun's email API.
