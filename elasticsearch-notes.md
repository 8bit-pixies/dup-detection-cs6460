Question and Answer bot
=======================

This repo is used to demonstrate how one might create a simple question and answer bot.

Given a set of questions and answers that are loaded into some database, when a query comes in the most "relevant" answer can be provided if the similarity exceeds a certain level. Currently this is implemented to always give the top answer it has in its database - though filtering by similarity/relevance is fairly trivial using query DSL in elasticsearch (e.g. using `cutoff_frequency`).

Running the Script
------------------

1. Start an elasticsearch server
2. python -i create-repo.py

Enjoy!

Example:

```
# query - "registration"

The best answer returned by ES is:
    You will be issued a time ticket usually about ten days before classes start that tells you when to log in and register. There will be an email usually a few days before time tickets are assigned that explains the process in excruciating detail. To see when time tickets will be issued, check out the [Academic Calendar](http://www.registrar.gatech.edu/calendar/).

from source:
    reddit
match question:
    How does registration work for new students?

```
