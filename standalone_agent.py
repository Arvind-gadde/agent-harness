from openai import OpenAI

from dotenv import load_dotenv

load_dotenv()


#initialize the client
client = OpenAI()

response = client.chat.completions.create(
    model= "gpt-5-mini",
    messages=[
        {"role" : "user","content" : "what is grpc"},
        {"role" : "assistant","content" : "gRPC (gRPC Remote Procedure Calls) is an open-source, high-performance RPC framework originally developed by Google. It lets you define services and call methods on remote servers as if they were local functions, with automatic generation of client and server code."}
    ]
)

print(response.choices[0].message.content)
