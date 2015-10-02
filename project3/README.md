## Project 3: Advanced SQL Assignment, CMSC424, Fall 2015

*The assignment is to be done by yourself.*

### Assignment Questions

**Question 1 (.5 pt)**: Consider the following query which finds the number of status updates for users whose name starts with 'Anthony'. Before doing this, make sure to create a new database with the provided `populate-socialskewed.sql` file, and use that database for all the questions here.

```
select u.userid, name, count(*) 
from users u join status s on (u.userid = s.userid and u.name like 'Anthony%') 
group by u.userid, name order by u.userid;
```

The result however does not contain the users whose name contains 'Anthony' but who have no status update (e.g., `user1`). So we may consider
modifying this query to use a left outer join instead, so we get those users as well: 

```
select u.userid, name, count(*) 
from users u left outer join status s on (u.userid = s.userid and u.name like 'Anthony%') 
group by u.userid, name order by u.userid;
```

Briefly explain why this query does not return the expected answer, and rewrite the query so that it does. Note: the query has two issues -- it uses
left outer join incorrectly, and also does not reason about aggregates over NULLs properly. 

The final answer should look like this:
```
	   userid   |         name         | count 
	   ------------+----------------------+-------
	   user0      | Anthony Martin       |     0
	   user1      | Anthony Rodriguez    |    11
	   user2      | Anthony Taylor       |    91
	   user3      | Anthony Williams     |     0
	   user4      | Anthony Wright       |    27
	   (5 rows)

```

**Question 2 (.5 pt)**: As we discussed in class, EXPLAIN can be used to see the query plan used by the database system to execute a query. For the following
query, draw the query plan for the query, clearly showing the different operators and the options they take. The query is trying to find, for each user, how many of its friends have never written a status update. 

```
select f.userid1, count(*) 
from friends f join (select * from users 
		     where userid not in (select userid from status)) u 
		     on (u.userid = f.userid2) 
group by f.userid1;
```

**Question 3 (.5 pt)**: Similarly draw the query plan for the following query, and annotate which operators are responsible for creating `temp1`, `temp2`, and the final answer.

```
with temp1 as (
        select m1.groupid, count(*) as m
        from members m1, members m2, friends f
        where m1.groupid = m2.groupid and f.userid1 = m1.userid 
              and f.userid2 = m2.userid and m1.userid < m2.userid
        group by m1.groupid
),
temp2 as (
    select m.groupid, count(*) as n
    from members m
    group by m.groupid
)
select temp1.groupid, 2.0*m/(n*(n-1))
from temp1, temp2
where temp1.groupid = temp2.groupid
order by temp1.groupid;
```

**Question 4 (.5 pt)**: The EXPLAIN output also shows how many tuples the optimizer expects to be generated after each operation (`rows`). EXPLAIN ANALYZE 
executes the query and also shows the **actual** number of tuples generated when the query plan was executed. 

For the following query, how well do the cardinality estimates made by the optimizer (for the outputs of different operators) match up with the actual numbers of tuples that were generated? Make sure to do this on the `socialskewed` dataset.

```
select u.name, count(*) from users u, friends f1, status s 
where u.name like 'Chris%' and extract(month from status_time) = 10 
      and u.userid = f1.userid1 and s.userid = f1.userid2 
group by u.name;
```

**Question 5 (1 pt)**: [Trigger] Create a new table: `NumberOfStatusUpdates(userid, user_name, num_updates)`
using the `Status` table, where you record the number of status made by each user. 
Write a `trigger` to keep this new table updated when a new entry is inserted into 
or a row is deleted from the Status table. Remember the user name corresponding to the 
new status update may not exist in the NumberOfStatusUpdates. Similarly, if deletion of 
a status update from the Status table results in a user not having any status update,
then the tuple in NumberOfStatusUpdates should be deleted.
 
**Question 6 (2 pt)**:  As we discussed in the class a few weeks ago, one of more prominent ways to use a database system is using an external client, using APIs such as ODBC and JDBC.
This allows you to run queries against the database and access the results from within say a Java program.

Here are some useful links:
- [Wikipedia Article](http://en.wikipedia.org/wiki/Java_Database_Connectivity)
- [Another resource](http://www.mkyong.com/java/how-do-connect-to-postgresql-with-jdbc-driver-java/)
- [PostgreSQL JDBC](http://jdbc.postgresql.org/index.html)

The last link has detailed examples in the `documentation` section. The `project3` directory (in the git repository) also contains an example 
file (`JDBCExample.java`) and `project1` directory also has `SQLTesting.java` file. To run the JDBCExample.java file, do:
`javac JDBCExample.java` followed by `java -classpath .:./postgresql-9.0-801.jdbc3.jar JDBCExample`.

Your task to write a JDBC program that will take in JSON updates and insert appropriate data into the database. 
Two types of updates should be supported:
- Status Updates, an example is show below. You can assume that the statustime follows the same format, and you can use `to_date` exactly as used in the `populate.sql` files.
```
{ "statusupdate": {
	"userid": "user1",
	"statustime": "2015-09-25 12:57:13",
	"text": "This is a status update
	}
}
```
- New user, where along with the user information, you also an array of his/her friends. Note that: both links need to be added.
```
{ "newuser": {
	"userid": "user300",
	"name": "XYZ",
	"birthdate": "1991-12-06",
	"joined": "2011-12-06",
	"friends": [
		{"friend_id" : "user0"},
		{"friend_id" : "user100"}
		]
	}
}
```

There are quite a few Java JSON parsing libraries out there to simplify the parsing process.

The provided `JSONProcessing.java` file already takes care of the input part, and you just need to focus on finishing
the `processJSON(String json)` function. An example JSON file is provided: `example.json`.

There may be errors in the updates, and in those cases, your code should print out a helpful error.

### Submission Instructions
We have provided a `answers.docx` file -- fill in your answers to the first 5 question into that doc file (including scanned PDFs or images).
In addition, submit your `JSONProcessing.java` file.

You may want to use some tool (e.g., Google Drawing) to draw query plans.

