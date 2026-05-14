#!/bin/sh

echo ""
echo ""

echo "=+=+=+=+=+=+=+=--- Updating The DB ---=+=+=+=+=+=+=+="
python3 scripts/add_data.py

echo ""
echo ""

echo "=+=+=+=+=+=+=+=--- Backing up DB to GitHub ---=+=+=+=+=+=+=+="
git add .
git commit -a -m "Automatic DB Update"
git push

echo ""
echo ""

echo "=+=+=+=+=+=+=+=--- Sending data to the website directory ---=+=+=+=+=+=+=+="
cat scripts/db_magic.sql | sqlite3 ticks
python3 scripts/graphs-to-website.py

cd ../websitejazzhands
./update.sh