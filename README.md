## Installation

1. Install requirements and create virtual environment:
   pipenv install pipenv shell
2. Create and fill out the local settings `.env` file placed at root directory, obligatory environment variables:
    - django secret key `SECRET_KEY`
    - debug setting `DEBUG`
    - database url `DATABASE_URL`

3. Run database migrations using `./manage.py migrate`
4. Run tests to make sure that everything is ok `./manage.py test`
5. Run server using `./manage.py runserver`

## Description

App allows managing books - listing, creating and importing. Books can be added in two ways. The first method is by
create form. The second way is by importing batch of books via Google Books API from Google Books db. Books can be
imported via import form which allows importing books based on Google Books API keywords: title, author, subject or
ISBN. Imported or created books are stored in database and can be accessed via list. List is browsable using criteria:
title, author and publication date range.
