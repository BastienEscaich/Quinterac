import sys
import argparse
import string
import os.path

#Front End of Quinterac banking system. A retail banking transaction acceptor for simple
#Interac-style banking trasaction. This software runs as a console application and uses
#text and text file input/output only.

#The software reads in a list of valid account numbers, processes a stream of transactions
#one at a time and writes out a summary file of transactions at the end of the day.

#Use preferably Python2.7. To use the software, you need the file "ValidAccountFile.txt"
#To call the software just type "python2.7 Quinterac.py -i test.txt -s SummaryTransactionFile.txt"
#You can obtain help by typing "python2.7 Quinterac.py --help"

#Written by :
#Bastien Escaich 10162797
#Peter Ju 10072884

#TODOs

#Modify the program to handle test text file

###############################################################################################
#GLOBAL VARIABLES
###############################################################################################

i=0

###############################################################################################
#SUMMARYLINE METHOD
###############################################################################################

#Create the summary transaction line according to the specifications and return it.
#Returns SummaryTransactionFile
def summaryLine(Operation, AccountNumberTo, AccountNumberFrom, AmountNumber, AccountName):
    SummaryTransactionLine = Operation + ' ' + AccountNumberTo + ' ' + AccountNumberFrom + ' ' + AmountNumber + ' ' + AccountName
    return SummaryTransactionLine 

###############################################################################################
#INPUT METHOD
###############################################################################################

#Special implementation to read the file line by line instead of using raw_input like in Quinterac.py
def Input(Text, InputFile):
	global i #Global variable which count the number of times the function Input is called
	j=0
	file = open(InputFile, 'r')
	for line in file:
		if (i == j):
				i = i + 1
				print (Text)
				print line.replace("\n", "")
				return line.replace("\n", "")
		j = j + 1


################################################################################################
#INPUT VERIFICATION METHODS
################################################################################################

#Check if account number is valid (int, length and already existing)
#Returns boolean
def checkAccount(AccountNumber, ValidAccountList):
    try:
        val = int(AccountNumber) #Check if the number is an int
    except ValueError:
        print("The number you entered is invalid / Not an int")
        return False
    if(len(AccountNumber)!=6): #Check if the length of the account number is 6.
        print("The number you entered is invalid / The account number should be 6 digits")
        return False
    if(AccountNumber+'\n' not in ValidAccountList): #Check if the account number exists in the list
        print("This account number doesn't exist")
        return False

#Check if the amount entered is valid (int, limitation according to login mode)
#Returns boolean
def checkAmount(AmountNumber, LoginMode):
    try:
        val = int(AmountNumber)
    except ValueError:
        print("The number you entered is invalid / Not an int")
        return

    if LoginMode == 'retail': 
		if (len(AmountNumber)>6):
			print("The number you entered is invalid / Amount above $1,000.00")
			return False
		elif (AmountNumber < '0'):
			print("The number you entered is invalid / Negative Amount")
			return False
		elif ((AmountNumber.zfill(6)) > '100000'): #If amount entered is above $1,000.00
			print("The number you entered is invalid / Amount above $1,000.00")
			return False
		else:
			print ('Amount accepted')	
			return True

    elif LoginMode == 'agent':
        if (AmountNumber < '0'):
            print("The number you entered is invalid / Negative Amount")
            return False
        elif (len(AmountNumber)>8): #If amount entered is above $9,999.99
			print("The number you entered is invalid / Amount above $9,999.99")
			return False
        else:
			print ('Amount accepted')	
			return True

#Check if the name is not more than 15 characters
#Returns Boolean
def checkName(AccountName):
    if (len(AccountName)>15): 
        print("The name you entered is too long")
        return False

################################################################################################
#TRANSACTIONS METHODS
################################################################################################

#Allow the user to create an account, ask for account number and name
#Returns SummaryTransactionLine
def create(ValidAccountList, InputFile):
    print("\nCreate an account")

    AccountNumber = Input('Account number >> ', InputFile)
    try:
        val = int(AccountNumber) #Check if the number is an int
    except ValueError:
        print("The number you entered is invalid / Not an int")
        return
    if (len(AccountNumber)!=6): #Check if the length of the account number is 6.
        print("The number you entered is invalid")
    	return
    if (AccountNumber+'\n' in ValidAccountList): #Check if the account number exists in the list
        print("This account number is not valid / Account already exists")
        return

    AccountName = Input('Account Name >> ', InputFile)
    CheckName = checkName(AccountName)
    if CheckName == False: #If the name is not valid, return to main
        return

    SummaryTransactionLine = summaryLine('04', AccountNumber, '000000', '00000000', AccountName.ljust(15))
    print ('Account created!')	
    return SummaryTransactionLine

