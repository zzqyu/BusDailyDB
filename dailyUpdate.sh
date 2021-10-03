#!/bin/bash
rm -rf update_*
echo `date` > update_start.txt
git pull
echo `python3 ./BaseDataToDB.py` > update_run.txt
echo "success" > update_end.txt