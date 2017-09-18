#####IMPORTANT#####
#this program should be run from the directory lab-crypto1.
# the fastgcd too must also have been extracted and installed in the lab-crypto/tools/fastgcd directory.

#this program reads the files Public-keyA.txt and Public-KeyB.txt and useing fastgcd determines their private keys.

import os
import struct
import rsa
from Crypto.PublicKey import RSA

#searches for matching gcd's from public key A and B. indexes their location.
def gcdCheck(gcdA, gdcB):
 for i in range(len(gcdA)):
  for j in range(len(gcdB)):
   if(gcdA[i]==gcdB[j] and i!=j):
    index=[]
    index.append(i)
    index.append(j)
    return index

#divides the indexed moduli by the indexd gcd's to get the value of q1 and q2
def qFind(vulnerable_moduliA,vulnerable_moduliB, gcdA, gcdB, gcdIndex):
 pValue=[]
 pValue.append(int(vulnerable_moduliA[gcdIndex[0]],16)/int(gcdA[gcdIndex[0] ],16))
 pValue.append(int(vulnerable_moduliB[gcdIndex[1]],16)/int(gcdB[gcdIndex[1]],16))
 return pValue

#the extended euclidean algorithm.
def extendedEucl(inA, inB):
 if inA==0:
  return(inB, 0, 1)
 else:
  x, y, z = extendedEucl(inB % inA, inA)
  return(x, z - (inB//inA)*y, y)

#returns the modular inverse
def getInv(ex, mod):
 gcd, a, b =extendedEucl(ex, mod)
 if (gcd!=1):
  return None
 else:
  return a%mod

#given the p value, the q value, the vulnerable modulus and the public exponent, returns the private key decrypted private key.
def getPrivateKey(qVal, pVal, publicExp, gcdIndex, indexSlot, vulnerable_moduli):
 #inorder to bugcheck im going to break each of these into its own components
 e= int(publicExp,16)
 n= int(vulnerable_moduli[gcdIndex[indexSlot]].split('0x',1)[1],16)
 p=int(pVal[gcdIndex[indexSlot]],16)
 q=(qVal[indexSlot])
 t=(p-1)*(q-1)
 d=getInv(e, t)
 pk = RSA.construct((n, long(e), d, long(p), long(q)))
 return pk

#assignes the value of the public Exponent
def parsExp(contents):
 publicExponent = ''.join(contents)
 publicExponent = publicExponent.split("publicExponent:", 1)[1] #[0] returns left [1] returns right
 publicExponent = publicExponent.split("(",1)[0]
 publicExponent=publicExponent.replace(' ', '')
 publicExponent='0x'+publicExponent
 return publicExponent

# returns a list of the parsed modulus values 
def parsMods(contents):
 mod=''.join(contents)
 mod=mod.split("modulus:",1)[1]
 mod=mod.split("publicExponent:", 1)[0]
 mod=mod.replace(" ", '')
 mod=mod.replace(":", '')
 return mod

#uses fastgcd to find the gcd's of vunerable moduli, passes those values as well as the moduli.
def findGCD(gcds, mods, vulnerable_moduli):
 textFile=open('mod.txt','w')
 textFile.write(mods)
 textFile.close()
 os.system("tools/fastgcd/./fastgcd mod.txt")
 os.system("rm mod.txt")
 with open('vulnerable_moduli', 'rt') as inFile:
 	for line in inFile:
		vulnerable_moduli.append('0x'+line) #read the mod in as hex
 with open('gcds', 'rt') as inFile:
	for line in inFile:
		gcds.append('0x'+line.split('\n', 1)[0])
os.system("rm vulnerable_moduli")
os.system("rm gcds")

#converts a hex value to a double
def double_to_hex(f): 
 return hex(struct.unpack('<Q',struct.pack('<d', f))[0])

#creates a file containing a properly formated RSA Private key
def getPrivateKeyFile(qVal, pVal, publicExponent, gcdIndex, indexSlot, fileName, vulnerable_moduli):
 outFile=open(fileName, 'w')
 pk=getPrivateKey(qVal, pVal, publicExponent, gcdIndex, indexSlot, vulnerable_moduli)
 outFile.close()


vulnerable_moduliA=[]
vulnerable_moduliB=[]
gcdA=[]
gcdB=[]
contents =[]


#read in text from Public-KeyA
with open('Public-KeyA.txt', 'rt') as inFile:
	for line in inFile:
		contents.append(line)

#assigns the value of the exponent to publicExponentA
publicExponentA=parsExp(contents)

#assignes moduli from Public-KeyA to modA
modA=parsMods(contents)

#read in text from public key B
contents=[]
with open('Public-KeyB.txt', 'rt') as inFile:
	for line in inFile:
		contents.append(line)

#assigns the value of of exponent to publicExponentB
publicExponentB=parsExp(contents)

#if the publicExponents do not match, print statment and exit program.
if publicExponentA != publicExponentB: 
	print("These keys do not have the same exponent. Unable to find the private key.")
	exit()

#assignes moduli from public key B to modB
modB=parsMods(contents)


#finds the gcds from Key A, then B, reads in vunerable mods and their gcds
findGCD(gcdA, modA, vulnerable_moduliA)
findGCD(gcdB, modB, vulnerable_moduliB)

#searches for matching gcd's from public key A and B. indexes their location.
gcdIndex = gcdCheck(gcdA, gcdB) 

#divides the indexed moduli by the indexd gcd's to get the value of q1 and q2
qValue = qFind(vulnerable_moduliA,vulnerable_moduliB, gcdA, gcdB, gcdIndex)

getPrivateKeyFile( qValue, gcdA, publicExponentA, gcdIndex, 0, 'PrivateKeyA.txt', vulnerable_moduliA)
getPrivateKeyFile( qValue, gcdB, publicExponentB, gcdIndex, 1, 'PrivateKeyB.txt', vulnerable_moduliB)

