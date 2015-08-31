# Lab 0

---

## Computing Environment

Over the course of the semester, you will work with a variety of software packages, including PostgreSQL, Apache Spark, Apache Cassandra, Ruby on Rails, and others. 
Installing those packages and getting started can often be a hassle, because of software dependencies. You have three choices.

* Install the different software packages on your own machine (most of these packages should have tutorials to install them on different OSs). If you have a linux and Mac, this should be possible; it may be more difficult with Windows. In any case, we would likely not be able to help you with any problems.
* Use Virtual Box (as discussed below). We have provided an image for you to download that contains some of the basic software (or you can do it yourself directly). If you have a reasonably modern machine, VirtualBox should generally work fine, but with older laptops, the performance may not be as good. This is the recommended approach.
* Use a VM in the CS Departments Horvitz Cluster (as discussed below). You would only be able to connect through ssh (unless you want to set up X on your machine). **Make sure to take backups of all your data on those VMs (e.g., you can use `git` as discussed below). You should be prepared for those virtual machines to be removed.**
 
### Virtual Box

[Virtual Box](https://www.virtualbox.org/) is a virtualization software package (similar to VMWare or Parallels). We will use it to create a work environment for you to
complete assignments. We will provide an image with latest Ubuntu Linux, with many of the required packages pre-installed.

You are welcome to set up an environment on your own machine, but we won't be able to support it or help you with it. 

- Download and Install Virtual Box on your machine. 
- **Option 1:** 
    - Download the virtual image at: [Virtual Image](http://www.cs.umd.edu/class/fall2015/cmsc424/CMSC424.ova) (**Warning**: This is a 2.7GB file)
    - Start Virtual Box
    - From the main menu, do "Import Appliance", and point at the OVA file that you have downloaded
    - The username and password are both "terrapin"
    - Press Start
    - **Tip:** On Macs, if the Command-Tab stops working, press Command by itself once, and then try Command-Tab again (the first "Command" makes the virtual machine release the keyboard)
    - Move on to **Confirm Things Work** below
- **Option 2:** It is not particularly complicated to recreate the above virtual image yourselves, but we likely won't be able to help you if you
run into problems. Here are the steps we followed:
    - Download the latest Ubuntu ISO from http://www.ubuntu.com/download/desktop. We used the 64-bit version.
    - Create a new virtual machine with options: Type = Linux, Version = Ubuntu (64 bit). 
    - Recommended memory size: 2GB (you would want at least 1GB)
    - Select: "Create a Virtual Hard Drive Now". 
        - Leave the setting for Hard Drive File Type unchanged (i.e., VDI). 
        - Set the hard drive to be "Dynamically Allocated".
        - Size: 20GB (approximately)
    - The virtual machine is now created. 
    - Press "Start"
        - On the screen asking you to select a virtual optical disk file: Navigate to the Ubuntu ISO that you have downloaded, and Press Start.
        - On the Boot Screen: "Install Ubuntu"
        - Deselect both of "Download Updates while Installing" and "Install Third-Party Software"
        - **Tip:** On Macs, if the Command-Tab stops working, press Command by itself once, and then try Command-Tab again (the first "Command" makes the virtual machine release the keyboard)
        - Press Continue
        - Select "Erase disk and install Ubuntu"
        - Who are you?
            - Name = "Terrapin"; username = "terrapin"; password = "terrapin"; 
            - Select "Log In Automatically"
        - Go get a coffee !!
        - Press "Restart Now"
    - If you are having trouble getting the machine to restart, the problem is likely the boot order. 
        - Go to the Virtual Box Window 
        - Power Off the machine (right click the machine name -- the option is under "Close")
        - Go to "Settings" (under "Machine")
        - Under "System --> Motherboard", you will see the boot order. Deselect CD/DVD, and Press Okay.
        - Press Start again.
    - Hopefully the machine starts now. 
    - Open a Terminal. 
        - Get the setup script: `wget http://www.cs.umd.edu/class/fall2015/cmsc424/setup-script.sh`
        - Make it executable: `chmod +x setup-script.sh`
        - Run it: `./setup-script.sh`
            - Password: terrapin (unless you used a different password)
            - Say "yes" if you want to be prompted for each package install
    - **Note: You will likely not be able to resize the virtual machine window. After the setup script has finished executing, click on `Devices -> Insert Guest Additions...`, and follow the instructions to install the Guest Additions (the password is 'terrapin' as above). Restart the machine. Now you should be able to resize the window.**

- Confirm things work:
    - **java**: Run `javac` and `java -version` to ensure the programs are running

    - **Git**: See below for more details

    - **sqlite3**: 

        SQLite is an "embedded" SQL database (it doesn't depend on a dedicated server process;  instead the client just manipulated a stored
        datbase file directly.)

        To ensure it is installed, type `sqlite3` and verify that you see the following:

        ```
        SQLite version 3.8.2 2013-12-06 14:53:30
        Enter ".help" for instructions
        Enter SQL statements terminated with a ";"
        sqlite>
        ```

        If you do, push `ctrl+d` to exit the prompt.

    - **PostgreSQL**: PostgreSQL is a full-fledged and powerful relational database system, and will be used for several assignments. 
        To ensure it is installed, try `sudo -u postgres psql` and verify that you see the following:

	```
	psql (9.3.9)
	Type "help" for help.

	postgres=# 
	```
        If you do, push `ctrl+d` to exit the prompt.

	If you wish, you can follow the initial instructions in the SQL assignment (Project 1) to set up a proper database (you have to do that for the first reading assignment anyway).

    - **Ruby and Rails**: You may have to `source .bash_profile` if these are not being found.
    	- Try `rvm --version | sed '/^.*$/N;s/\n//g' | cut -c 1-11`: It should be rvm 1.26.11 or higher.
	- Try `ruby -v | cut -d " " -f 2`: It should be ruby 2.2.2.
	- Try `rails -v`: It should be Rails 4.2.1 or higher.


    - **Apache Spark**: Spark is a distributed cluster programming framework for large data processing tasks. We will cover it later. Try: `~/spark/spark-1.4.1-bin-cdh4/bin/spark-shell` and verify that you see the following:
    ```
    Welcome to
    ____              __
    / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
    /___/ .__/\_,_/_/ /_/\_\   version 1.4.1
    /_/
    Using Scala version 2.10.4 (OpenJDK 64-Bit Server VM, Java 1.7.0_79)
    Type in expressions to have them evaluated.
    Type :help for more information.
    Spark context available as sc.
    SQL context available as sqlContext.

    scala> 
    ```
    If you do, push `ctrl+d` to exit the prompt.

    - **Apache Cassandra**: Finally, Cassandra is a key-value store that we will cover later. Open another terminal tab and try: `cassandra -f`. This should print out a bunch of information and start the Cassandra server. As above, you may have to do `source .bash_profile` so that the shell finds these commands.

    In another terminal tab, try `cqlsh` and verify that you see the following output:
    ```
    Connected to Test Cluster at 127.0.0.1:9042.
    [cqlsh 5.0.1 | Cassandra 2.2.0 | CQL spec 3.3.0 | Native protocol v4]
    Use HELP for help.
    cqlsh>
    ```

---

### Using a VM in the CS Horvitz Cluster

The above is the preferred approach for you to set up the computing environment. But if for any reasons you are not able to set up a VM as above, we have
a few VMs running in the CS Horvitz Cluster. The VMs are also running Ubuntu, with the same software pre-installed as the provided VirtualBox image. However, 
you will have to use those through `ssh`, and you would not be able to run Firefox, etc., there (at least not without some effort).

The IP addresses, usernames, and passwords are different for different VMs, and will be provided as requested.  

After connecting, make sure all the software is running as discussed above. You don't have `sudo` access on these VMs, so some of the commands above
may not work (e.g., for PostgreSQL, just try `createdb university` followed by `psql university` instead).

---

## Git & Github

Git is one of  the most widely used version control management system today, and invaluable when working in a team. Github is a web-based hosting service built around Git --
it supports hosting git repositories, user management, etc. There are other similar services, e.g., bitbucket.

We will use Github to distribute the assignments, and other class materials. Our use of git/github for the class will be minimal; however, we encourage you to use it for
collaboration for your class project, or for other classes. 

Repositories hosted on github for free accounts are public; however, you can easily sign up for an educational account which allows you to host 5 private repositories. More
details: https://education.github.com/

- Create an account on Github: https://github.com
- Generate and associate an SSH key with your account
    - Instructions to generate SSH Keys: https://help.github.com/articles/generating-ssh-keys#platform-linux
        - Make sure to remember the passphrase
    - Go to Profile: https://github.com/settings/profile, and SSH Keys (or directly: https://github.com/settings/ssh)
    - Add SSH Key
- Clone the class repository:
    - In Terminal: `git clone git@github.com:umddb/cmsc424-fall2015.git`
    - The master branch should be checked out in a new directory 
- Familiarize yourself with the basic git commands
    - At a minimum, you would need to know: `clone`, `add`, `commit`, `push`, `pull`, `status`
    - But you should also be familiar with how to use **branches**
