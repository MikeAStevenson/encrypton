#Copyright 2013 Michael Sisco
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

#Imports
import sys
import os
import random
import platform

#Initialize the arrays (probably not actually needed)
charArray = []
charSubArray = []
primeArray = []
spaceArray = []

#Load the character set
def loadCharSet():
	# Opens the dat file which MUST be next to this script
	charFile = open('charset.dat')
	while True:
		# Read the file one line at a time
		char = charFile.read(1)
		if not char:
			#End of file
			break
		else:
			# Put the character set in both the original, and substituted array
			charArray.append(char)
			# This will be shuffled later
			charSubArray.append(char)
	return
# End of function (Notepad++ likes it...)

# Load the character set that is going to be used to fill the spaces
# There are multiple characters in the file, and more could be added,
# as long as those characters aren't in the actual character set
def loadSpaces():
	spaceFile = open('spaceset.dat')
	while True:
		char = spaceFile.read(1)
		if not char:
			#End of file
			break
		else:
			spaceArray.append(char)
	return
# EOF

# Used to load the primes into the array
# The numbers are started at 3, because that's
# the lowest prime we will be using. 2 is technically
# prime, but it's not an important enough number
def loadPrimes():
	for num in range(3, len(charArray)):
		if checkIfPrime(num):
			primeArray.append(num)
	return
# End of function

# Trial division! (Thank you wikipedia)
def checkIfPrime(num):
	# Iterates through the numbers below square root. **0.5 = square root
	# Anything larger than half the number times anything else, is 
	# obviously larger than the number. Hence, just ignore any number
	# larger than half the original number. ( Which is why we square root )
	for checkNum in range(2, int(num**0.5)+1):
		if num % checkNum == 0:
			return False
	return True
# End of function
	
#functions

# Function to check input used for the menu
def checkInput(strInput):
	# If it isn't an integer, then make them try again
	if not checkIfInt(strInput):
		return False
	intInput = int(strInput)
	if (intInput is 1) or (intInput is 2) or (intInput is 3):
		return True
	else:
		# If it isn't a 1, 2, or 3, then make them try again
		return False
	return
#EOF

#check if their choice was an integer or not
def checkIfInt(strInput):
	try:
		# Try to force it to become an integer
		int(strInput)
		return True
	except ValueError:
		#It doesn't want to be an integer, so return False
		return False
# End of function

# Load the actual menu and accept input from the user
def loadMenu():
	while True:
		print ("1) Create Ciphertext 2) Decrypt Ciphertext 3) Exit")
		intInput = input("Please select a valid option: ")
		boolCheck = checkInput(intInput)
		if boolCheck:
			break
		else:
			continue
	return int(intInput)
# EOF

# Prompt the user for the "public" key
# It has to be between 0 and whatever the max number
# of elements in the character set array is.
def promptForKey():
	while True:
		strKeyIn = input("Enter a number between 0 and " + str(len(charArray)) + ": ")
		if checkIfInt(strKeyIn):
			intKeyIn = int(strKeyIn)
			if (intKeyIn >= 0 and intKeyIn <= len(charArray)):
				break
			else:
				continue
	return int(strKeyIn)
# EOF

# Gets the closest prime, out of the prime array, to the given number
# Doesn't really take anything into account for distance at the beginning,
# so it might be slightly inefficient. BUT, it's a small set of numbers, so
# overall, it doesn't really matter.
def getClosestPrime(num):
	closestPrime = None
	distance = 50
	for primeNum in primeArray:
		if abs(primeNum - num) <= distance:
			distance = abs(primeNum - num)
			closestPrime = primeNum
	return closestPrime
# EOF

# Used to get a file for reading
# fileType is used to determine if it should check for .txt or .enc
# 0 - txt, anything else for .enc
def getFile(fileType):
	while True:
		fileName = input('Enter the file name (must include extension): ')
		#Check that the file exists
		if os.path.exists(fileName):
			# Check to see if the file is the right extension. Either .txt or .enc
			if (os.path.splitext(fileName)[1] == '.txt' and fileType is 0) or (os.path.splitext(fileName)[1] == '.enc'):
				file = open(fileName)
				break
			else:
				print ("Wrong file extension")
				if (systemOs == "Windows"):
					print ("(CTRL+C to exit.")
				else:
					print ("(CTRL+Z to exit.")
		else:
			print ("File does not exist")
	return file
