## main.py - this is a ChatGPT tool called "Doug"
# Doug is here to guide you. Please do not fear Doug. Doug is your friend.
# Doug always refers to themselves in third person.

import pdb

from os import environ
from sys import exit, path
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

from langchain.vectorstores import Chroma

from langchain.embeddings.openai import OpenAIEmbeddings

## Custom Module Path Injection
# inject our module path so we can resolve 'import' statements later
path.insert(0, './data/modules')

## Custom Modules
from SignalHandler  import signalHandler
from PdfLoader      import pdfLoader

print("   - - - - - - - - DOUG V1.0 : AI ASSISTANT - - - - - - - -\n")

## Initialization #############################################################
# load our .env file, which has our OPENAI_API_KEY
load_dotenv()

osSignalHandler = signalHandler()

dougLLMModel=environ.get("OPENAI_LLM_MODEL")

if environ.get("OPENAI_API_KEY") is None:
    print("ERROR: OpenAI API Key is not set")
    exit(1)

# to get a list of models, run utils/get-openai-models.py
if dougLLMModel is None:
    print("WARN: OPENAI_LLM_MODEL not set, defaulting to 'gpt-3.5-turbo-0301'")
    dougLLMModel="gpt-3.5-turbo-0301"

# temperature adjusts the 'randomness', with values closer to 0.0 intended to make the output more reproduceable
dougLLM = ChatOpenAI(model_name=dougLLMModel, temperature=0.4)

# initialize our chat message memory for our interactive chat session
dougWorkingMemory = ConversationBufferMemory(memory_key="history", input_key="input")
dougSummaryMemory = ConversationSummaryMemory(llm=dougLLM, input_key="input")

dougPersistentMemory = 'data/db'
dougEmbedding = OpenAIEmbeddings()

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
dougDB = Chroma(persist_directory=dougPersistentMemory, embedding_function=dougEmbedding)

###############################################################################
print("\n [ commands: .quit - exit this cli app, .debug - pdb console ] ")

documents = None

while True:
    osSignalHandler.reset_signal()
    userInquiry = input('\n: ')

    if userInquiry:
        cmd = userInquiry.split()[0]

        if cmd == ".exit" or cmd == ".quit":
            dougDB.persist()
            exit(0)

        if cmd == ".debug":
            pdb.set_trace()
            continue

        if cmd == ".pdf":
            if len(userInquiry.split()) > 1:
                try:
                    arg = " ".join(userInquiry.split()[1:])
                    dougPdf = pdfLoader(persistdb=dougDB, path=arg, signalHandler=osSignalHandler)

                    dougPdf.addPathToQueue(arg)
                    dougPdf.processQueue()
                    dougPdf.storeQueue()

                except Exception as error:
                    print("  ~> " + str(error))

            else:
                print("-> pdf command requires one path argument")

            continue

        if cmd == ".search":
            if len(userInquiry.split()) > 1:
                try:
                    query = " ".join(userInquiry.split()[1:])
                    retriever = dougDB.as_retriever(search_type="mmr")

                    documents = retriever.get_relevant_documents(query)
                    print("-> returned " + str(len(documents)) + " documents")

                except Exception as error:
                    print("  ~> " + str(error))
            else:
                print("-> search command requires something to search for")

            continue

        if cmd == ".docs":
            try:
                docsAvailable = len(documents)
                if docsAvailable < 1:
                    print("-> no documents found, try searching first")
                    continue

                if len(userInquiry.split()) > 1:
                    arg = int(userInquiry.split()[1])
                    if arg > docsAvailable:
                        print("-> index out of range")
                        continue
                    else:
                        print(documents[arg])
                else:
                    print("-> " + str(docsAvailable) + " documents available")

            except Exception as error:
                print("  ~> " + str(error))

            continue

        ## Main LLM Block - reach out to LLM with inquiry
        try:
            result = dougChain.run(input=userInquiry)
            if result:
                print(result)
            else:
                print("ERROR: LLM did not respond")
        except:
            print("ERROR: error during run(), bailing until we write proper error recovery")
            exit(1)
