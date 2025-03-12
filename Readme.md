#react #agents #llms #ai #demo

# REACT Agentic Pattern Demo

This repository demonstrates how to use the **REACT** (Reason, Act, and Observe) agentic pattern with OpenAI's API to perform complex mathematical operations such as **softmax**, **dot product**, etc. The agent formulates and carries out a structured plan for each user request. The agent has access to function calls for basic arithmetic operations such as  **add**, **subtract**, **multiply**, **divide**, and **power**.

## Features:
- Uses the **REACT** pattern to reason about the task, act on it, and observe the result.
- Can perform **arithmetic operations** via tool calling.
- Allows the addition of **user requests** in a `user_prompts.json` file.
- Uses the OpenAI API for model interaction.

## Requirements:
To use this repository, you'll need to install some Python dependencies and set up your environment.

### Dependencies:
- `openai`
- `pydantic`
- `python-dotenv`

### Setting Up:

1. **Clone the Repository:**
   First, clone the repository to your local machine:
   ```bash
   git clone https://github.com/saketd403/react-demo.git
   cd react-demo
   ```

2. **Create a Virtual Environment (optional but recommended):**
   It's good practice to use a virtual environment to keep dependencies isolated:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Windows, use `venv\Scripts\activate`
   ```

3. **Install the Dependencies:**
   Install the required Python packages by running:
   ```bash
   pip install -r requirements.txt
   ```

   This will install the necessary dependencies: `openai`, `pydantic`, and `python-dotenv`.

4. **Set Up OpenAI API Key:**
   You'll need to provide your OpenAI API key to interact with OpenAI models.

   - **Option 1:** Create a `.env` file in the project directory and add your OpenAI key like so:
     ```
     OPENAI_API_KEY=your-openai-api-key-here
     ```

   - **Option 2:** Alternatively, export the API key directly in your terminal:
     ```bash
     export OPENAI_API_KEY=your-openai-api-key-here  # For Linux/macOS
     set OPENAI_API_KEY=your-openai-api-key-here    # For Windows (Command Prompt)
     ```

5. **Add User Prompts in `user_prompts.json`:**
   User-specific prompts can be added in the `user_prompts.json` file. The JSON file should contain a list of tasks or operations you'd like the agent to perform.

   Example `user_prompts.json`:
   ```json
    {
        "user_requests":["Find the dot product of [2,3,5] and [3,4,5]",
                        "Find the dot product of [2,3] and [3,4,5]",
                        "Subtract 9 from 10 and multiply the result by 7."
                        ]
    }
   ```

   You can define different tasks (such as arithmetic operations or complex calculations) and pass them to the agent in this format.

### Running the Code:

To run the demo, execute the following command:

```bash
python main.py --model <model_name> --temperature <temperature_value> --num_steps <max_iterations>
```

#### Arguments:
- `--model`: The OpenAI model to use (e.g., `"gpt-4o"`, `"gpt-4o-mini"`).
- `--temperature`: The temperature for generating responses (e.g., `0.3`), where lower values are more deterministic.
- `--num_steps`: The maximum number of iterations for the REACT process (i.e., how many times the model will try to reason and act before stopping, even if the task isn't complete).

Example:
```bash
python main.py --model "gpt-4" --temperature 0.3 --num_steps 10
```

### How the REACT Process Works:
1. **Reason**: The model breaksdown the task and reasons about the next logical action.
2. **Act**: The model performs action which is just a call to a specific tool.
3. **Observe**: The model observes the result of the action (tool-call) and iterates the process if needed, within the `num_steps` limit.

### REACT Step

REACT breaks down the task into smaller, manageable steps. Each step consists of following -
1. **Status** : Current status of the workflow. It can be `FINISHED` or `IN-PROGRESS` based on completion status. The LLM would set this to `UNABLE TO PROCESS USER REQUEST` if the LLM could not process user's request for some reason.
2. **Observation** : The observation made after receiving tool output in previous step.
3. **Thought** : The rationale behind the next logical action. Based on this, function/tool is selected for tool call.
4. **tool-call** : OpenAI tool call with correctly formatted input arguments.  

### Output schema

At each step, the LLM responds in following json schema -

    
        "schema": {
                "type": "object",
                "properties":{
                    "observation": {
                                "type":"string"                                },
                    "thought": {
                                "type":"string"
                            },
                    "status": {
                                "type":"string"
                                "enum":["IN-PROGRESS","FINISHED","UNABLE TO PROCESS USER REQUEST"]
                            }    

                    }
            }

### Example of a Task:
When running the code, the user may try to perform tasks like:
- **dot product**: Multiply the corresponsing elements and sum them up.
- **softmax**: Breaking down the softmax formula to simple addition, divison and multiplication. Step by step carry out the operations and produce the required output.

### Troubleshooting:
- **API Key Issues**: Ensure that the `OPENAI_API_KEY` is correctly set either in the `.env` file or exported as an environment variable.
- **Package Installation**: If you encounter issues installing packages, ensure you're using the correct Python environment and that `pip` is up to date.
- **Model Errors**: Make sure that the model name you provided is available with your OpenAI API key.

---

## Example Output:

If you use the `user_prompts.json` file mentioned above and run the script with a command like:

```bash
python main.py --model "gpt-4o" --temperature 0.3 --num_steps 10
```

The agent may process the requests and produce results like:

```
User request : Subtract 9 from 10 and multiply the result by 7.

Status : IN-PROGRESS 
Observation :  ""
Thought : First, subtract 9 from 10. This will give us the intermediate result, which we will then multiply by 7.
Action : subtract_two_numbers

Status : IN-PROGRESS 
Observation : The result of subtracting 9 from 10 is 1.0. 
Thought : Now, let's multiply the result 1.0 by 7 to get the final answer.
Action : multiply_two_numbers

Status : FINISHED 
Observation : The product of 1.0 and 7 is 7.0. This means we have the final answer.
Thought :

Final answer : 7.0
```