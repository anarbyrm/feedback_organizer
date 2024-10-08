# feedback_organizer

## Introduction

The project is aimed to perform aggregation operations for specified data on MongoDB, retrieve the result and present the aggregated data in table structure.

### Tech stack

It is build on the top of **Python, Django, MongoDB** and **Docker**. Connection with MongoDB is established with pymongo adapter.

### URLs

http://localhost:8000/feedbacks - retrieves json feedback data if exists in db or it seeds db with data then fetches it.

http://localhost:8000/feedbacks/scores - fetches all aggregated data based on pipelines and presents it in table form.


## Development Stages

### Initial stage

The project initialized and structured for starters. Then environment variables are configured. After that project has been dockerized using env variables.


### Pipeline building stage

After initial configurations, pipelines are started to be built using MongoDB compass. MongoDB Compass is a tool to connect to a MongoDB instance and do various operations. It also makes it easy to build pipelines for aggregation operations in the aggregation section.

Pipelines are list of objects. Each object called a stage. In the project 4 stages are used: 1 unwind, 2 grouping and 1 project operations.

**Unwind:** separated documents based on feedback_rate field which is array.

**First Group:** grouped documents based on branch name and service name and accumulated count of rates in it.

**Second Group:** grouped documents generated on previous stage based on branch name and pushed objects into an array. Objects contains service name and calculated score based on rates with given formula.

**Project:** projected branch name and service objects array


Final result looks like this:

```json

{

    "_id": "<branch_name>",

    "branch_name": "<branch_name>",

    "services": [{

        "name": "<service_name>",

        "score": "<service_score>"

    }]

}

```

***NOTE: I have decided to save the pipelines data into a json file and read from it when they are needed instead of writing it inside codebase.***

  

### MongoDB integration to project

Django ORM does not support NoSQL databases by default. There is various packages to connect a django project to MongoDB. One of the famous ones is Djongo. Reasons it is not used in the project are:

1) It is using Django ORM. This means Django ORM will first create SQL queries and then convert them into MongoDB queries. It will slow the querying process.
2) it does not allow to do complex queries like aggregations freely.
3) it is not stable because project is not maintained anymore.


In this project **pymongo** package is used. Pymongo is MongoDB adapter allows us to leveradge all functionalities of MongoDB. The downside of this package is that it is not possible to follow the traditional connection settings opinions for django completely. So I have created MongoService class to handle the connection. It also have some handful methods to perform operations on db related to the needs of this project. These methods helps hugely to separate business logic from views and makes it more readable as well.


###  Usage of MongoDB queries on views
MongoService class is initialized once and used inside the views as needed.

## Setup
1. Clone the project repo:

```bash

git clone <github_repo_link>

```
2. Set environment variables:
create .env file and set values like below:

  
```
MONGO_DB_HOST=
MONGO_DB_PORT=
MONGO_DB_NAME=
DEBUG=
SECRET_KEY=
```

3. Run the server using docker
```bash

docker-compose up --build

```
4. Go to "http://localhost:8000" to see the website.
