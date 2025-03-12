
import inspect
import re

from logger import setup_logger

# Create a logger specific to this module
logger = setup_logger('tools')

type_mappping = {
                    "float" : "number",
                    "str" : "string",
                    "int" : "number"
                }

def get_param_description(docstring,parameters):

    param_names = [param.name for param in parameters.values()]

    param_description = {}

    lines = docstring.split('\n')

    for line in lines:

        # Regular expression to match the pattern
        match = re.match(r"(\w+):\s*(.*)", line)

        if match:
            # Extract 'arg' and 'description'
            arg = match.group(1)
            description = match.group(2)

            if(arg in parameters):           
                param_description[arg] = description

    return param_description

def convert_to_tool_format(func,description):
    """
    Converts a Python function to OpenAI API tool format, including parameter descriptions.
    
    Parameters:
    func (function): The Python function to convert.
    
    Returns:
    dict: A dictionary in the format required by the OpenAI API.
    """
    
    # Extract function name
    function_name = func.__name__
    
    # Extract function docstring
    docstring = inspect.getdoc(func)
    
    # Extract function parameters
    signature = inspect.signature(func)
    parameters = signature.parameters
    
    # Prepare the parameters structure for the tool format
    properties = {}
    required_params = []
    
    # Extract parameter descriptions
    param_descriptions = get_param_description(docstring,parameters)
    
    for param, details in parameters.items():

        # Type of the parameter (usually inferred from the annotation or default to string)
        param_type = str(details.annotation.__name__) if details.annotation is not inspect.Parameter.empty else "str"
        data_type = type_mappping[param_type]

        # Add to properties
        properties[param] = {
            "type": data_type,
            "description": param_descriptions.get(param, "No description available.")  # Add description if available
        }
        
        # If the parameter has no default, it's required
        #if details.default is inspect.Parameter.empty:
        required_params.append(param)
    
    # Construct the tool format structure
    tool_format = {
        "type": "function",
        "function": {
            "name": function_name,
            "description": description if description else "",
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required_params,
                "additionalProperties": False
            },
            "strict": True
        }
    }

    logger.info(f"\n {tool_format}")

    return tool_format


class Tool:

    def __init__(self,func):

        self.func = func
        self.name = func.__name__

        self.description = None
        self.tool_call = None

        self.description = self.get_description()

        self.tool_call = self.get_tool_call()

    def get_tool_call(self):

        if(self.tool_call is None):
            self.tool_call = convert_to_tool_format(self.func,self.description)

        return self.tool_call
        

    def get_description(self):

        if(self.description is None):

            docstring = inspect.getdoc(self.func)

            end_index = docstring.find("Parameters:")

            if(end_index==-1):
                raise Exception(f"Docstring for function {self.name} is not properly written.")

            self.description = docstring[:end_index].strip()

        return self.description

    def execute(self,func_args):

        for param,value in func_args.items():

            func_args[param] = float(value)

        result = self.func(**func_args)
    
        return result
