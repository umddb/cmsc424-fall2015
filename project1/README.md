## Project 1: SQL Assignment, CMSC424, Fall 2015

*The assignment is to be done by yourself.*

The following assumes you have gone through PostgreSQL instructions and have ran some queries on the `university` database. 
It also assumed you have cloned the git repository, and have done a 'git pull' to download
the files. The files are:
    1. README.md: This file
    2. populate-small.sql: The SQL script for creating the data.
    3. queries.txt: The file where to enter your answer; this is the file to be submitted
    4. answers.txt: The answers to the queries on the small dataset.
    5. SQLTesting.java: File to be used for testing your submission -- see below

*Note:* The testing will be done on a different, larger dataset. We will release that dataset later.

### Getting started
Create a new database called `social` and switch to it (see the PostgreSQL setup instructions).

Run ``\i populate-small.sql'' to create and populate the tables. 

### Schema 
The dataset contains a synthetic social network dataset (inspired by Facebook etc.). Specifically it contains the following tables:
* Users: userid, name, birthdate, joined 
* Groups: groupid, name
* Friends: userid1, userid2: This is a symmetric table. For every entry $(X, Y, d)$, there is a symmetric entry $(Y, X, d)$.
* Status: userid1, status_time, text
* Members: userid, groupid

The dataset was generated synthetically: the user names, birthdates etc., 
were randomly generated, and the group names were chosen from a list of 
universities around the world. The status text is always concatenation 
of the userid and the status update time, and should not be required 
in any queries. Only status updates from a period of about 10 days
are included in the dataset, with many users having no status updates 
during that period.

In many cases (especially for complex queries or queries involving 
`max` or `min`), you will find it easier to create temporary tables
using the ``with'' construct. This also allows you to break down the full 
query and makes it easier to debug.

You don't have to use the "hints" if you don't want to; there might 
be simpler ways to solve the questions.

### Testing and submitting using SQLTesting.java
Your answers (i.e., SQL queries) should be added to the `queries.txt` file. A simple query is provided for the first answer to show you how it works.
You are also provided with a Java file `SQLTesting.java` for testing your answers.

- We recommend that you use `psql` to design your queries, and then paste the queries to the `queries.txt` file, and confirm it works.

- Compile the file: `javac -classpath ./commons-cli-1.3.1.jar:./postgresql-9.0-801.jdbc3.jar:. SQLTesting.java`

- SQLTesting takes quite a few options: use `java -classpath ./commons-cli-1.3.1.jar:./postgresql-9.0-801.jdbc3.jar:. SQLTesting -h` to see the options.

- You may get a password authentication error, since no password is set for the user. Use `\password` in `psql` to set password (SQLTesting.java
  assumes `terrapin`, but you can specify another password using `-w` option to SQLTesting.java).

- If you want to test your answer to Question 1, use: `java -classpath ./commons-cli-1.3.1.jar:./postgresql-9.0-801.jdbc3.jar:. SQLTesting -n 1`.
The program compares the result of running your query against the provided answer (in the `answers.txt` file).

- If you want to test your answers to all questions (this is what we will do), use: `java -classpath ./commons-cli-1.3.1.jar:./postgresql-9.0-801.jdbc3.jar:. SQLTesting`

- `-i` flag to SQLTesting will run all the queries, one at a time (waiting for you to press Enter after each query).

- **Note that**: We will basically run this same program on your submitted `queries.txt` file, but with the larger dataset; your score on the assignment will 
be score output by the program. The program tries to do partial credits (as you can see in the code). It is very unlikely that your score on the larger, hidden 
dataset will be higher than your score on the provided dataset.  

### Submission Instructions
Submit the `queries.txt` file using ELMS.
      
### Assignment Questions

1. Count the number of the friends of the user 'Betty Garcia'.

2. Write a query to find the name(s) of the user(s) with the largest
number of friends by first creating a temporary table using the "WITH"
construct. Order the output by name.

3. Write a query to output a list of users and their friends, such that the friend has an
upcoming birthday within next 21 days.  Assume today is Sept 1, 2015
(so look for birthdays between Sept 1 and Sept 21). You can hardcode
that if you'd like. The output should have two columns: user_name, friend_to_wish (so latter's birthday is
in the next 3 weeks). Order by user_name, friend_to_wish.<br>
Hint: Use "extract" function that operates on the dates.

IMPORTANT: Do not use `user` as the name of a column -- it is a reserved word and gives wrong answers.

4. For each user who has posted at least two status updates, count the
average amount of time between his or her status updates in seconds.
Output should contain two columns: userid, avgtime
Order the results in the increasing order by the userid.<br>
Hint: Date substraction returns the amount in (fractional) number of days. <br>
Hint 2: The number of seconds in a day is 86400.

5. Find the name(s) of the group with the maximum number of members. Order by the group 
name (in case there are more than one output).

6. Count the size of two-hop neighbrhood for the user 'Betty Garcia'. This
includes all of his friends, and the friends of his friends. Be careful
and make sure that your query does not count the same user twice.

7. For each user, report the time in days since there last status
update. If the user has no recorded status updates, then the
corresponding answer should be -1. Note that, such users do not 
appear in the status table. Since the answer depends on the date on which the query is run, your answer wouldn't match the provided sample answer exactly (which was calculated around the time when the assignment was posted). <br>
Order the result by the userid. 

8. Find the names of the 5 users with the largest number of friends. If there is a tie for the 5th place, all those users should be returned (as shown in the sample answers.txt).<br> Order by the user name.

9. Group memberships and friendships tend to be correlated. For a
specific group "g", let "n" denote the number of its members.  There are
a possible "n(n-1)/2" friendship links between these "n" members
(counting each friendship link only once). Let "m" denote the actual
number of links that exist among the members.  We will call m/(n(n-1)/2)
the "cohesiveness ratio". Write a query (or a set of queries) to find
the cohesiveness ratio for all the groups. <br>
Order the result by groupid.

10. Find the two users that were born closest to each other (there are no
two users with the same birthdate). There may be multiple such pairs.
The output should contain two columns: user1_name, user2_name, where user1_name was
born earlier than user2_name (so there will be only one row in the result for that pair). 
If there are multiple results, output should be sorted by user1_name.
