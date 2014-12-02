#!/bin/bash
#This script compare the difference between the log files and the summary files and create a readable report.

echo "#############################################################################################"
echo "#                             Checking test results for test Back End                       #"
echo "#############################################################################################"
echo "---------------------------------------------------------------------------------------------"
echo "                              Checking summary files of test Back End"
echo "---------------------------------------------------------------------------------------------"
diff -iwsB outputsBackEnd/"$now"/MasterAccountFile.txt outputsBackEnd/expected/MasterAccountFile.txt #Check the diff between the summary files
echo "---------------------------------------------------------------------------------------------"
echo "                                Checking log files of test Back End"
echo "---------------------------------------------------------------------------------------------"
diff -iwBs outputsBackEnd/"$now"/log.txt outputsBackEnd/expected/log.txt #Check the diff between the log files
echo "\n"