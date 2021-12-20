# Number Guessing
# I tried to use some of Python magic but not over do it at the same time.
import random
import enum
import functools

# Here I set basic parameters for my project.

def int_check(text): # Checking if number are int type.
    while True:
        try:
            a = int(input(text))
        except ValueError:
            print("Value must be whole number.")
            continue
        else:
            return a

def bigger_number(bottom, sealing): # Checking if first number is bigger than second one and if not, redefine variables  
    while bottom < sealing:
        print("Start of spectrum must be bigger than its end. Choose new numbers.")
        bottom = int_check("Choose start of spectrum.\t")
        sealing = int_check("Choose end of spectrum. \t")
    return (bottom, sealing)                

def pick_number(value1, value2): # Random selection of numbers which will be guess.
    a = random.randint(int(value1),int(value2))
    return a

def shuffle_numbers(value1, value2): # Preparation of list which helps my build clues.
    b = [*range(int(value1), int(value2) + 1, 1)]
    random.shuffle(b)
    return b

def def_all(): # Setting of all needed variables to global namespace
    global bottom, sealing, random_number, shuffle_list, all_picks

    bottom = int_check("Choose start of spectrum.\t")
    sealing = int_check("Choose end of spectrum. \t")

    while bottom > sealing:
        print("Start of spectrum must be smaller than its end. Choose new numbers.")
        bottom = int_check("Choose start of spectrum.\t")
        sealing = int_check("Choose end of spectrum. \t")

    random_number = pick_number(int(bottom),int(sealing)) # I strugle with concept of using function before definition. I am looking forward to learn more elegant solution.
    shuffle_list = shuffle_numbers(int(bottom),int(sealing))
    all_picks = []
    

def_all()

######################################################################################

# Here is defined condition for sufficient range of numbers and shuffle_list is adjust for use in bigger_or_smaller function.

while len(shuffle_list) < 10 or len(shuffle_list) > 100: # Checking if range of numbers isn't too small or too big.
    try:
        if len(shuffle_list) < 10:
            print("Range of numbers must be at least 10 numbers long.\n")
            def_all()
        elif len(shuffle_list) > 100:
            print("Range of numbers can't be longer than 100 numbers.\n")
            def_all()
        else:
            break
    except ValueError:
        print("Value must be number.")

shuffle_list.remove(random_number)
######################################################################################

# Lower are defined functions for settting difficulty of the game. Names of functions indicate what they do.

class Difficulty(enum.Enum): # Using enum to set values for keywords
    easy = 15
    medium = 12
    hard = 10

class Difficulty_setting:
    difficulty_answer = str(input("Choose game difficulty: Easy, Medium, Hard.\t"))
    def __init__(self):
        while True:
            all_dif = ["easy", "medium", "hard"]
            answer1 = "Choose valid difficulty."
            try:
                if Difficulty_setting.difficulty_answer.lower() in all_dif:
                    break
                else:
                    print(answer1)
            except ValueError:
                print(answer1)


    def setting(answer):
        tries = 0
        for e in (Difficulty):
            if e.name == answer:
                tries = e.value
                return int(tries)
            else:
                continue

d = Difficulty_setting.difficulty_answer
number_of_tries = Difficulty_setting.setting(d) + 1
######################################################################################

# Lower are defined functions for setting different clues and their using. Names of functions indicate what they do.

class Clues: # Clues go from general to more concrete. Def multiples starts from number 3 because telling if number is even or odd and if number is multiple of 2 felt like same clue.
    multiples_range = list(range(3,11))
    list_of_multiples = []

    def __init__(self, number):
        self.number = number

    def trackcalls(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wrapper.has_been_called = True
            return func(*args, **kwargs)
        wrapper.has_been_called = False
        return wrapper

    @trackcalls
    def even_or_odd(number): # I am not sure if I could use decorator earlier in project. I will be glad if someone pinpoint that.
        if number % 2 == 0:
            return print("Number you want to guess is even.\n")
        elif number % 2 == 1:
            return print("Number you want to guess is odd.\n")


    def multiples(number):
        x = Clues.multiples_range
        y = Clues.list_of_multiples
        a = "Number you want to guess is multiple of number {}.\n".format

        for multiple in x:
            if number % multiple == 0:
                x.remove(multiple)
                y.append(multiple)

        for i in y:
            y.remove(i)
            yield print(a(i))

    def bigger_or_smaller(number): # 100 numbers limit is set becouse of this function. With bigger numbers, this clue felt too random and useless.
        for n in shuffle_list:
            shuffle_list.remove(n)
            if n < number:
                yield print("Number you want to guess is higher than number {}.\n".format(n))
            elif n > number:
                yield print("Number you want to guess is smaller than number {}.\n".format(n))

######################################################################################

# Finally here I use everything from upper part of code and process it into game outcome. I use lot of if statments, which does not fell to pythonic so I am looking forward to improve this area.

for i in range(number_of_tries):
    number_of_tries -= 1
    if number_of_tries == 0:
        print("You run out of tries. Better luck next time, GAME OVER!")
    else:
        print("Tries left: \t {}".format(number_of_tries))
        print("Tried numbers: \t {} \n".format(all_picks))
        try:
            my_pick = int(float(input("Choose your number.\t")))
            if my_pick == random_number:
                print("\nYou found right number. Good job!")
                break
            elif my_pick not in all_picks:
                all_picks.append(my_pick)
                print("\nThat's wrong answer. Here is one clue and try another one.")
                if Clues.even_or_odd.has_been_called == False:
                    Clues.even_or_odd(random_number)
                elif Clues.even_or_odd.has_been_called == True:
                    try:
                        next(Clues.multiples(random_number))
                    except StopIteration:
                        try:
                            next(Clues.bigger_or_smaller(random_number))
                        except StopIteration:
                            print("There are no more clues left.\n")
            else:
                print("You already picked this number. Try another one.")
        except ValueError:
            print("Value must be number.")
