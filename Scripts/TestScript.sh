#!/bin/bash

#This script runs a bench of tests to check the robustness of the QuinteracTest.py software
#The test inputs are stored in inputs/ as well as the valid account files for each test
#The test expected outputs are stored in outputs/expected
#Each run of this script create a new directory were the outputs will be stored

now=$(date +%F-%H%M%S) #Get the current date and format it.
j=1 #Counter used for the test numbers
for i in inputs/input* #For every input file in inputs folder
do
	echo "running test $i"
	mkdir -p outputs/"$now" #Create the new folder with the date, to keep tracking of the results
	python QuinteracTest.py -i "$i" -s outputs/"$now"/sum"$j".txt -a inputs/acc"$j".txt > outputs/"$now"/log"$j".txt #Run the sofware and output in a log file
	j=$((j+1))
done

export now #Export now to use it in the CheckScript
sh ./CheckScript.sh