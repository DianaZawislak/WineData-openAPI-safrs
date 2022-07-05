# Flask Project 1
### Name: <Insert Here>
### UCID: <Insert Here>
### Put a picture of your homepage here [example](endpoints.png)
## Introduction
The purpose of this unit is to demonstrate how a framework / library like [SAFRS](https://github.com/thomaxxl/safrs)
automates some boilerplate code required to create a REST API. Primarily SAFRS provides openAPI spec and JSON API in one
package. This project also illustrates how to use some commands of the [Pandas](https://pandas.pydata.org) library to
normalize and import a csv file into a SQL database. It also introduces you to the basics
of [SQLAlchemy](https://www.sqlalchemy.org)
### Unit Video - [Watch Here](https://youtu.be/WrkX6o7rUWg)
### Required Readings
1. [AAA Testing](https://jamescooke.info/arrange-act-assert-pattern-for-python-developers.html)
2. [SAFRS EXAMPLE WITH TESTS](https://github.com/thomaxxl/safrs-example) <- This is more than you need but a good
   reference for how to do some things
3. [SAFRS Library](https://github.com/thomaxxl/safrs)
4. [SAFRS DEMO AND DOCUMENTATION](https://github.com/thomaxxl/safrs/wiki?ref=morioh.com&utm_source=morioh.com)
## Project Requirements
For this project you need to select a CSV data set and modify the code in this project to import the data, create the
sqlalchemy models, and write meaningful tests that test all the endpoints generate by SAFRS. You need at least one
test for each endpoint, and you need to create at least one test for each endpoint that tests the endpoints' validation.
You need to be able to create at least two tables like I have done with countries and cities. You should make separate
functions for each test and create fixtures to remove redundant code. I have provided [test_task1.py](tests/test_task1.py) and test_task2.py
for you to add your tests. Test task 1 is for all tests for one of your models and test task 2 is for your other models.
### Sample CSV Files
1. [Fun Data](https://domohelp.domo.com/hc/en-us/articles/360043931814-Fun-Sample-DataSets)
2. [More CSV Data](https://people.math.sc.edu/Burkardt/datasets/csv/csv.html)
### Grading Notes:
This project will be graded manually and using GitHub Classroom. You should write at least 20 test functions, a process
to import your data, and at least one fixture. You also need to follow AAA testing and provide good documentation for
your tests, so that it is clear what you are testing. Follow the example in [test_task1.py](tests/test_task1.py).
#### Grading Rubric:
1. Write meaningful complete tests as demonstrated in [test task_1.py](tests/test_task1.py) = 40 Points
2. 40 Tests = 40 Points
3. Follow the AAA Test Pattern = 10 Points
4. 1 Fixture or Helper = 5 Points
5. 1 Import Process = 5 Points
* Total:  100 Points
### Steps to submit
1. Put your name in the README.MD as indicated above. If you don't do this you will get a 0.
2. Put a screenshot that shows the API Homepage with all the endpoints displaying. [Example](endpoints.png)
3. Submit a link to your GitHub Classroom repository to the Canvas assignment i.e. the one with your github ID in it
## Steps to Install Application

1. Clone the repo, do pip install -r requirements.txt, and then pytest --pylint all the tests pass
2. Run pytest --pylint to see that the test tasks are failing currently and that you need to complete them
3. Setup Pycharm run configuration for flask ![Pycharm Flask Run Configuration](flask-run-config.png)