#Allow the user to delete an account, ask for account number and name
#Returns ValidAccountList, SummaryTransactionLine
def delete(ValidAccountList, InputFile):
    print("\nDelete an account")

    AccountNumber = Input('Account number >> ', InputFile)
    CheckNumber = checkAccount(AccountNumber, ValidAccountList)
    if CheckNumber == False: #If the number is not valid, return to main
        return ValidAccountList, None

    AccountName = Input('Account Name >> ', InputFile)
    CheckName = checkName(AccountName) 
    if CheckName == False: #If the name is not valid, return to main
        return ValidAccountList, None

    SummaryTransactionLine = summaryLine('05', AccountNumber, '000000', '00000000', AccountName.ljust(15))
    print ('Account deleted!')	
    ValidAccountList.remove(AccountNumber +'\n') #Remove the account number from the ValidAccountList, so that it won't be usable for any transaction

    return ValidAccountList, SummaryTransactionLine

#Allow the user to deposit money, ask for an account number and a deposit amount
#Returns SummaryTransactionLine
def deposit(LoginMode, ValidAccountList, InputFile):
    print("\nDeposit")

    AccountNumber = Input('Account number >> ', InputFile)
    CheckNumber = checkAccount(AccountNumber, ValidAccountList)
    if CheckNumber == False:
        return None

    DepositAmount = Input('Amount you want to deposit >> ', InputFile)
    CheckAmount = checkAmount(DepositAmount, LoginMode)

    if CheckAmount == False:
        return None
    elif CheckAmount == True:
        SummaryTransactionLine = summaryLine('01', AccountNumber, '000000', DepositAmount.zfill(8), '000000000000000')
        print ('Deposit successful!')
        return SummaryTransactionLine

#Allow the user to withdraw money, ask for an account number and a withdraw amount
#Returns SummaryTransactionLine, WithdrawTotalAmount 
def withdraw(LoginMode, ValidAccountList, WithdrawTotalAmount, InputFile):
    print("\nWithdraw")

    AccountNumber = Input('Account number >> ', InputFile)
    CheckNumber = checkAccount(AccountNumber, ValidAccountList)
    if CheckNumber == False:
        return None, WithdrawTotalAmount

    WithdrawAmount = Input('Amount you want to withdraw >> ', InputFile)
    CheckAmount = checkAmount(WithdrawAmount, LoginMode)

    
    if CheckAmount == False:
        return None, WithdrawTotalAmount
    elif CheckAmount == True:
    	if LoginMode == 'agent':
    		SummaryTransactionLine = summaryLine('02', AccountNumber, '000000', WithdrawAmount.zfill(8), '000000000000000')	
    		print ('Withdraw successful!')	
        	return SummaryTransactionLine, WithdrawTotalAmount
    	elif (AccountNumber in WithdrawTotalAmount):
    		print AccountNumber
    		if ((int(WithdrawTotalAmount[AccountNumber]) + int(WithdrawAmount)) > 100000):
    			print ('Withdraw rejected / Total withdraw amount above $1.000,00')
    			return None, WithdrawTotalAmount
    		else:
    			WithdrawTotalAmount[AccountNumber] = int(WithdrawAmount) + int(WithdrawTotalAmount[AccountNumber])
    			SummaryTransactionLine = summaryLine('02', AccountNumber, '000000', WithdrawAmount.zfill(8), '000000000000000')	
    			print ('Withdraw successful!')
    			return SummaryTransactionLine, WithdrawTotalAmount
    	else:
    		WithdrawTotalAmount.update({AccountNumber: WithdrawAmount})
    		SummaryTransactionLine = summaryLine('02', AccountNumber, '000000', WithdrawAmount.zfill(8), '000000000000000')
    		print ('Withdraw successful!')	
    		return SummaryTransactionLine, WithdrawTotalAmount

#Allow the user to transfer money, ask for a 'to' account number, a 'from' account number and a transfer amount
#Returns SummaryTransactionLine
def transfer(LoginMode, ValidAccountList, InputFile):
    print("\nTransfer")

    AccountNumber = Input('Account number to >> ', InputFile)
    CheckNumber = checkAccount(AccountNumber, ValidAccountList)
    if CheckNumber == False:
        return None

    AccountNumber2 = Input('Account number from >> ', InputFile)
    CheckNumber = checkAccount(AccountNumber2, ValidAccountList)
    if CheckNumber == False:
        return None

    TransferAmount = Input('Amount you want to transfer >> ', InputFile)
    CheckAmount = checkAmount(TransferAmount, LoginMode)
    
    if CheckAmount == False:
        return None
    elif CheckAmount == True:
        SummaryTransactionLine = summaryLine('03', AccountNumber, AccountNumber2, TransferAmount.zfill(8), '000000000000000')
        print ('Transfer successful!')
        return SummaryTransactionLine

