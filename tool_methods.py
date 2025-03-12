import math
import inspect



def add_two_numbers(number_1 : float, number_2 : float) -> float:
    """
    Add number_1 and number_2.
    
    Parameters:
    number_1: The first number to add.
    number_2: The second number to add.
    
    Returns:
    float: The sum of two numbers.
    """

    return number_1 + number_2

def subtract_two_numbers(number_1 : float, number_2 : float) -> float:
    """
    Subtract number_2 from number_1 i.e. number_1 - number_2
    
    Parameters:
    number_1: The number to subtract from.
    number_2: The number that gets subtracted.
    
    Returns:
    float: number_1 - number_2
    """

    return number_1 - number_2

def multiply_two_numbers(number_1 : float, number_2 : float) -> float:
    """
    Multiply number_1 and number_2.
    
    Parameters:
    number_1: The first number to multiply.
    number_2: The second number to multiply.
    
    Returns:
    float: The product of two numbers.
    """

    return number_1 * number_2

def divide_two_numbers(number_1 : float, number_2 : float) -> float:
    """
    Divide number_1 by number_2.
    
    Parameters:
    number_1: The number to divide.
    number_2: The number to divide by.
    
    Returns:
    float: number_1/number_2.
    """

    if(number_2!=0.0):
        return number_1/ number_2
    
    return "Cannot divide by zero."

def logarithm(input_number : float):
    """
    Perform logarithm operation on the input_number with base e.

    Parameters:
    input_number: The number to perform logarithm operation on.

    Returns:
    float: log(input_number)
    """

    return math.log(input_number)

def power(input_number : float, power : float) -> float:
    """
    Raise input_number by power e.g. when you raise 4.0 by 2 you get 16.0.
    
    Parameters:
    input_number: The input number.
    power: What power to raise the input number by.
    
    Returns:
    float: input_number ** power
    """

    return input_number ** power





