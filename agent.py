from openai import OpenAI
import json
from tools import read_file,write_file,run_command,list_files
from tool_schemas import tools

def get_tool(tool_name,args):
    tool_dic={
        "read_file":read_file,
        "write_file":write_file,
        "list_files":list_files,
        "run_command":run_command
    }

    return tool_dic[tool_name](**args)

def tool_handler(msg):
    responses=[]
    for tool_call in msg.tool_calls:
        tool_name=tool_call.function.name
        args=json.loads(tool_call.function.arguments)
        result=get_tool(tool_name=tool_name,args=args)

        responses.append({
            "role":"tool",
            "content":json.dumps(result),
            "tool_call_id":tool_call.id
        })
    return responses


def model_init(api_key,base_url)->object:
    model=OpenAI(api_key=api_key,base_url=base_url)
    return model

def coder(messages,model,model_name,reasoning="low"):
    response=model.chat.completions.create(messages=messages,model=model_name,reasoning_effort=reasoning,tools=tools)

    while True:
        msg=response.choices[0].message
        if not msg.tool_calls:
            return msg.content 
        messages.append(msg.model_dump(exclude_none=True))
        tool_responses=tool_handler(msg)
        messages.extend(tool_responses)

        response=model.chat.completions.create(messages=messages,model=model_name,reasoning_effort=reasoning,tools=tools)