###############################################################################################
#LOGIN / LOGOUT METHODS
###############################################################################################

#Open a new session and ask for the login mode. 
#Returns ValidAccountList and LoginMode    
def login(InputFile, ValidAccountFile, SummaryTransactionFile): 
    LoginMode = Input('username: (agent or retail - quit to exit software) >> ', InputFile)
    if LoginMode == 'retail':
        print 'login successful / retail mode'
    elif LoginMode == 'agent':
        print 'login successful / agent mode: all transactions possible'
    elif LoginMode == 'quit':
    	print 'Quit'
    	if (os.path.exists(SummaryTransactionFile)):
    		sys.exit()
    	else:
    		with open(SummaryTransactionFile, 'w') as File:
    			File.write("\n")
			sys.exit()
    elif not LoginMode:
    	print 'Quit'
    	if (os.path.exists(SummaryTransactionFile)):
    		sys.exit()
    	else:
    		with open(SummaryTransactionFile, 'w') as File:
    			File.write("\n")
			sys.exit()
    else:
        print "login refused / please enter the login again"
        main()
    
    ValidAccountFile = open(ValidAccountFile, "r") #Read the ValidAccountFile.txt
    ValidAccountList=list()
    for Line in ValidAccountFile: #Read the file line by line
        ValidAccountList.append(Line) #Store each line as an item of a list
    ValidAccountFile.close()

    return ValidAccountList, LoginMode

#Write the SummaryTransactionFile.txt and call the main to prompt for login
def logout(SummaryTransactionList, SummaryTransactionFile):
    SummaryTransactionList.append(summaryLine('00', '000000', '000000', '00000000', '000000000000000'))
    with open(SummaryTransactionFile, 'w') as File:
        for SummaryLine in SummaryTransactionList:
        	if SummaryLine:
        		File.write("%s\n" % SummaryLine)

	sys.exit()

##############################################################################################
#MAIN METHOD
##############################################################################################

#main function of the suftware all the others functions are called from here.
def main():
	parser = argparse.ArgumentParser()#Parser to parse the different following arguments
	parser.add_argument('-i', dest='input', help='input file', required=True)
	parser.add_argument('-s', dest='summary', help='summary file', default='SummaryTransactionFile.txt')
	parser.add_argument('-a', dest='account', help='valid account file', required=True)
	args = parser.parse_args()
	InputFile = args.input
	SummaryTransactionFile = args.summary
	ValidAccountFile = args.account

	ValidAccountList, LoginMode=login(InputFile, ValidAccountFile, SummaryTransactionFile)
	Operation=True
	WithdrawTotalAmount = {}
	SummaryTransactionList = list()

	while Operation: #Menu to select the operation
		print ("""
		1.Create an account
		2.Delete an account
		3.Deposit
		4.Withdraw
		5.Transfer
		6.Logout
		""")
		Operation=Input("What would you like to do? ", InputFile) 
		if Operation=="create":
			if LoginMode == 'retail':
				print("\nOperation not permitted") #Check if retail doesn't have access to create function
			elif LoginMode == 'agent':
				SummaryLine = create(ValidAccountList, InputFile)
				SummaryTransactionList.append(SummaryLine) #Add the summary line to the the list
		elif Operation=="delete":
			if LoginMode == 'retail':
				print("\nOperation not permitted") #Check if retail doesn't have access to delete function
			elif LoginMode == 'agent':
				ValidAccountList, SummaryLine = delete(ValidAccountList, InputFile)
				SummaryTransactionList.append(SummaryLine) #Add the summary line to the the list
		elif Operation=="deposit":
			SummaryLine = deposit(LoginMode, ValidAccountList, InputFile)
			SummaryTransactionList.append(SummaryLine) 
		elif Operation=="withdraw": #WithdrawTotalAmount allow to check the total amount limitation for retail
			SummaryLine, WithdrawTotalAmount = withdraw(LoginMode, ValidAccountList, WithdrawTotalAmount, InputFile)
			SummaryTransactionList.append(SummaryLine) 
		elif Operation=="transfer":
			SummaryLine = transfer(LoginMode, ValidAccountList, InputFile)
			SummaryTransactionList.append(SummaryLine) 
		elif Operation=="logout":
			print("\nLogout")
			logout(SummaryTransactionList, SummaryTransactionFile)
		elif Operation !="":
			print("\nChoice unvalid, try again") 


if __name__ == "__main__":
    main()