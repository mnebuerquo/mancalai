#!/bin/sh

# Create Python App
# by Mnebuerquo
# https://github.com/mnebuerquo/create-python-app
# Please keep the above link in place if you are using this in your project!

# Use this script to download all the necessary scripts to your project.
# Run it any time to upgrade to the newest version of this tool.
# Happy Pythoning!

RAW="https://raw.githubusercontent.com/mnebuerquo/create-python-app/master/"

# I want to download files from my git repo, but without the .git and stuff.
# This is easiest with just a wget, but it's tedious since I have to
# download each file.

get_executable() {
	wget "$RAW/$1" -O "$1"
	chmod +x "$1"
}

get_file() {
	wget "$RAW/$1" -O "$1"
}

get_executable mn_build
get_executable mn_cpa_install.sh
get_executable mn_image
get_executable mn_lint
get_executable mn_run
get_executable mn_test
get_executable pip
get_executable python

get_file mn_Dockerfile
get_file pytest.ini
get_file flake8.ini

./mn_build
