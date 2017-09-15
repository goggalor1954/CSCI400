#for num in range(2, 256):
#	if num > 1:	
#		for i in range(2, num):
#			if (num%i)==0:
#				break
#			else:
#				print(num)


#lower = int(input("Enter lower range: "))  
#upper = int(input("Enter upper range: "))  
  
for num in range(2,256):  
   if num > 1:  
       for i in range(2,num):  
           if (num % i) == 0:  
               break  
       else:  
           print(num)  
