
EXAMPLES = """
1) user : What is twice the product of 4 and 5?
   assistant : {"observation" : "",
                "thought" : "First find the sum of 4 and 5. We will use this calculation later
                             to come up with the final answer.",
                "status" : "IN-PROGRESS"}
               tool_call - add_two_numbers(number_1 = 4, number_2 = 5)
   tool : 9.0
   assistant : {"observation" : "The sum of 4 and 5 somes out to be 9.0."
                "thought" : "Now lets multiply 9.0 by 2. This will give us the required answer.",
                "status" : "IN-PROGRESS"}
               tool_call - multiply_two_numbers(number_1 = 2, number_2 = 9.0) 
   tool : 18.0
   assistant : {"observation" : "The product of 2 and 9.0 is 18.0. This means we have the final answer.",
                "thought" : "",
                "status" : "FINISHED"}
                tool_call - None

2) user : Divide 4.7 by 0 and add 1 to it.
   assistant : {"observation" : "",
                "thought" : "First, we divide 4.7 with 0. We will then add 1 to output of this operation.",
                "status" : "IN-PROGRESS"} 
               tool_call - divide_two_numbers(number_1 = 4.7, number_2 = 0)
   tool : Cannot divide by zero.
   assistant : {"observation" : "It seems that division by zero is not possible.",
                "thought" : "",
                "status" : "UNABLE TO PROCESS USER REQUEST"}
               tool_call - None

3) user : Is 35 + 43 greater than 100?
   assistant : {"observation" : "",
                "thought" : "First, we add 35 and 43. Then we can compare the sum with 100",
                "status" : "IN-PROGRESS"} 
               tool_call - add_two_numbers(number_1 = 35, number_2 = 43)
   tool : 78.0
   assistant : {"observation" : "The sum is 78.0.",
                "thought" : "Let's compare 78.0 to 100. But there is no external tool to for
                             comparison operation.",
                "status" : "UNABLE TO PROCESS USER REQUEST"}
               tool_call - None

4) user : Find the softmax value of value at position 3 in array [2.6,-4.5,1.3].
   assistant : {"observation" : "",
                "thought" : "The equation of softmax looks as follows -

                            \text{softmax}(z_i) = \frac{e^{z_i}}{\sum_{j=1}^{n} e^{z_j}} 

                            Here:                           
                            z_i  is the raw score number at i-th position.
                            e is Euler’s number (approximately 2.718).
                            The denominator is sum of exponentials of all the individual numbers in the given vector.

                            We need to get the exponential of each number in guven vector. We start with 2.6.
                            ",
                "status" : "IN-PROGRESS"} 
               tool_call - power(number_1 = 2.718, power = 2.6)
   tool : 13.46
   assistant : {"observation" : "The exponential of 2.6 is 13.46.",
                "thought" : "Let's get exponential of -4.5.",
                "status" : "IN-PROGRESS"}
               tool_call - power(number_1 = 2.718, power = -4.5)
   tool : 0.01
   assistant : {"observation" : "The exponential of -4.5 is 0.01",
                 "thought" : "Let's get exponential of 1.3.",
                 "status" : "IN-PROGRESS"}
                tool_call - power(number_1 = 2.718, power = 1.3)
   tool : 3.66
   assistant : {"observation" : "The exponential of 1.3 is 3.66.",
                 "thought" : "Now to calculate the denominator of the softmax equation, we need to summ all exponentials i.e. 13.46 + 0.01 + 3.66. We start by summing 13.46 and 0.01",
                 "status" : "IN-PROGRESS"}
                tool_call - add_two_numbers(number_1 = 13.46, number_2 = 0.01)
   tool : 13.47
   assistant : {"observation" : "The exponential of 13.46 and 0.01 is 13.47.",
                "thought" : "Now, let's add 13.47 to 3.66.",
                "status" : "IN-PROGRESS"}
                tool_call - add_two_numbers(number_1 = 13.47, number_2 = 3.66)
   tool : 17.13
   assistant : {"observation" : "The sum of 13.47 and 3.66 is 17.13.",
                "thought" : "The denominator of softmax equation is 17.13. We need to find softmax value of number at position 3 which is 1.3.
                                The exponential of 1.3is already calculated as turns out to be 3.66. So we neeed to divide 3.66 by 17.13.",
                "status" : "IN-PROGRESS"}
                tool_call - divide_two_numbers(number_1 = 3.66, number_2 = 17.13)
   tool : 0.21
   assistant : {"observation" : "The final answer is 0.21",
                "thought" : "",
                "status" : "FINISHED"}
                tool_call - None

"""




