from helper_functions import get_args, get_method_list
from OpenAIClient import OpenAIClient
from ReActAgent import ReactAgent
import tool_methods
from tools import Tool
from system_prompt import REACT_SYSTEM_PROMPT_TEMPLATE 
from examples import EXAMPLES

import json
import inspect
from dotenv import load_dotenv

from logger import setup_logger

# Create a logger specific to this module
logger = setup_logger('main')

def get_tools():

    function_list = get_method_list(tool_methods)
    tools={}
    for func in function_list:
        tools[func.__name__] = Tool(func)

    return tools

def create_tool_description(tools):

    tool_description = ""

    for i,(name,tool) in enumerate(tools.items()):
        tool_description += f"{str(i+1)}. **{tool.name}**: {tool.description} \n"

    return tool_description



def create_sys_prompt(tools,prompt_template,examples):

    tool_description = create_tool_description(tools)

    sys_prompt = prompt_template.format(examples=examples, external_tools=tool_description) 

    logger.info(f" System prompt:\n + {sys_prompt}")

    return sys_prompt

def run(args):

    tools = get_tools()

    tool_calls = [tool.tool_call for name,tool in tools.items()]

    # Setup OpenAI client
    client = OpenAIClient(
                        args.model,
                        num_requests=1,
                        temperature=args.temperature,
                        tools=tool_calls,
                        tool_choice="auto", # could set this to 'required' but last response will just be a string
                        parallel_tool_calls=False # only one function call at a time.
                        )

    sys_prompt = create_sys_prompt(tools,REACT_SYSTEM_PROMPT_TEMPLATE,EXAMPLES)

    with open("user_prompts.json","r") as file:
        input_json = json.load(file)

    agent = ReactAgent(
                client,
                sys_prompt,
                num_steps=args.num_steps,
                tools=tools
                )

    for user_request in input_json["user_requests"]:

        try:

            result = agent.generate_response(user_request)
            if(result):
                logger.info(f"Final answer : {result}")

        except Exception as e:

            logger.error(f"The following error occured while processing the user request : {user_request}")
            logger.error(f"\n{e}")



if __name__ == "__main__":

    load_dotenv()
    args = get_args()
    run(args)