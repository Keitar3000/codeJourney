# Write your code here :-)
#collatz.py
#keita linden
'''Write a function named collatz() that has one parameter named number.
If number is even, then collatz() should print number // 2 and return this
value. If number is odd, then collatz() should print and return 3 * number + 1.'''

def collatz(number): #define collatz with parameter number
    if number % 2 == 0: #if number is even, print number // 2
        number = number//2

    elif number %2 ==1: #if number is odd, print (3*number) +1
        number = (number * 3) + 1

    print(number)
    return (number)



'''Then write a program that lets the user type in an integer and that keeps
calling collatz() on that number until the function returns the value 1.
(Amazingly enough, this sequence actually works for any integer—sooner or
later, using this sequence, you’ll arrive at 1! Even mathematicians aren’t
sure why. Your program is exploring what’s called the Collatz sequence,
sometimes called “the simplest impossible math problem.”)'''

def collatz_seq():
    while True:
        try:
            user_input = int(input('Enter an integer: '))
            while user_input != 1:
                user_input = collatz(user_input)
            break #when user inputs 1
        except ValueError:
            print('Enter a legal integer')

collatz_seq()


'''Remember to convert the return value from input() to an integer with the
int() function; otherwise, it will be a string value. '''



