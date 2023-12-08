#! /bin/sh
# Description: This script is used to manage the version control system.

git add .
git commit -m "AT $(date +%Y-%m-%d-%H-%M-%S) BY $(whoami)"
git push heroku master
git push github

# End of file