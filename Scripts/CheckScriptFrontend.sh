#!/bin/bash
#This script compare the difference between the log files and the summary files and create a readable report.
k=1
for i in inputs/input* #For every input file in inputs folder
do
	echo "#############################################################################################"
	echo "#                             Checking test results for test "$k"                             #"
	echo "#############################################################################################"
	echo "---------------------------------------------------------------------------------------------"
	echo "                              Checking summary files of test "$k""
	echo "---------------------------------------------------------------------------------------------"
	diff -iwsB outputs/"$now"/sum"$k".txt outputs/expected/sum"$k".txt #Check the diff between the summary files
	echo "---------------------------------------------------------------------------------------------"
	echo "                                Checking log files of test "$k""
	echo "---------------------------------------------------------------------------------------------"
	diff -iwBs outputs/"$now"/log"$k".txt outputs/expected/log"$k".txt #Check the diff between the log files
	echo "\n"
	k=$((k+1))
done