import json

def get_system_prompt():
    
    knowledgeUrlsString = json.dumps(knowledgeUrls)
    knowledgeCommandsString = json.dumps(knowledgeCommands)
    
    thePrompt = """
    Your job is to help the user navigate the website. The user may wish to go to specific URL or ask to scroll the page, sort the data, etc.
    You are given a list of URLs related to disaster recovery, government programs, financial analyses,
    and other related topics.
    You are also given a list of available commands.
    Based on the user’s input or keywords, determine what action to take, navigate to the given URL or execute the desired command.
    Choose the most appropriate action by matching the user's input to one of the descriptions. Here is the list of URLs:\n###\n
    """ + knowledgeUrlsString + """\n###Here is the list of available commands:\n""" + knowledgeCommandsString
    
   
    print(thePrompt)
    return thePrompt

with open("urls.json", "r") as file:
    knowledgeUrls = json.load(file)

with open("commands.json", "r") as file:
    knowledgeCommands = json.load(file)


functions = [
    {
                "type": "function",
                "name": "navigate_to_url",
                "description": "Navigate to the specified URL",
                "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The URL to navigate to",
                    },
                },
                "required": ["url"],
            },
    },
    {
                "type": "function",
                "name": "execute_command",
                "description": "Execute command to adjust display as desired, scroll, sort, etc.",
                "parameters": {
                "type": "object",
                "properties": {
                    "cmd": {
                        "type": "string",
                        "description": "The command to execute",
                    },
                },
                "required": ["cmd"],
            },
    }
]


if __name__ == "__main__":
    from openai import OpenAI
    client = OpenAI()

    test_data = [
       { "prompt": "go to publik asistanc", "expectedResult": { "args": {"url": "/recovery-programs/public-assistance"}, "name": "navigate_to_url"}},
       # { "prompt": "go to individual assistance", "expectedResult": { "args": {"url": "/recovery-programs/individual-assistance"}, "name": "navigate_to_url"}},
       # { "prompt": "scroll up", "expectedResult": { "args": {"cmd": "scrollUp"}, "name": "execute_command"}},
       # { "prompt": "scroll down", "expectedResult": { "args": {"cmd": "scrollDown"}, "name": "execute_command"}},
       # { "prompt": "whats the size of the earth?", "expectedResult": None }
    ]    

    system_prompt = get_system_prompt()
    for test in test_data:
        user_prompt = test["prompt"]
        expectedResult = test["expectedResult"]
        
        print("Testing user prompt: " + user_prompt)

        completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
            ],
            functions=functions
        )

        function_call = completion.choices[0].message.function_call
        #url = json.loads(function_call.arguments)["url"]
        #print(url)
        print(function_call)
        if expectedResult is not None:
            parsed_fc = json.loads(function_call.arguments)
            print(parsed_fc)
            print(expectedResult)
            ## expect the name to be the same
            assert function_call.name == expectedResult["name"]
            ## expect the args to be the same
            assert parsed_fc == expectedResult["args"]
        else:
            resp = completion.choices[0].message.content
            print("Response: " + resp)