#EOF

# Creates an encrypted file by reading the file in character by character
# and replacing each character with one created by looking at the character
# that is in the substitution array at the index of the character in the original
# array, and shifting it over a certain number of times.
def encryptFile(file, pubKey, priKey):
	strArray = []
	newArray = []
	for line in file:
		for char in line:
			# Check that the character is in the array. If not, treat it like a space
			if char in charArray:
				# Get the variable that is going to be used to shift the chars over
				shiftVar = getSecondShiftVar(pubKey, priKey)
				# Get the index of the character in the original array
				charIndex = charArray.index(char)
				newIndex = charIndex
				# Move the index of the character up in the array
				# It also has a tendency to sometimes generate negative stuff, so get the absolute value
				for x in range(0, abs(shiftVar)):
					newIndex += 1
					# Wrap the number back around if it goes "out of bounds"
					if newIndex > (len(charArray)-1):
						newIndex = 0
					if newIndex < 0:
						newIndex = (len(charArray)-1)
				# Add the new character to the array that will be used to create the file
				newArray.append(charSubArray[newIndex])
			else:
				# If the character isn't part of the original character set, we will put a random
				# character from the space array in its place. We don't want the same one over and over,
				# or it may get guessable.
				randInt = random.randint(0, len(spaceArray)-1)
				# I do this because the randInt by itself seems to always return the same thing
				random.shuffle(spaceArray)
				newArray.append(spaceArray[randInt])
		# Put a new line at the end of each line
		newArray.append('\n')
	# Create the new file and write the array to it, one character at a time
	newFile = open(os.path.splitext(file.name)[0]+'.enc', 'w+')
	for char in newArray:
		newFile.write(char)
	newFile.write(str(len(charArray))+'-'+str(pubKey)+'-'+str(priKey))
	newFile.close()
	return strArray
#EOF

# Used to decrypt the file by reading and converting one character at a time
# It looks for the given character in the substitution array, and moves it backwards
# a certain number of times, which is generated by the public and private key.
# After shifting it backwards, the character from the original character set
# is taken with the given index.
def decryptFile():
	# get the file and read it one line at a time
	file = getFile(1)
	lineArray = []
	for line in file:
		lineArray.append(line)
	# get the last line, which contains our keys
	keyLine = lineArray[len(lineArray)-1]
	# Split the key up with the delimiter that was used during encryption
	keyArray = keyLine.split('-')
	# Remove the line with the key from the array that is going to be decrypted
	lineArray.remove(lineArray[len(lineArray)-1])
	# Max Charset value
	maxCharValue = int(keyArray[0])
	# Public key
	pubKey = int(keyArray[1])
	# Private key
	priKey = int(keyArray[2])
	# Create the sub array with the given public and private keys
	createSubArray(pubKey, priKey)
	newArray = []
	for line in lineArray:
		# Read it one character at a time
		for char in line:
			# If it is in the original character array, decrypt it
			if char in charArray:
				# Get the number of times shifted based on public and private key
				shiftVar = getSecondShiftVar(pubKey, priKey)
				# Get the index of the character in the substitution array
				charIndex = charSubArray.index(char)
				newIndex = charIndex
				# Move the character backwards the amount of times given earlier
				# It also has a tendency to sometimes generate negative stuff, so get the absolute value
				for x in range(0, abs(shiftVar)):
					newIndex -= 1
					# Wrap back around if "out of bounds"
					if newIndex > (len(charArray)-1):
						newIndex = 0
					if newIndex < 0:
						newIndex = (len(charArray)-1)
				# Put the decrypted character into the array that is going to be written to the file
				newArray.append(charArray[newIndex])
			else:
				# Put a space in place of any unknown characters, which should put them in the right places
				newArray.append(' ')
		# Put a newline at the end of each line
		newArray.append('\n')
	# Write it all out
	newFile = open(os.path.splitext(file.name)[0]+'.dec','w+')
	for char in newArray:
		newFile.write(char)
	newFile.close()
	return
