# Trivia app documentation

This application performs a trivia game, where the user can
pick and responde to several different questions belonging to different
categories.

# API documentation

* This documentation shows how to use the API of trivia app, with information
of how to use the endpoints, how to call then, and the return data when success
is attained or when failure appears.
* Authentication: up to this moment no authentication is needed to use this API.

The base URL is:
```
http: // 127.0.0.1: 5000
```

# Error handling

There can be several type of errors got when using this API.

**Error code 400**

Example json error response:

```
{
    "error": 400,
    "message": "bad request",
    "success": false
}
```

**Error code 404**

Example json error response:

```
{
    "error": 404,
    "message": "resource not found",
    "success": false
}
```

**Error code 422**

Example json error response:

```
{
    "error": 422,
    "message": "unprocessable",
    "success": false
}
```

**Error code 500**

Example json error response:

```
{
    "error": 500,
    "message": "internal server error",
    "success": false
}
```

# API Endpoint Library

## GET requests:

1. ```'/categories'``` 
* Endpoint: returns the existing categories at the database
* Sample request: ```curl http://127.0.0.1:5000/categories```
* Arguments including data types: not applicable

```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true,
  "total_categories": 6
}
```

2. ```'/questions'``` 
* Endpoint: returns the existing questions at the database
* Sample request: ```curl http://127.0.0.1:5000/questions```
* Arguments including data types: not applicable
* Response object including status codes and data types: The result is paginated  
in groups of 10 questions each

```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": null,
    "questions": [
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer": "Brazil",
            "category": 6,
            "difficulty": 3,
            "id": 10,
            "question": "Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer": "Uruguay",
            "category": 6,
            "difficulty": 4,
            "id": 11,
            "question": "Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Lake Victoria",
            "category": 3,
            "difficulty": 2,
            "id": 13,
            "question": "What is the largest lake in Africa?"
        },
        {
            "answer": "The Palace of Versailles",
            "category": 3,
            "difficulty": 3,
            "id": 14,
            "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
            "answer": "Agra",
            "category": 3,
            "difficulty": 2,
            "id": 15,
            "question": "The Taj Mahal is located in which Indian city?"
        },
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        }
    ],
    "success": true,
    "total_questions": 21
}
```

3. ```'/categories/<int:category>/questions'``` 
* Endpoint: returns the existing questions that belong to a given category
* Sample request: ```curl http://127.0.0.1:5000/categories/6/questions```
* Arguments including data types: not applicable

```
{
  "current_category": 6,
  "questions": [
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

## DELETE requests:

1. ```'/questions/<int:question_id>'``` 
* Endpoint: delete a question by id
* Sample request: ```curl -X DELETE http://127.0.0.1:5000/questions/13```
* Arguments including data types: the id of the given questions, integer type
* Response object including status codes and data types: returns the deleted question,  
the current questions and the number of current questions

```
{
  "deleted": 13,
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }
  ],
  "success": true,
  "total_questions": 19
}
```

## POST requests:

1. ```'/questions'``` 
* Endpoint: Creates a new question
* Sample request: ```
                curl -X POST -H "Content-Type: application/json" -d '{"question":"What is the capital city of Mongolia?",
                                                                      "answer":"Ulaanbaatar", 
                                                                      "category": "3", 
                                                                      "difficulty": "5"}' http://127.0.0.1:5000/questions
                 ```
* Arguments including data types: the question and answer as strings, category and difficulty as integers
* Response object including status codes and data types: Returns the number of the created questions,  
the first 10 questions, and the number of total questions currently

```
{
  "created": 29,
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }
  ],
  "success": true,
  "total_questions": 21
}
```

2. ```'/questions'``` 
* Endpoint: Gets the questions that have a search term as a substring in the question
* Sample request: ```
                curl -X POST -H "Content-Type: application/json" -d '{"search_term":"title"}' http://127.0.0.1:5000/questions 
                 ```
* Arguments including data types: the search_term as a string
* Response object including status codes and data types: Returns the questions that match the search  
criteria and the number of them as well

```
{
  "created": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ],
  "success": true,
  "total_questions": 2
}
```

2. ```'/quizzes'``` 
* Endpoint: It gets a new questions to play the quiz
* Sample request: ```
                curl -X POST http://localhost:5000/quizzes -H "Content-Type: application/json" -d '{"previous_questions": [1, 2, 3], "quiz_category": {"id": 1}}' | jq '.'```
* Arguments including data types: previous_questions as a list of integers, quiz_category as a  
dictionary containing id field as an integer
* Response object including status codes and data types: Returns the new question belonging to the given category

```
{
  "question": {
    "answer": "The Liver",
    "category": 1,
    "difficulty": 4,
    "id": 20,
    "question": "What is the heaviest organ in the human body?"
  },
  "success": true
}
```