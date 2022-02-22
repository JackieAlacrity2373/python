#buzz divisor#
print("It looks like you want to play fizzbuzz but first I need some information", "\n", "What should the first divisor be? 3 is the default")
a = int(input()) 
#fizz divisor#
print("Okay great what should the second divisor be? 5 is the default")
b = int(input()) 
#stop value#
print("Were almost ready to play fizzbuz, please give me a value to stop playing at")
c = int(input())
#Derive fizzbuzz from the inputs given for fizz and buzz #
d = (a * b)
print("Okay lets play fizzbuzz to ", c)
loop = int(0)
while(loop < c):
    loop = loop + 1
    if (loop % d == 0):
        print("Fizzbuzz")
    else:
        if(loop % b == 0):
            print("fizz")
        else:
            if(loop % a == 0):
                print("buzz")
            else:
                print(loop)
else:
        print("done here is fizzbuzz to ", c)
        print("Strange game the only winning move is not to play")
