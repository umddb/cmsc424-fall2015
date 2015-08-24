#!/bin/bash

# This script is modified from the setup script for SaaSBook Image
# https://github.com/saasbook/courseware/blob/master/vm-setup/configure-image-0.10.3.sh

# This script is designed for Ubuntu 12.04
# run with . <filename>.sh

# Get password to be used with sudo commands
# Script still requires password entry during rvm and heroku installs
echo -n "Enter password to be used for sudo commands:"
read -s password

echo -n "Prompt before installing each package? [yes/no] "
read prompt

# Function to issue sudo command with password
function sudo-pw {
    echo $password | sudo -S $@
}

# Start configuration
cd ~/
sudo-pw apt-get update
sudo-pw apt-get upgrade

for i in dkms vim emacs git chromium-browser curl postgresql postgresql-contrib mongodb openjdk-7-jdk sqlite3
do
    if [ "$prompt" = "yes" ]; then
        tput clear; echo "================== INSTALLING " $i " ==== Press Enter to Continue"; read answer 
    fi
    sudo-pw apt-get install -y $i
done


# Install maven
if [ "$prompt" = "yes" ]; then
    tput clear; echo "================== INSTALLING Apache Maven ==== Press Enter to Continue"; read answer 
fi
sudo-pw curl -o /usr/local/apache-maven-3.3.3-bin.zip http://mirror.olnevhost.net/pub/apache/maven/maven-3/3.3.3/binaries/apache-maven-3.3.3-bin.zip
cd /usr/local/
sudo-pw unzip apache-maven-3.3.3-bin.zip
echo 'PATH=/usr/local/apache-maven-3.3.3/bin:$PATH' >> ~/.bashrc
cd ~

# Install sbt (for Spark)
if [ "$prompt" = "yes" ]; then
    tput clear; echo "================== INSTALLING SBT ==== Press Enter to Continue"; read answer 
fi
echo "deb http://dl.bintray.com/sbt/debian /" | sudo tee -a /etc/apt/sources.list.d/sbt.list
sudo-pw apt-get update
sudo-pw apt-get install sbt

#===============================================================================================================
# Install Ruby, Rails, and Gems
# Copied from Heroku Instructions, from: https://raw.githubusercontent.com/railsgirls/installation-scripts/master/rails-install-ubuntu.sh
if [ "$prompt" = "yes" ]; then
    tput clear; echo "================== INSTALLING Ruby on Rails ==== Press Enter to Continue"; read answer 
fi
gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3
curl -L https://get.rvm.io | bash -s stable --rails
source ~/.rvm/scripts/rvm

echo "Installs Ruby"
rvm install 2.2.2
rvm use 2.2.2 --default
echo rvm use 2.2.2 >> ~/.profile

echo "gem: --no-ri --no-rdoc" > ~/.gemrc
gem install bundler
gem install rails

echo -e "\n- - - - - -\n"
echo -e "Now we are going to print some information to check that everything is done:\n"

echo -n "Should be sqlite 3.8.1 or higher: sqlite "
sqlite3 --version
echo -n "Should be rvm 1.26.11 or higher:         "
rvm --version | sed '/^.*$/N;s/\n//g' | cut -c 1-11
echo -n "Should be ruby 2.2.2:                "
ruby -v | cut -d " " -f 2
echo -n "Should be Rails 4.2.1 or higher:         "
rails -v
echo -e "\n- - - - - -\n"

echo "If the versions match, everything is installed correctly. If the versions don't match or errors are shown, something went wrong with the automated process."

#===============================================================================================================
echo "Installing Apache Cassandra -- type Enter to continue"
read dummy
mkdir $HOME/cassandra
cd $HOME/cassandra
curl -O http://www.cs.umd.edu/class/fall2015/cmsc424/apache-cassandra-2.2.0-bin.tar.gz
tar -xvf apache-cassandra-2.2.0-bin.tar.gz
cd -
#cp logback.xml $HOME/cassandra/apache-cassandra-2.1.1/conf/
echo 'export CASSANDRA_HOME="${HOME}/cassandra/apache-cassandra-2.2.0"' >> ~/.profile
echo 'JAVA_HOME="/usr/lib/jvm/java-7-openjdk-i386/jre"' >> ~/.profile
echo 'export PATH=${PATH}:${CASSANDRA_HOME}/bin:${JAVA_HOME}/bin' >> ~/.profile
source ~/.profile
mkdir $CASSANDRA_HOME/data
mkdir $CASSANDRA_HOME/data/commitlog
mkdir $CASSANDRA_HOME/data/data
mkdir $CASSANDRA_HOME/data/saved_caches
cd $HOME

#===============================================================================================================
echo "Installing Apache Spark -- type Enter to continue"
read dummy
mkdir $HOME/spark
cd $HOME/spark
curl -O http://www.cs.umd.edu/class/fall2015/cmsc424/spark-1.4.1-bin-cdh4.tgz
tar -xvf spark-1.4.1-bin-cdh4.tgz
cd $HOME

#===============================================================================================================
# Install Data Science Stuff
echo -n "Install Python and other Data Science packages (these will not be used in the 424 class)? [yes/no] "
read datascience

if [ "$datascience" = "yes" ]; then
	for i in r-base-core python-setuptools python-dev python-pip python-matplotlib ipython-notebook python-numpy  python-pandas python-scipy python-zmq python-jinja2 
	do
		if [ "$prompt" = "yes" ]; then
			tput clear; echo "================== INSTALLING " $i " ==== Press Enter to Continue"; read answer 
		fi
		sudo-pw apt-get install -y $i
	done

	# These have binaries and can be installed through apt-get -- pip install -U numpy pandas ipython jinja2 zmq
	# These don't -- pip install -U scikit-learn tornado
	# Not sure whether we really need: zmq tornado
	if [ "$prompt" = "yes" ]; then
		tput clear; echo "================== INSTALLING scikit-learn ==== Press Enter to Continue"; read answer 
	fi
	pip install -U scikit-learn
fi
