# Udacity_Fullstack_Web_developer_nanodegree

## Summary
The Full Stack Web Developer Nanodegree program equips students with the essential skills to build and deploy 
dynamic web applications. Through hands-on projects, learners gain proficiency in front-end technologies like 
HTML, CSS, and JavaScript, as well as back-end frameworks such as Flask and SQLAlchemy. 
The curriculum covers RESTful APIs, database management, and deployment strategies, enabling students to create 
robust applications that can handle user interactions and data storage.

## 1 - Project Fyyur

Fyyur is a web application designed to help users discover and manage live music events. Built using Flask and 
SQLAlchemy, this project allows users to create, view, and manage events, as well as register for them. 
The application features user authentication, event filtering, and a responsive design to enhance the user experience. 
Fyyur serves as a practical demonstration of the application of Flask and SQLAlchemy, with creation and managing of a 
database in the backend, ensuring that the data is checked before it is passed to the database.

<img src="0-Media/1-Project_Fyyur_server_running.gif" width="900" height="400" />

## 2 - Trivia App

The Trivia App allows users to play quizzes by answering questions that are organized into different categories. The app provides functionality for:

* Retrieving questions from a PostgreSQL database.
* Filtering questions by category.
* Searching for questions based on keywords.
* Adding new questions.
* Deleting questions.
* Playing a quiz by randomly selecting questions from specific categories.

The backend is developed using Python and Flask, while the database is managed with PostgreSQL.  
The application is designed to follow RESTful API principles and includes unit tests for verifying its functionality.

<img src="0-Media/2-Trivia_App_running.gif" width="900" height="400" />


https://github.com/user-attachments/assets/a01999ee-cbf4-491d-a9f5-de9df82767da




## 3 - Coffee Shop Full Stack App

This project is a part of the Udacity Full Stack Web Developer Nanodegree program, showcasing skills in creating a complete web application with a focus on backend development, authentication, and API integration.

## Project Overview

The Coffee Shop Full Stack App allows users to manage drinks offered by a fictional coffee shop. The app includes a backend built with Python and Flask, and it’s secured with Auth0 for user authentication and authorization. The frontend is developed with modern web technologies to provide a smooth, interactive experience.

## Features

- **User Roles**: The app implements two roles:
  - **Barista** - read-only access to view drinks.
  - **Manager** - full access to create, update, and delete drinks.
- **CRUD Operations**: Users with the appropriate permissions can create, read, update, and delete drinks.
- **Authorization**: Uses JWT tokens and Auth0 to secure endpoints and manage access based on user roles.
- **RESTful API**: Provides structured and secure API endpoints for frontend communication.
- **Database Integration**: Stores drink information using PostgreSQL, including details like drink recipes and ingredient amounts.

## Tech Stack

- **Backend**: Python, Flask, SQLAlchemy, PostgreSQL, Auth0
- **Frontend**: JavaScript, HTML/CSS
- **Deployment**: Configured for easy deployment on services like Heroku or AWS

https://github.com/user-attachments/assets/c42e9454-9d62-4f98-9385-4806a0804922



