# what i need to do
# write a program that reads in the text of public ket a and b
# parses checks public exponent and addigns its value
# parses mudulus of a and b and assignes them their values. removing incorect characters.
# runs the gcd program twice
#reads in the gcd results from the fromgram and assignes them to p and w.
#inputs the variables into the formula and outputs answer to the screen and a text file.
# i figured out whats wrong, i need to just add one modulus. not all of them
#use the gcd from the mod, find the prime numbers that plug into the function
#ok, so i dont need to compare the 2 for the first part. just factor the moduli for 4.4.1
#4.4.2 you need to generate the private key


#generate prime numbers for later use
primes=[]
for num in range(2,256):  
   if num > 1:  
       for i in range(2,num):  
           if (num % i) == 0:  
               break  
       else:  
           primes.append(num)

#test
print(primes) 
print(2==0x2)

contents =[]
#read in text from public key A
with open('Public-KeyA.txt', 'rt') as inFile:
	for line in inFile:
		contents.append(line)
#assigns the value of of exponent to publicExponent
publicExponentA = ''.join(contents) #contains the public exponent
publicExponentA = publicExponentA.split("publicExponent:", 1)[1] #[0] returns left [1] returns right
publicExponentA = publicExponentA.split("(",1)[0]
publicExponentA=publicExponentA.replace(' ', '')

#assignes modulus from public key a to modA
modA=''.join(contents)
modA=modA.split("modulus:",1)[1]
modA=modA.split("publicExponent:", 1)[0]
modA=modA.replace(" ", '')
modA=modA.replace(":", '')


#repeat for B. make sure the exponents match
contents=[]
with open('Public-KeyB.txt', 'rt') as inFile:
	for line in inFile:
		contents.append(line)

publicExponentB = ''.join(contents) #contains the public exponent
publicExponentB = publicExponentB.split("publicExponent:", 1)[1] #[0] returns left [1] returns right
publicExponentB = publicExponentB.split("(",1)[0]
publicExponentB=publicExponentB.replace(' ', '')

if publicExponentA != publicExponentB: #if the publicExponents do not match, print statment and exit program.
	print("These keys do not have the same exponent. Unable to factor the RSA modulus.")
	exit()
#assignes modulus from public key B to modB
modB=''.join(contents)
modB=modB.split("modulus:",1)[1]
modB=modB.split("publicExponent:", 1)[0]
modB=modB.replace(" ", '')
modB=modB.replace(":", '')


#generate gcd from mods a
textFile=open('modA.txt','w')
textFile.write(modA)
textFile.close()
import os
os.system("./fastgcd modA.txt")
os.system("rm modA.txt")
os.system("mv vulnerable_moduli vulnerable_moduli_A")
os.system("mv gcds gcds_A")

#generate gcd from mods b
textFile=open('modB.txt','w')
textFile.write(modB)
textFile.close()
os.system("./fastgcd modB.txt")
os.system("rm modB.txt")
os.system("mv vulnerable_moduli vulnerable_moduli_B")
os.system("mv gcds gcds_B")