# EOFunction

# returns the variable that is going to be used to shift the variables.
# The number returned can become VERY large. Very large. But that's good.
# Makes it harder to follow. (not really)
# This is where all of the fun stuff happens, since the random means
# I really shouldn't know the outcome. Which is good.
# This is only used to create the substitution array
def getShiftVariable(pubKey, priKey, char):
	# Putting a seed insures that the same numbers will be generated everytime.
	# Without this, it will be hard to decrypt
	random.seed(pubKey*priKey)
	# Creates the number that will be used to do math for a certain number of times
	randInt = random.randint(pubKey+priKey, pubKey+priKey+((pubKey%len(charArray))))
	# Start the number at the index of the character in the original array
	shiftVar = charArray.index(char)
	for x in range(0, randInt):
		# Add, and subtract, and random number to the variable. Sometimes it's half the number, sometimes it isn't.
		shiftVar += random.randint(6, 30) * random.randint(1,2)
		shiftVar -= random.randint(0, 40) / random.randint(1,2)
	if shiftVar is 0:
		# If the number for some reason comes out to be zero, it should become
		# a random number between 5 and 50
		shiftVar = random.randint(5, 50)
	return shiftVar
# EOF

# Get the second variable that will be used when shifting the characters.
# It is only used for shifting, not for creating the other array.
# This is just as random as the other number, which I enjoy.
def getSecondShiftVar(pubKey, priKey):
	# Seed the random number using the private key, so that it will be the same each time
	random.seed(priKey)
	# Creates the number that will be used to do math for a certain number of times
	randInt = random.randint(pubKey, pubKey+(priKey*len(charArray))*pubKey)
	# Get the starting point for the number shift
	shiftVar = random.randint(0, len(charArray))
	for x in range(0, randInt):
		# Do a "coin flip" with a 65% probability of heads
		if random.random() > .65:
			# If it's heads, move it up
			shiftVar += 1
		else:
			# If it's tails, move it down
			shiftVar -= 1
	if shiftVar is 0:
		# Like the other, if zero, make it a random number between 5 and 50
		shiftVar = random.randint(5, 50)
	return shiftVar
# EOFunction

# Creates the substition array, which is a key part of the whole thing
# The function just takes a public and private key, and creates the array
# by shuffling the array multiple times. Whatever it uses to shuffle is
# based upon a seed created by the public key, private key, and the index of the char
# pubKey - the chosen public key
# priKey - the private key, or closest prime
def createSubArray(pubKey, priKey):
	# Shuffle it once for each character in the array. Isn't necessary, but I want to
	for char in charSubArray:
		# Do the whole absolute thing, in case of negative
		shiftVar = abs(getShiftVariable(pubKey, priKey, char))
		charIndex = charArray.index(char)
		newIndex = charIndex
		# seed based upon number, that way it's always the same result
		random.seed(shiftVar)
		# Shuffle the array around
		random.shuffle(charSubArray)
	return
#EOF


# The main of the script, this is where everything is first called
if __name__ == '__main__':
	# Should probably be moved somewhere farther up to increase visibility...
	systemOs = platform.system()
	
	# Load up the character sets and primes
	loadCharSet()
	loadPrimes()
	loadSpaces()
	
	# Do the menu stuff
	intChoice = loadMenu()
	if intChoice is 1:
		# If they choose to encrypt a the file, start calling those methods
		intSelectedKey = promptForKey()
		intClosestPrime = getClosestPrime(intSelectedKey)
		createSubArray(intSelectedKey, intClosestPrime)
		file = getFile(0)
		strArray = encryptFile(file, intSelectedKey, intClosestPrime)
	elif intChoice is 2:
		# Start the decryption stuff
		decryptFile()
	else:
		# Exit
		sys.exit(0)
#EOI
