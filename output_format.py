
from pydantic import BaseModel, ValidationError
from typing import List


response_format = {
    "type": "json_schema",
    "json_schema":{
        "name": "output_schema",
        "description": "Schema to follow for each step output",
        "strict": True,
        "schema": {
                "type": "object",
                "properties":{
                    "observation": {
                                "type":"string",
                                "description":"Observation made for the output received from tool_call."
                            },
                    "thought": {
                                "type":"string",
                                "description":"Thought on what action should be taken next and the rationale behind the decision."
                    },
                    "status": {
                                "type":"string",
                                "description":"Status for current step. If the task is completed then status='FINISHED'. If it is in progress, then status='IN-PROGRESS' and if there is no logical way to find a solution then status='UNABLE TO PROCESS USER REQUEST'",
                                "enum":["IN-PROGRESS","FINISHED","UNABLE TO PROCESS USER REQUEST"]
                    }     
                },
                "required":["observation","thought","status"],
                "additionalProperties":False
            }
    }
}

# Define types that match the JSON Schema using pydantic models
class Step(BaseModel):
    observation : str
    thought : str
    status : str
