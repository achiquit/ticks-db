#!/bin/sh

python3 scripts/add_data.py

echo "Updating github"
git commit -a -m "Automatic DB Update"

echo "Sending data to the website directory"