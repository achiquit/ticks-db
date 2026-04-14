#!/bin/sh

echo ""
echo ""

echo "=+=+=+=+=+=+=+=--- Updating The DB ---=+=+=+=+=+=+=+="
python3 scripts/add_data.py

echo ""
echo ""

echo "=+=+=+=+=+=+=+=--- Backing up DB to GitHub ---=+=+=+=+=+=+=+="
git commit -a -m "Automatic DB Update"
git push

echo ""
echo ""

echo "=+=+=+=+=+=+=+=--- Sending data to the website directory ---=+=+=+=+=+=+=+="
cat scripts/send-to-website.sql | sqlite3 ticks

cd ../websitejazzhands
./update.sh