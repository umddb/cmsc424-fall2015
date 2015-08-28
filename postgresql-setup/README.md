### SQL

The goal here is to introduce you to SQL. We will use the open source PostgreSQL database system for this.

#### Setting up PostgreSQL on the virtual machine

PostgreSQL is already installed on your virtual machine. The current version of PostgreSQL is 9.4.4. You will find the detailed documentation at:
http://www.postgresql.org/docs/9.4/interactive/index.html. However, the version installed on the VMs is 9.3.9, the one available through `apt-get`
right now.

Following steps will get you started with creating a database and populating it with the `University` dataset provided on the book website: http://www.db-book.com

   1. You will be using PostgreSQL in a client-server mode. 
   Recall that the server is a continuously running process that listens on a specific port (the actual port would
   differ, and you can usually choose it when starting the server). In order to connect to the server, the client
   will need to know the port. The client and server are often on different machines, but
   for you, it may be easiest if they are on the same machine. 

   Using the **psql** client is the easiest -- it provides
   a commandline access to the database. But there are other clients too. We will assume **psql** here.

   Important: The server should be already started on your virtual machine -- you do not need to start it. However, the following two help pages discuss how to start the
   server: [Creating a database cluster](http://www.postgresql.org/docs/current/static/creating-cluster.html) and [Starting the server](http://www.postgresql.org/docs/current/static/server-start.html)

   2. PostgreSQL server has a default superuser called **postgres**. You can do everything under that
   username, or you can create a different username for yourself. If you run a command (say createdb) without
   any options, it uses the same username that you are logged in under. However, if you haven't created a
   PostgreSQL user with that name, the command will fail. You can either create a user (by logging in as the superuser),
   or run everything as a superuser (typically with the option: **-U postgres**).

   For our purposes, we will create a user with superuser priveledges. **Note: This step is already done on the VMs on Horvitz cluster -- you don't have sudo access on those machines.**

   `sudo -u postgres createuser -s cmsc424`

   3. After the server has started, the first step is to **create** a database, using the **createdb** command.
   PostgreSQL automatically creates one database for its own purpose, called **postgres**. It is preferable 
   you create a different database for your data. Here are more details on **createdb**: 
   http://www.postgresql.org/docs/current/static/tutorial-createdb.html

   We will create a database called **university**.

   `createdb university`

   4. Once the database is created, you can connect to it. There are many ways to connect to the server. The
   easiest is to use the commandline tool called **psql**. Start it by:

   `psql university`

    **psql** takes quite a few other options: you can specify different user, a specific port,
     another server etc. See documentation: http://www.postgresql.org/docs/current/static/app-psql.html

     Note: you don't need a password here because PostgreSQL uses what's called `peer authentication` by default. You would typically need
     a password for other types of connections to the server (e.g., through JDBC).

Now you can start using the database. 
    
   - The psql program has a number of internal commands that are not SQL commands; such commands are often client and database specific. For psql, they begin with the
   backslash character: `\`. For example, you can get help on the syntax of various PostgreSQL SQL commands by typing: `\h`.

   - `\d`: lists out the tables in the database.

   - All commands like this can be found at:  http://www.postgresql.org/docs/current/static/app-psql.html. `\?` will also list them out.

   - To populate the database using the provided university dataset, use the following: `\i DDL.sql`, followed by 

   ```\i smallRelationsInsertFile.sql``` 

   For this to work, the two .sql file must be in the same directory as the one where you started psql. The first command creates the tables, and the
   second one inserts tuples in it. 

   - Create a different database `university_large` for the larger dataset provided (`largeRelationsInsertFile.sql`). Since the table names
   are identical, we need a separate database. This would be needed for the reading homework.

#### University Dataset

The University Dataset is the same as the one discussed in the book, and contains randomly populated information about the students, courses, and
instructors in a university. The schema diagram for the database is as follows:

<img src="university.png"/ width=900>

#### Introduction to SQL

Queries in psql must be terminated with a semicolon. After populating the database, you can test it by 
running simple queries like: 

`select * from department;`

Some resources for SQL:
   - There are numerous online resource. PostgreSQL manual is a good place for introduction to SQL.  http://sqlzoo.net also has many examples.
   - There is also a nice tutorial from [Khan Academy](https://www.khanacademy.org/computing/computer-programming/sql), although it might be too
   basic and simple for you.

#### Example Queries 

Here are some example queries on the University dataset and the SQL for them. There are of course many more queries in the textbook.

   - Report the total number of medals won by M. Phelps over both olympics.

   `select * from course where title like '%Biology%';`

   There are two courses. How many students are enrolled in the first one (ever)?

   `select * from takes where course_id = 'BIO-101';`

   There are two courses. How many students were enrolled in Summer 2009?

   `select * from takes where course_id = 'BIO-101' and year = 2009 and semester = 'Summer';`

   - **Aggregates**: Count the number of instructors in Finance.

   `select count(*) from instructor where dept_name = 'Finance';`

   - Find the instructor(s) with the highest salary.
   
         select * 
         from instructor 
         where salary = (select max(salary) from instructor);
   
       Note that using a nested "subquery" (which first finds the maximum value of the density) as above is the most compact way to write this query.

   - **Joins and Cartesian Product**: To find building names for all instructors, we must do a join between two relations:

           select name, instructor.dept_name, building
           from instructor, department 
           where instructor.dept_name = department.dept_name;

    Since the join here is a equality join on the common attributes in the two relations, we can also just do:

           select name, instructor.dept_name, building
           from instructor natural join department;

    On the other hand, just doing the following will lead to a large number of tuples, most of which are not meaningful:

            select name, instructor.dept_name, building
            from instructor, department;
   

   - `as` can be used to rename tables and simplify queries:
           select distinct T.name
           from instructor as T, instructor as S 
           where T.salary > S.salary and S.dept_name = 'Biology';

      Self-joins (where two of the relations in the from clause are the same) are impossible without using `as`. The following query associates a
      course with the pre-requisite of one of its pre-requisites. There is no way to disambiguate the columns without some form of renaming.

              select p1.course_id, p2.prereq_id as pre_prereq_id 
              from prereq p1, prereq p2 
              where p1.prereq_id = p2.course_id;

     The small database doesn't have any chains of this kind. Let's add one more tuple:

            insert into prereq values ('CS-101', 'PHY-101');

    Now the above query would return some results.
   
   - Create a new table that records the medals for individual sports.

         create table IndividualMedals as
         select r.player_id, e.event_id, medal, result
         from results r, events e
         where r.event_id = e.event_id and is_team_event = 0;
       

   - *Union* operation can be used to combine information from two tables (from Section 3.5.1):

           (select course_id
            from section
            where semester = 'Fall' and year= 2009)
           union
           (select course_id 
            from section
           where semester = 'Spring' and year= 2010);

   - **Aggregation with Grouping** (Section 3.7.2):

            select dept_name, avg(salary) as avg_salary 
            from instructor
            group by dept_name;

    You can use `having` to filter out groups.

            select dept_name, avg(salary) as avg_salary 
            from instructor
            group by dept_name
            having count(*) > 2;


   - **(WITH)**: In many cases you might find it easier to create temporary tables, especially
   for queries involving finding "max" or "min". This also allows you to break down
   the full query and makes it easier to debug. It is preferable to use the WITH construct
   for this purpose. The syntax appears to differ across systems, but here is the link
   to PostgreSQL: http://www.postgresql.org/docs/9.0/static/queries-with.html

   The following query is from Section 3.8.6:

           with max_budget(value) as (
                select max(budget) 
                from department
            )
            select budget
            from department, max_budget 
            where department.budget = max_budget.value;


   - **(LIMIT)** PostgreSQL allows you to limit the number of results displayed which 
   is useful for debugging etc. Here is an example:

   `select * from instructor limit 2;`
