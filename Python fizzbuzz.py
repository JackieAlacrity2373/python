a = 3 
b = 5 
print("Lets play fizzbuzz to an value please give me a value")
c = int(input())
print("Okay lets play fizzbuzz to ", c)
loop = int(0)
while(loop < c):
    loop = loop + 1
    if (loop % 15 == 0):
        print("Fizzbuzz")
    else:
        if(loop % 5 == 0):
            print("fizz")
        else:
            if(loop % 3 == 0):
                print("buzz")
            else:
                print(loop)
else:
        print("done here is fizzbuzz to ", c)
        print("Strange game the only winning move is not to play")
