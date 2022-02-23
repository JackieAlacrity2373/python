a = 3 
b = 5 
print("Lets play fizzbuzz to an value please give me a value")
while True:
        try:
           c = int(input("Please enter a number:  "))
           break
        except ValueError:
                   print("That is not a number do you think this is a game human? give me a number please... ")
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
