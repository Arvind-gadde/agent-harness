from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

#here we will mantain the chat history context for memory of llm so it can go back and forth
messages = []


#step 2 we will have a user input for input and a quit mechanism
while True:
    user_input = input("you: enter your question , type quit to close the application ")
    if user_input.strip().lower() == "quit":
        break
    
    #so we will store the first message in context arrray
    messages.append({"role" : "user" , "content" : user_input})


    #response initialization and all 
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=messages,
    )

    #grabbing the result ffrom ai
    reply = response.choices[0].message.content

    #also appending the ai message into context array
    messages.append({"role" : "assistant" , "content" : reply})
    print("bot : " , reply)




