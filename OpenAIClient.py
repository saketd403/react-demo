import openai
from openai import OpenAI
from functools import partial
from logger import setup_logger

# Create a logger specific to this module
logger = setup_logger('OpenAIClient')

class OpenAIClient():

    def __init__(self,model,
                num_requests=1,
                temperature=1.0,response_format=None,
                tools=None,tool_choice="auto",
                parallel_tool_calls=False):

        client_kwargs = {
            "model" : model,
            "n" : num_requests,
            "max_completion_tokens" : 5000,
            "response_format" : response_format
        }

        if(tools is not None):
            tool_kwargs = {
                            "tools":tools,
                            "tool_choice":tool_choice,
                            "parallel_tool_calls":parallel_tool_calls
                        } 
            client_kwargs.update(tool_kwargs)


        client = OpenAI()

        self.completion = None

        if(model in ["o1-mini","o1","o3-mini"]):

            self.completion = partial(
                func=client.chat.completions.create,
                reasoning_effort="medium",
                **client_kwargs,
                )

        else:

            self.completion = partial(
                client.chat.completions.create,
                temperature=temperature,
                top_p=1.0,
                **client_kwargs
            )

    def generate_response(self,messages,response_format=None):

        try:
            if(self.completion):

                return self.completion(messages=messages,response_format=response_format)
            
            return None
        except Exception as e:
            logger.error(f"Following exception occured while")

