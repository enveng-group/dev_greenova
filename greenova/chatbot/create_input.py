# This file creates inputs for the chatbot to respond with.
# Please run this command at most once, to avoid duplicate data.

from data.chatdata_pb2 import ChatBotResponse
from data.chatdata_pb2 import ChatBotPrompts

# Iterates though all people in the AddressBook and prints info about them.
def Create(prompt_list, id, prompt_txt, response_txt):
    r = prompt_list.responses.add()
    r.id = id
    r.prompt = prompt_txt
    r.response = response_txt
    return r

def ListPrompts(prompt_list): 
    for response in prompt_list.responses:
        print("Response ID:      ", response.id)
        print("Response Prompt:  ", response.prompt)
        print("Response Response:", response.response)

# Read existing data...
prompt_list = ChatBotPrompts()
prompt_list_fname = "./data/chatdata-serialised.protobin"

# Delete it, we are starting new
f = open(prompt_list_fname, "w")
f.close()

# Write all our information...
p_hello = Create(prompt_list, 1, "Hello", "Hello, I am Greenova's chatbot! How can I help you today?")





ListPrompts(prompt_list)

# Write the new address book back to disk.
with open(prompt_list_fname, "wb") as f:
    f.write(prompt_list.SerializeToString())
    f.close()