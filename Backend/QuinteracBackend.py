import sys
import argparse

#Quinterac Back Office reads in the previous day's master accounts file and
#Then applies all of the transactions in a set of daily transaction files to
#The accounts to produce today's new master accounts file. Because transactions
#May also open or close new accounts, it also produces a new valid accounts
#list for tomorrow's Front End runs.

#Use preferably Python2.7. To use the software, you need the files "OldMasterAccountFile" 
#& "SummaryTransactionFile.txt" 
#To call the software just type "python QuinteracBackEnd.py -m SummaryTransactionFile.txt -a OldMasterAccountFile"
#You can obtain help by typing "python2.7 QuinteracBackEnd.py --help"

#Written by :
#Bastien Escaich 10162797
#Peter Ju 10072884

###############################################################################################
#LISTS RELATED METHODS
###############################################################################################

def fileToList(File, Limit): #Get a file a split limit and return a 2D list
	File = open(File, "r") #Open the file
	List = list()
	for Line in File: #Read the file line by line
		Line = Line.split(" ",Limit) #Split the Line until the limit, the limit allow to keep the name as a single string
		if Line:
			List.append(Line)
	File.close()

	return List

def accountList(OldMasterAccountList): #Get the MasterAccountList and generate the ValidAccountList out of it.
	ValidAccountList=list()
	j=0
	for Line in OldMasterAccountList:
		ValidAccountList.append(OldMasterAccountList[j][0]) #Get only the valid account numbers
		j+=1
	return ValidAccountList 

###############################################################################################
#SECURITY CHECKS
###############################################################################################

def checkNegative(Line, Summary): #Returns True if the balance becomes negative, False else
	if int(Line[1]) - int(Summary[3]) < 0:
		return True
	else:
		return False

def accountExists(AccountList, AccountNumber): #Returns True if the AccountNumber is in the ValidAccountList
	if AccountNumber in AccountList:
		return True
	else:
		return False #Else, returns False

###############################################################################################
#TRANSACTIONS METHODS
###############################################################################################

def deposit(OldMasterAccountList, Summary, ValidAccountList): #Deposit Method
	if accountExists(ValidAccountList, Summary[1]) == True:
		for Line in OldMasterAccountList:
			if Summary[1] == Line[0]:
				if int(Summary[3]) + int(Line[1]) > 99999999:
					print "Failed / Amount over the limit"
				else:
					Line[1] = str(int(Summary[3]) + int(Line[1])).zfill(8) #Sum the old balance and the deposit amount
					print Line[1]
					print "Success"
	else:
		print "Failed / Account doesn't exist"

def withdraw(OldMasterAccountList, Summary, ValidAccountList): #Withdraw Method
	if accountExists(ValidAccountList, Summary[1]) == True:		
		for Line in OldMasterAccountList:
			if Summary[1] == Line[0]:
				if checkNegative(Line, Summary) == True:
					print "Failed / Account with negative balance"
				else:		
					Line[1] = str(int(Line[1]) - int(Summary[3])).zfill(8) #Do the maths to get the new balance and replace it in the array
					print Line[1]
					print "Success"
	else:
		print "Failed / Account doesn't exist"

def transfer(OldMasterAccountList, Summary, ValidAccountList): #Transfer Method
	if accountExists(ValidAccountList, Summary[1]) == True & accountExists(ValidAccountList, Summary[2]) == True:	
		for Line in OldMasterAccountList:
			if Summary[1] == Line[0]:			
				Line[1] = str(int(Summary[3]) + int(Line[1])).zfill(8) #Basically a deposit operation
				print Line[1]
				print "Success"

		for Line in OldMasterAccountList:
			if Summary[2] == Line[0]:
				if checkNegative(Line, Summary) == True:
					print "Failed / Account with negative balance"
				else:		
					Line[1] = str(int(Line[1]) - int(Summary[3])).zfill(8) #Basically a withdraw operation
					print Line[1]
					print "Success"
	else:
		print "Failed / Account doesn't exist"

def create(OldMasterAccountList, Summary, ValidAccountList): #Create Method
	if accountExists(ValidAccountList, Summary[1]):
		print "Failed / Account already exists"
	else:
		if Summary[3] == '00000000':
			ValidAccountList.append(Summary[1]) #Add the new account to the ValidAccountList
			NewAccount = Summary[1] + " " + Summary[3] + " " + Summary[4] #Format the new account's information
			NewAccount = NewAccount.split(" ", 2) #Format the new account's information
			OldMasterAccountList.append(NewAccount) #Add the new account the Master Account list
			print "Success"
		else: 
			print "Failed / Amount is not 0"

def delete(OldMasterAccountList, Summary, ValidAccountList): #Delete Method
	Name = False
	if accountExists(ValidAccountList, Summary[1]) == True:
		for Line in OldMasterAccountList:
			if Summary[4] == Line[2]:
				Name = True
				if Line[1] == '00000000': #Verify that the amount is 0
					ValidAccountList.remove(Summary[1]) #Remove the old account to the ValidAccountList
					DeletedAccount = Summary[1] + " " + Summary[3] + " " + Summary[4] #Format the old account's information
					DeletedAccount = DeletedAccount.split(" ", 2) #Format the old account's information
					OldMasterAccountList.remove(DeletedAccount) #Remove the old account the Master Account list
					print "Success"
				else:
					print 'Failed / Amount not zero'
		if Name == False:
			print 'Failed / Names do not match'
	else: 
		print 'Failed / Account doesn\'t exist'

def writeFile(Filename, List, Bool): #Get a list and a filename and write the content of the list in the file, line by line
	File = open(Filename,'w')
	for Line in List:
		if Bool == False: #The List is a 1D list
			if Line:
				File.write("%s\n" % Line)
		else: #The List is a 2D list
			if Line:
				AccountLine = Line[0] + ' ' + Line[1] + ' ' + Line[2]
				File.write("%s" % AccountLine)

###############################################################################################
#MAIN METHOD
###############################################################################################

def main():
	parser = argparse.ArgumentParser()#Parser to parse the different following arguments
	parser.add_argument('-m', dest='merged', help='merged transaction summary file', required=True)
	parser.add_argument('-a', dest='account', help='old master account file', required=True)
	parser.add_argument('-o', dest='output', help='output directory', required=True)

	args = parser.parse_args()
	MergedSummaryTransactionFile = args.merged
	OldMasterAccountFile = args.account
	OutputFile = args.output

	OldMasterAccountList = fileToList(OldMasterAccountFile, 2)
	MergedSummaryTransactionList = fileToList(MergedSummaryTransactionFile, 4)
	ValidAccountList = accountList(OldMasterAccountList)

	for Summary in MergedSummaryTransactionList:
		if Summary[0] == "01": #Deposit
			deposit(OldMasterAccountList, Summary, ValidAccountList)
		elif Summary[0] == "02": #Withdraw
			withdraw(OldMasterAccountList, Summary, ValidAccountList)
		elif Summary[0] == "03": #Transfer
			transfer(OldMasterAccountList, Summary, ValidAccountList)
		elif Summary[0] == "04": #Create
			create(OldMasterAccountList, Summary, ValidAccountList)
		elif Summary[0] == "05": #Delete
			delete(OldMasterAccountList, Summary, ValidAccountList)
		elif Summary[0] == "00": #EndOfSession
			ValidAccountList = accountList(OldMasterAccountList)
			writeFile(OutputFile, OldMasterAccountList, True)
			writeFile('ValidAccountFile.txt', ValidAccountList, False)
			sys.exit()

if __name__ == "__main__":
    main()