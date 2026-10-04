from openai import OpenAI
from dotenv import load_dotenv
import subprocess
import json
import os


load_dotenv()
client = OpenAI()

model = "gpt-5-mini"

SYSTEM_PROMPT = """You are a coding agent running in the user's terminal.
You can list files, read files, write files, and run shell commands.
Use your tools to complete the user's task, then briefly summarize what you did.
The working directory is the folder the user launched you from."""



#SO LETS BUILD SOME TOOLS FOR code editor agent calls so it crud the code files

#firs list tools list the all the files in dir if not provided dir name it will take the current
def list_files(path="."):
    entries= []
    # It uses a conditional expression (ternary operator) to check if the item is a folder (entry.is_dir()). If it is a folder, it adds a trailing slash (/) to the name; if it's a file, it adds nothing (""). The final name is added to the entries list.

    for entry in os.scandir(path):
        entries.append(entry.name + ("/" if entry.is_dir() else ""))


    #Sorts the list alphabetically (sorted(entries)) and combines them into a single block of text separated by new lines ("\n".join(...)).
    return "\n".join(sorted(entries)) or "(empty directory)"



#it  is just a rading file tool 
def read_file(path):
    with open(path , "r" ,encoding="utf-8" ) as f:
        return f.read()

def write_file(path, content):
    with open(path , "w" , encoding="utf-8") as f:
        f.write(content)
        return f"saved {path} ({len(content)}) characters"

def run_command(command):
    answer = input(f"run '{command}'? [y/n]")

    if answer.strip().lower() != "y":
        return "user denied to run this command"


    result = subprocess.run(
        command , shell=True , capture_output=True , text=True , timeout=120
    )
    # • What the parameters mean:
	# • shell=True: Allows the command to be run through the system shell (like bash or cmd).
	# • capture_output=True: Intercepts and saves the terminal results so Python can read them.
	# • text=True: Returns the results as a clean Python text string instead of raw bytes.
	# • timeout=120: Forces the command to shut down if it hangs or takes longer than 2 minutes.

    output = (result.stdout + result.stderr).strip()

    return output or f"(no output , exit code {result.returncode})"


#will have all the tools in single array so it will be usefull place 
TOOLS = {
    "list_file" : list_files,
    "read_file" : read_file,
    "write_file" : write_file,
    "run_command" : run_command,
}


TOOL_SCHEMAS = [
    {
        "type" : "function",
        "function":{
            "name" : "list_files",
            "description" : "list the files in a directory. folders with /.",
            "parameters" : {
                "type" : "object",
                "properties" : {
                    "path":{
                        "type" : "string",
                        "description" : "directory to list , eg '.'"
                    }
                }
                ,"required" : ["path"]
            },
        },
    },
    {    
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "Read a text file and return its contents.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string", 
                    "description": "Path of the file to read"
                }
            },
            "required": ["path"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Create or overwrite a text file with the given content.",
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string", 
                    "description": "Path of the file to write"
                },
                "content": {
                    "type": "string", 
                    "description": "Full contents of the file"
                }
            },
            "required": ["path", "content"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "run_command",
        "description": "Run a shell command and return its output. The user approves it first.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string", 
                    "description": "The shell command to run"
                }
            },
            "required": ["command"]
        }
    }
},  
]

def run_tool(tool_call):
    name = tool_call.function.name
    args = json.loads(tool_call.function.arguments)
    print(f" [Executing Tool] -> {name}({args})")
    try:
        return str(TOOLS[name](**args))
    except Exception as error:
        return f"Error: {error}"


messages = []
def run_agent(messages):
    while True:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOL_SCHEMAS,
        )

        message = response.choices[0].message
        messages.append(message)

        # No tool calls means the model is done and answered in plain text
        if not message.tool_calls:
            return message.content

        for tool_call in message.tool_calls:
            result = run_tool(tool_call)
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                }
            )

def main():
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    print("Mini agent ready. Type 'exit' to quit.")
    
    while True:
        user_input = input("\nYou: ")
        if user_input.strip().lower() in ("exit", "quit"):
            break
            
        messages.append({"role": "user", "content": user_input})
        reply = run_agent(messages)
        print(f"\nAgent: {reply}")

if __name__ == "__main__":
    main()
