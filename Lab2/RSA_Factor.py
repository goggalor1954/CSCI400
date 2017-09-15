#what i need to do
# read in text from key a and b : done
# format moduli so that it can be read by fastgcd. : done
#output moduli to fastgcd : done
# read in vunerable moduli and factors from fast gcd: done
#compute the primes of up to 1024:done
#compute the prime factors of the moduli(mutiply primes to get the moduli)
#store these prime factors
#find 2 distinct moduli whose share one prime factor but not the other:
#im going to create an object for each moduli so that i can keep their primes straight.
# ok, i can't figure out how to pass mutiple data to a class object right now. ill figure out in the morning.
class mods:
 modulus=""
 primeFactors=[]
 def __init__(self, mod):
  modulus=mod
 def __repr__(self):
	return modulus
 

 


import os

vulnerable_moduliA=[]
vulnerable_moduliB=[]
gcdA=[]
gcdB=[]
contents =[]
mod_A_Primes=[]
mod_B_primes=[]

#read in text from public key A
with open('Public-KeyA.txt', 'rt') as inFile:
	for line in inFile:
		contents.append(line)

#assignes moduli from public key a to modA
modA=''.join(contents)
modA=modA.split("modulus:",1)[1]
modA=modA.split("publicExponent:", 1)[0]
modA=modA.replace(" ", '')
modA=modA.replace(":", '')

#read in text from public key B
contents=[]
with open('Public-KeyB.txt', 'rt') as inFile:
	for line in inFile:
		contents.append(line)

#assignes moduli from public key B to modB
modB=''.join(contents)
modB=modB.split("modulus:",1)[1]
modB=modB.split("publicExponent:", 1)[0]
modB=modB.replace(" ", '')
modB=modB.replace(":", '')

#generate gcd from Key A, read in vunerable mods and their gcd
textFile=open('modA.txt','w')
textFile.write(modA)
textFile.close()
os.system("./fastgcd modA.txt")
os.system("rm modA.txt")
with open('vulnerable_moduli', 'rt') as inFile:
	for line in inFile:
		vulnerable_moduliA.append(mods(line))
with open('gcds', 'rt') as inFile:
	for line in inFile:
		gcdA.append(line)
os.system("rm vulnerable_moduli")
os.system("rm gcds")

#generate gcd from Key B, read in vunerable mods and their gcd
textFile=open('modB.txt','w')
textFile.write(modB)
textFile.close()
os.system("./fastgcd modB.txt")
os.system("rm modB.txt")
with open('vulnerable_moduli', 'rt') as inFile:
	for line in inFile:
		vulnerable_moduliB.append(mods(line))
with open('gcds', 'rt') as inFile:
	for line in inFile:
		gcdB.append(line)
os.system("rm vulnerable_moduli")
os.system("rm gcds")

#generate prime numbers for later use
primes=[]
for num in range(2,1024):  
   if num > 1:  
       for i in range(2,num):  
           if (num % i) == 0:  
               break  
       else:  
           primes.append(num)

#test
print(vulnerable_moduliA[0])

#find prime factors
for i in range(0, len(vulnerable_moduliA)):
 for j in range(0, len(primes)-1):
  for k in range(j+1, len(primes)):
   if primes[j]*primes[k]==vulnerable_moduliA[i].modulus:
    vulnerable_moduliA[i].primeFactors.append(primes[j])
    vulnerable_moduliA[i].primeFactors.append(primes[k])

#test
print("a")
for i in range(0, len(vulnerable_moduliA[0].primeFactors)):
 print(vulnerable_moduliA[0].primeFactors[i])
print("b")
