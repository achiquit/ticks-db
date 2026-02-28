#!/bin/sh

python3 scripts/add_data.py

echo "Backing up DB to GitHub"
git commit -a -m "Automatic DB Update"
git push

echo "Sending data to the website directory"
cat scripts/send-to-website.sql | sqlite3 ticks

cd ../websitejazzhands
./update.sh