## Project 2: Web Development with Ruby on Rails, CMSC424, Fall 2015

**This assignment is to be done by yourself, but you are welcome to discuss the assignment with others.**

The goal of this project is to learn how Web Application Frameworks like Ruby-on-Rails work, and
how they interact with the underlying data store. We will be providing you with a skeleton code, and 
describe a set of files that you need to modify. There are two final deliverables for the assignment:

* An Entity-Relationship diagram for the scenario described below, and the corresponding relational schema
* Your modified Ruby-on-Rails files 

We will copy your files onto our installation, and run it, to confirm that it works.

### Getting Started
Although we will provide skeleton code to get started, you might benefit from going through a tutorial on Ruby-on-Rails.
There are several such tutorials on the web -- [Rails for Zombies](http://railsforzombies.org) provides a nice
interactive overview, whereas the [Rails Getting Started Guide](http://guides.rubyonrails.org/getting_started.html) is 
also pretty accessible.

We have created two web apps for you to get started. Both are present in the `project2` directory on the git repository.
The `blog` webapp is the result of the Getting Started Guide from above, whereas the `grading` webapp is for you 
to get started with the project itself. See below for more details.

### Application Scenario
The goal of the web application development project is to build an end-to-end application 
that has a web frontend, and a database backend.  The application scenario is that of handling 
homework assignments/quizzes for courses (somewhat similar to the ELMS functionality).
Although there are quite a few tools out there for this purpose today, we picked this scenario given 
you are well-familiar with the setting.

We will keep things simple. We will not worry about different departments, semesters, and also not worry about having users logged in (more
on that below). The following is a list of entities that you should start with. You would need to figure out how to model 
the assignments, questions within those, student answers, etc.
- **Students** who are taking the course. A student may take multiple courses that are being administered by the system. 
- **Instructors**  for the course. This includes both professors and TAs. As above, an instructor may teach multiple courses.
- **Courses:**  Standard information about courses (title, description, etc.) should be maintained.
- **Assignments:** A course will have many different assignments, each consisting of several questions. Assignments have due dates.
- **Questions:** The answer to a question may be of different types, e.g., question may be a multiple choice,
the answer may be a single word or a paragraph etc. See <a
href=https://support.google.com/docs/bin/answer.py?hl=en&answer=140941&topic=20322&ctx=topic>Google forms options</a> for some ideas. Your design 
should support at least paragraph answers and multiple choice answers. 

Feel free to add more entities if you'd like.

To keep things simple and with the goal to get an application built, we will not worry about having users logged in, and doing different things for different users etc.
The following describes the main webpages that one would see when starting the app (i.e., when loading the website at `http://localhost:3000`, the default address used by Rails).

- **Main**: The main webpage would contain a list of instructors and a list of students, all clickable. Clicking on an instructor would take you to the Instructor page for that instructor, and clikcking on a student will get you to the Student page.
- **Instructor Page**: This page would show all the courses for the instructor, and for each course, it would show a link to "Grade Submissions", and "Create New Assignment".
- **Grade Submissions**: This page would show links to all the available student submissions to grade (across all assignments for that course). 
Clicking on any one of them would take me to the another page that allows me to grade (Question-by-Question grading is fine). You can decide how you want the interaction to go beyond this.
- **Student Page**: This works similarly. The main page would show all the available assignments across all courses for the student (whose due dates aren't past), and 
clicking on any one of them would allow the student to start answering the question (again Question-by-Question answering is fine, where the student has to click next to go the next question etc).
The interface should allow editing the submission (as long as the due date isn't past).
The main student page would also have a section with current scores for all previously submitted assignments. This could be simple -- a table with course+assignment information, and the score.
- **Create New Assignment**: This page would alllow the instructor to create a new assignment for the course, by adding questions, etc.

To elaborate on a point above: typically you would want to do some authorizations to separate out the different functionality. This is easy to add by having users, and using `sessions`. We will not worry about it for now. Our focus is on designing the E/R model and the schema, and understanding how to use Ruby-on-Rails.

### Heroku (Optional)
If you are interested in publishing your app, you can try Heroku.
[Heroku](http://www.heroku.com) is one of the easiest ways to host your app in the Cloud. You will need to sign up (the free stuff is enough to get started -- I don't believe they ask for credit card information, but be very careful if you do that).

[Heroku Ruby](https://devcenter.heroku.com/articles/getting-started-with-ruby#introduction) getting started guide discusses how to set up a basic RoR app using Heroku. Note that: Heroku requires you to use PostgreSQL (and doesn't work with SQLite which is default for Rails). So it takes a little bit of work to get started with it (and possibly installation of more stuff).

### Skeleton Code and Files to be Modified

We have created the app in rails, and constructed the three entities for you (Students, Instructors, Courses). We have set up the basic webpages to show a list of all instructors, a list of all instructors, and a list of all courses as separate webpages, with links from the main page (you shouldn't need the one about courses since those are always accessed through students or instructors). The latter two are currently empty and your first task should be create those from the instructors webpages.

You will have to create additional models (and controllers and views) for the other entities in your entity relationship model, and also have to set up the associations between them appropriately. You have to submit the entire source code for your app (as a zip file), along with E/R model (as a PDF).

Make sure to look through the ActiveRecord guides to understand how to set up relationships between the entities, and how to access entities from other related entities (e.g., how to get information for all courses taught by an instructor, etc.).
