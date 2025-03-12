from enums import Role
import json
from output_format import response_format, Step
from pydantic import BaseModel, ValidationError
from typing import List

from logger import setup_logger

# Create a logger specific to this module
logger = setup_logger('REACT')


class ReactAgent:

    def __init__(self,
                client,
                sys_prompt,
                num_steps,
                tools,
                verbose=True
                ):

        self.client = client
        self.sys_prompt = sys_prompt
        self.num_steps = num_steps
        self.tools = tools
        self.verbose=verbose

        self.message_history = [
            self.build_prompt(Role.SYSTEM.value,self.sys_prompt)
        ]

    def llm_call(self,messages,response_format):

        response = self.client.generate_response(messages=messages,
                                response_format=response_format)

        return response

    def build_prompt(self,role,message):

        return {"role":role,
                "content":message}

    def call_function(self, name, func_args):

        result = None

        if(name in self.tools):

            tool = self.tools[name]

            try:
                result = tool.execute(func_args)
            except Exception as e:
                result = f"Error while executing tool : {e}"

        return result

    def check_llm_message(self,message):

        message = json.loads(message)
                
        try:
            # Parse and validate the response content
            step = Step.model_validate(message)
        except ValidationError as e:
            # Handle validation errors
            print(e.json())
            raise

        if(self.verbose):
            logger.info(f"Status : {step.status} \n")
            logger.info(f"Observation : {step.observation} \n")
            logger.info(f"Thought : {step.thought} \n")

        return step

    def generate_response(self,usr_msg) -> float:

        # Generate response from generator
        self.message_history.append(
            self.build_prompt(Role.USER.value,usr_msg)
        )

        logger.info(f"User request \n {usr_msg}")

        result=None
        finished=False
        for step in range(self.num_steps):

            try:

                completion = self.llm_call(self.message_history,response_format)

                response = completion.choices[0]

                if(response.finish_reason=="tool_calls"):

                    self.message_history.append(response.message)

                    self.check_llm_message(response.message.content)

                    tool_call = response.message.tool_calls[0]
                    name = tool_call.function.name

                    if(self.verbose):
                        logger.info(f"Action : {name}")

                    func_args = json.loads(tool_call.function.arguments)

                    result = self.call_function(name, func_args)

                    if(not result):
                        raise Exception("Function not found")

                    self.message_history.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": str(result)
                        })

                elif(response.finish_reason=="stop"):

                    step = self.check_llm_message(response.message.content)

                    if(step.status=="UNABLE TO PROCESS USER REQUEST"):
                        raise Exception("Error from LLM : UNABLE TO PROCESS USER REQUEST")

                    if(step.status=="FINISHED"):
                        finished=True
                        break

            except Exception as e:

                logger.error(f"The following exception occured at step {str(step+1)}")
                logger.error(f"\n{e}")
                raise

        if(not finished):
            logger.info(f"Maximum number of iterations reached for user query {usr_msg}")
            return None

        return result



