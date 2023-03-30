## main.py
## This is a ChatGPT tool called "Doug"
# Doug is here to guide you. Please do not fear Doug. Doug is your friend.
# Doug always refers to themselves in third person.

import pdb

from os import environ
from sys import exit
from dotenv import load_dotenv
from pathlib import Path

# Import the langchain core
import langchain

from langchain import PromptTemplate

# Use OpenAI LLM
from langchain.chat_models import ChatOpenAI

from langchain.cache import SQLiteCache
langchain.llm_cache = SQLiteCache(database_path=".langchain.db")

from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory, CombinedMemory, ConversationSummaryMemory


## Initialization #############################################################
# load our .env file, which has our OPENAI_API_KEY
load_dotenv()

dougLLMModel=environ.get("OPENAI_LLM_MODEL")

if environ.get("OPENAI_API_KEY") is None:
    print("ERROR: OpenAI API Key is not set")
    exit(1)

if dougLLMModel is None:
    print("WARN: OPENAI_LLM_MODEL not set, defaulting to 'gpt-3.5-turbo-0301'")
    dougLLMModel="gpt-3.5-turbo-0301"

# to get a list of models, run utils/get-openai-models.py
# temperature adjusts the 'randomness', with values closer to 0.0 intended to make the output more reproduceable
dougLLM = ChatOpenAI(model_name=dougLLMModel, temperature=0.4)

# initialize our chat message memory for our interactive chat session
dougWorkingMemory = ConversationBufferMemory(memory_key="history", input_key="input")
dougSummaryMemory = ConversationSummaryMemory(llm=dougLLM, input_key="input")

dougMainMemory = CombinedMemory(memories=[dougWorkingMemory, dougSummaryMemory])

# TODO: load saved prompt from 'yaml' file
dougPrompt = Path('./data/prompt/doug-v1.prompt').read_text()

try:
    dougTemplate = PromptTemplate(
        input_variables=["history", "input"],
        template=dougPrompt
        )
except:
    print("Unable to create template")
    pdb.set_trace()
    exit(1)

dougChain = ConversationChain(llm=dougLLM, memory=dougMainMemory, prompt=dougTemplate)

###############################################################################
print("   - - - - - - - - DOUG V1.0 : AI ASSISTANT - - - - - - - -")
print(" [ commands: .quit - exit this cli app, .debug - pdb console ] ")

while True:
    userInquiry = input('\n: ')

    if userInquiry:
        if userInquiry == ".exit" or userInquiry == ".quit":
            exit(0)

        if userInquiry == ".debug":
            pdb.set_trace()
            continue

        try:
            result = dougChain.run(input=userInquiry)
            if result:
                print(result)
            else:
                print("ERROR: LLM did not respond")
        except:
            print("ERROR: error during run(), bailing until we write proper error recovery")
            exit(1)
