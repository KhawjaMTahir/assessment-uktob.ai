# assessment-uktob.ai

## Objective
This repository contains basic and efficient back-end for a note-taking application. The application is allowing to register, update and authenticate users alongside allowing users to create, read, update, and delete (CRUD) notes. THe application is using `rest_framework.authtoken` for authentication. `DRF Spectacular` has been used for API documentation.
Additionaly, application is using LangChain with ChatGPT to summarize users' notes.


## Installation
Clone this repository locally and follow the below listed steps to install:
1. **Virtual Environment [Optional]**

Here is a link about how to create [Virtual Environment](https://docs.python.org/3/library/venv.html) in python. After creating the environment, activate it and navigate to the project directory.

2. **Installation Command**

You will find a detail requirements.txt file which contains all the requirements for this application. Use the command below to install requirements
```
pip install -r requirements.txt
```
3. **Running the Application**

First, creating and migrating the models into Database, following commands can be used for it.

```
python manage.py makemigrations && python manage.py migrate
```
After migrations, the development server can be start using command listed below.
```
python manage.py runserver
```
3. **Browsing the API Docs**
Once the development server is started, use the below url for comprehensive documentation of the application
```
http:127.0.0.1:8000/api/docs
```


## API Endpoints
**User Endpoints**
```
POST /api/user/create/
GET /api/user/me/
PUT /api/user/me/
PATCH /api/user/me/
POST /api/user/token/
```
The above methods are associated with user endpoints, which will be utilized for register, update and authenticate user into the application.

**Notes Endpoint**
```
GET /api/notes/notes/
POST /api/notes/notes/
GET /api/notes/notes/{id}/
PUT /api/notes/notes/{id}/
PATCH /api/notes/notes/{id}/
DELETE /api/notes/notes/{id}/
```
Above all are the methods associated with Notes API, an authenticated user can create, update, view and delete his own notes. The user will not be able to view or perform any action on other users' notes.

**Schema and documentation**
```
GET /api/schema/
GET /api/docs/
```
This endpoint display **SCHEMA** of the API

## Testing the API
All the test cases related to user and notes including models and views are written. These tests can be find in the `/test/` directory of each module. The test can be executed and run using below command.
```
python manage.py test
```
**Important Note**
The langchain openai features requires api key and also test will also need that api key as well. So inorder to make the application test and run smooth, key must be specify in the `.env` file.
