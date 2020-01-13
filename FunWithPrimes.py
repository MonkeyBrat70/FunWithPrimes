from os import path
from os import system

from sys import exit

#Startup global parameters.
primes = []
PRIMES_FILENAME = 'Primes'
PRIME_PRODUCTS_FILENAME = 'PrimeProducts'
ERROR_MESSAGE = 'The function requires a single number, two numbers, or no input.'

#Open the file and get known primes or create a the file.
if path.exists(PRIMES_FILENAME):
    with open(PRIMES_FILENAME) as file:
        for line in file:
            primes.append(int(line))
else:
    with open(PRIMES_FILENAME, 'w') as file:
        file.write('2\n')
        primes.append(2)

def get_factors(number):
    """Gets the factors of a number or indicates that it is prime."""
    isPrime = False
    #Check to see if number is already a known prime.
    if number < primes[len(primes)-1]:
        isPrime = number in primes
    #Test to see if number is prime.
    if is_prime(number):
            isPrime = True
    else:
        factors = []
        for n in range (2, number):
            if n in factors:
                break
            else:
                if number % n == 0:
                    factors.append(n)
                    factors.append(number//n)
                    print(f'{n} and {number // n} are factors of {number}.')
    if isPrime:
        print(number, 'is a prime number')

def list_primes(*nums):
    """Prints prime numbers.
    
    A single input will print all primes less than the input number.

    Two input numbers will print the primes greater than or equal to 
    the lower of the two numbers which are less than the higher of the 
    input numbers.
    
    No input will list all of the known primes in the Primes file."""
    listOfPrimes =  get_primes(*nums)
    if listOfPrimes == []:
        print('There were no primes in the given range.')
    elif listOfPrimes == ERROR_MESSAGE:
        print(listOfPrimes)
    else:
        for prime in listOfPrimes:
            print(prime)

def is_prime(number):
    """Tests to see if a number is prime."""
    highestPrime = primes[len(primes)-1]
    #Test known primes.
    if number in primes:
        return True
    else:
        # Number is not a known prime, and needs to be tested, first 
        # with known primes. This only checks up to number//2, because
        # there cannot be a prime factorization beyond there.  The 
        # first test is number % 2.
        for x in primes:
            if x < number//2:
                if number % x == 0:
                    return False
            else:
                break
        # Number is not divisible by known primes, we so need to test 
        # all numbers after highest prime. middle is the highest factor
        # possible.
        middle = number // 2
        for x in range (highestPrime, middle + 1):
            if number % x == 0:
                return False
        # All possibilities are exhausted, number is prime.
        primes.append(number)
        return True

def old_list_primes(number):
    """Old method to calculate primes which is less efficient. 
    
    This method tests every integer from 2 to one less than the number 
    to determine if the number can be factored.  If not, the number is 
    prime.  A more efficient method only tests known prime numbers, 
    because all integers can be factored completely into prime numbers,
    unless they are themselves prime.
    
    This one is kept here for experimentation measuring the time 
    difference between this one and the more efficient 'list_primes'."""
    count = 0
    isPrime = True
    for n in range (2, number):
        for x in range (2, n):
            if n % x == 0:
                isPrime = False
                break
        else:
            isPrime = True
        if isPrime:
            print(n)
            count += 1
    print('\nThere are {} primes less than {}.'.format(count, number))

def get_primes(*numbers):
    """Returns prime numbers.
    
    A single input will return all primes less than the input number.

    Two input numbers will return the primes greater than or equal to 
    the lower of the two numbers which are less than the higher of the 
    input numbers.
    
    No input will return all of the known primes in the Primes file."""
    #User input one number.
    if len(numbers) == 1:
        minNumber = 0
        maxNumber = numbers[0]
    #User input two numbers.
    elif len(numbers) == 2:
        #First number is less than the second.
        if numbers[0] <= numbers[1]:
            minNumber = numbers[0]
            maxNumber = numbers[1]
        #Second number is less than the first.
        elif numbers[0] > numbers[1]:
            minNumber = numbers[1]
            maxNumber = numbers[0]
        #Numbers are the same.
        elif numbers[0] == numbers[1]:
            minNumber = 0
            maxNumber = numbers[0]
        else:
            return ERROR_MESSAGE
    #User input no numbers, so list all primes known.
    elif len(numbers) == 0:
        return primes
    #User entered too many numbers.
    else:
        return ERROR_MESSAGE
    primesList = []
    #User max number is less than the highest known prime in Primes file.
    highestPrime = primes[len(primes)-1]
    if maxNumber <= highestPrime:
        for prime in primes:
            if ((prime >= minNumber) and (prime < maxNumber)):
                primesList.append(prime)
            if prime >= maxNumber:
                break
    #Request may identify new primes.
    else:
        newPrimes = []
        countOfPrimes = len(primes)
        for prime in primes:
            if (prime >= minNumber) and (prime < maxNumber):
                primesList.append(prime)
        for num in range(highestPrime + 1, maxNumber):
            #Update the primes list with the new prime number if found.
            if is_prime(num):
                # Add new prime to list to be returned if it is in the 
                # range requested.
                if (num >= minNumber) and (num < maxNumber):
                    primesList.append(num)
                # Add new prime to the list to be added to the Primes
                # file.
                newPrimes.append(num)
        #Add newly discovered primes to file
        if len(primes) > countOfPrimes:
            add_primes_to_file(newPrimes, PRIMES_FILENAME)
            refresh_primes_list()
        
    return primesList

def distance_between_primes(*nums):
    """Gets a list of the difference between sequential prime numbers.
    
    A single input will get the differences between all primes less 
    than the input number.

    Two input numbers will get the differences between primes greater 
    than or equal to the lower of the two numbers which are less than 
    the higher of the input numbers.
    
    No input will get the differences between all of the known primes 
    in the Primes file."""
    lastPrime = 0
    highestDistance = 0
    listOfPrimes = get_primes(*nums)
    #Calculate and distances between primes.
    #If the response is empty return an empty array.
    if listOfPrimes == []:
        return listOfPrimes
    #If the response is an error, print the error.
    if listOfPrimes == ERROR_MESSAGE:
        print(listOfPrimes)
        return
    distanceArray = []
    lastPrime = listOfPrimes[0]
    for x in listOfPrimes:
        if x > lastPrime:
            distance, lastPrime = x - lastPrime, x
            if distance > highestDistance:
                highestDistance = distance
            distanceArray.append(distance)
    print ('Highest distance was', highestDistance)
    return distanceArray

def generate_primes_to_file(fileName, number):
    """Generates a list of primes in the range indicated and stores 
    them to a file."""
    originalPrimesLen = len(primes)
    def wrap_up():
        if count == 1:
            noun = 'prime'
        else:
            noun = 'primes'
        system('cls')
        print(f'{count} {noun} found, highest is {primes[count-1]}.')
        if len(primes) > originalPrimesLen:
            create_primes_file_from_list(PRIMES_FILENAME)
    #Open a new file and write the list of primes to it as strings.
    if fileName == PRIMES_FILENAME:
        print('"Primes" is a reserved filename and cannot be used.')
        return
    else:
        count = 0
        start = 2
        with open(fileName,'w') as file:
            try:
                for prime in primes:
                    if prime < number:
                        count += 1
                        file.write(str(prime) + '\n')
                    else:
                        system('cls')
                        print(f'{count} primes loaded...'
                            + f'current prime is {primes[count-1]}.')
                        wrap_up()
                        return
                system('cls')
                print(f'{count} primes loaded...'
                    + f'current prime is {primes[count-1]}...finding more...')
                start = primes[count-1] + 1
                for num in range(start, number):
                    if is_prime(num):
                        count += 1
                        file.write(str(num) + '\n')
                        system('cls')
                        print(f'Calculating...{count} primes so far...'
                            + f'current prime is {primes[count-1]}.')
                wrap_up()
            except KeyboardInterrupt:
                if count == 1:
                    noun = 'prime'
                else:
                    noun = 'primes'
                system('cls')
                print(f'{count} {noun} found. Highest was '
                    + f'{primes[count-1]}.')
                if len(primes) > originalPrimesLen:
                    create_primes_file_from_list(PRIMES_FILENAME)
                exit()

def create_primes_file_from_list(fileName):
    """Generates a file from a list of prime numbers."""
    with open(fileName, 'w') as file:
        for num in primes:
            line = str(num) + '\n'
            file.write(line)

def add_primes_to_file(newPrimes, fileName):
    """Appends a list of prime numbers to a file."""
    with open(fileName, 'a') as file:
        for newPrime in newPrimes:
            line = str(newPrime) + '\n'
            file.write(line)

def refresh_primes_list():
    """Refreshes the primes list in memory after an addition is made to
    the list."""
    primes.clear()
    with open(PRIMES_FILENAME) as file:
        for line in file:
            primes.append(int(line))

def count_primes(*numbers):
    """Counts the prime numbers in a range."""
    listOfPrimes = get_primes(*numbers)
    if listOfPrimes == ERROR_MESSAGE:
        print(listOfPrimes)
        return
    return len(listOfPrimes)
        

def get_prime_factors(number):
    """Returns the prime factors of a number in an array."""
    primeFactors = []
    highestFactor = number
    highestPrime = primes[len(primes)-1]
    nextHighestPrime = primes[len(primes)-2]
    if number > highestPrime * nextHighestPrime:
        get_primes((number // highestPrime) + 1)
    x = 0
    while primes[x] <= highestFactor:
        primeFactor = primes[x]
        if highestFactor % primeFactor == 0:
            x = 0
            primeFactors.append(primeFactor)
            highestFactor = highestFactor // primeFactor
        else: 
            x += 1
            if x > len(primes) - 1:
                get_primes(highestFactor + 1)
    return primeFactors

def print_prime_factors(number):
    """Prints the prime factorization of the input number"""
    primeFactors = get_prime_factors(number)
    count = 1
    outputString = ''
    for index, factor in enumerate(primeFactors):
        if index == len(primeFactors) - 1:
            if count > 1:
                outputString += (str(factor) + '^' + str(count))
            else:
                outputString += (str(factor))
        else:
            if factor == primeFactors[index + 1]:
                count += 1
                next
            else:
                if count > 1:
                    outputString += (str(factor) + '^' + str(count) + ' * ')
                else:
                    outputString += (str(factor) + ' * ')
                count = 1
    print(outputString)

#Print general information about the known primes.
refresh_primes_list()
if len(primes) == 1:
    verb = 'is'
    noun = 'prime'
else: 
    verb = 'are'
    noun = 'primes'
print(f'There {verb} currently {len(primes)} {noun} in the {PRIMES_FILENAME}'
    + ' file.')
print(f'The highest is {primes[len(primes)-1]}.')

