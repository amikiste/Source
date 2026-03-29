
import os
from swarm import Swarm, Agent, Result
from dotenv import load_dotenv
from tavily import TavilyClient

######## Setup Variables #######
#Hardcode context variables for now
context_variables = {"name": "Charlie", "user_id": 8675309}

# Load Env variables
# centralize all user parameters in .env file, such as API keys
load_dotenv()

######## Initialize Tavily Client #######
tavily_client = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))


############################
###### Seting up RAG #######
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import StorageContext, load_index_from_storage
#from llama_index.embeddings.fireworks import FireworksEmbedding
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
from llama_index.llms.openai import OpenAI

# Keys for the APIs are retrieved from the .env file, including OPENAI_API_KEY
# and FIREWORKS_API_KEY. Do NOT push versions of the .env file that contain
# any end user keys to Github. Instead, make a local copy of your .env file
# using .env_yourName which will not be included in the files to be published
# to the remote repository due to the content of the .gitignore file 

#Step 1: Set up the embedding model and LLM model.
#Settings.embed_model = FireworksEmbedding()
Settings.embed_model = OpenAIEmbedding()
Settings.llm = OpenAI("gpt-4o")

# Step 2: Load the local pdf files in the directory referenced by SOURCE_PDF_DIR in
# the .env file and create the index for retrieval.

PERSIST_DIR = os.getenv("INDEX_PERSIST_DIR")
pdf_filepath = os.getenv("SOURCE_PDF_DIR")

def load_or_create_rag_index(pdf_filepath):
    if not os.path.exists(PERSIST_DIR):
        os.makedirs(PERSIST_DIR)
        documents = SimpleDirectoryReader(pdf_filepath).load_data()
        index = VectorStoreIndex.from_documents(documents)
        print("DEBUG: Index created and persisted.")
        index.storage_context.persist(persist_dir=PERSIST_DIR)
    else:
        storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
        # load index
        index = load_index_from_storage(storage_context)
        print("DEBUG: Index loaded from persistence.")
    return index

print("DEBUG: Creating Rag Index")
# pdf_filepath = "C:\\Users\\charl\\OneDrive\\My Documents\\HomeBusiness\\BearPeak\\Clients\\Agile Leadership Journey\\AI Cohort\\RAG Docs"

rag_index = load_or_create_rag_index(pdf_filepath)
print("DEBUG: Creating Query Engine")
query_engine = rag_index.as_query_engine()

#Step 3: Create a query engine on the top of the rag_index.
def query_rag(query_str):
    print("DEBUG: Entering query_rag function")
    print(f"DEBUG: Query Request: {query_str}")
    response = query_engine.query(query_str)
    #print(f"DEBUG: Query Response: {response}")
    return str(response)

# Provide Instructions to the two Agents we are building
# context_variables = {} comment out because this line overwrites previous settings 

def triage_agent_instructions(context_variables):
    name = context_variables.get("name", "User")
    print(f"DEBUG: Instructions for our Agent are being setup for user={name}")
    return """You are a triage agent.
    You are a useful agent who answers many questions consisely. You should
    search the web if asked information you don't know.
    Anytime you have maths to do use the calculate function unless it doesn't return
    a good result and then just search the web for an answer.
    Anytime you have questions about authors, an AI article, document, or published document use the 'query_rag' function.
    Greet the user by name ({name}).
    """

def rag_agent_instructions(context_variables):
    return """You are a RAG agent. Always use the `query_rag` function to retrieve information for any answers before sending the information back to the triage agent.
    """

def math_agent_instructions(context_variables):
    return """You are an agent who does math, really well. You pass your information back to the triage agent.
    """

def search_agent_instructions(context_variables):
    return """You are an agent who searches the web for outside information. You pass your information back to the triage agent.
    """
def account_details_agent_instructions(context_variables):
    return """You are an agent who returns any information you have about the account of the current user.
    """

#Actually define the handoff to rag function
def handoff_to_rag_agent():
    print ("DEBUG: Sending control to the rag_agent")
    return Result(agent=rag_agent)

def handoff_to_math_agent():
    print ("DEBUG: Sending control to the math_agent")
    return Result(agent=math_agent)

def handoff_to_search_agent():
    print ("DEBUG: Sending control to the search_agent")
    return Result(agent=search_agent)

def handoff_to_account_details_agent():
    print ("DEBUG: Sending control to the account_details_agent")
    return Result(agent=account_details_agent)

def transfer_back_to_main():
    """Call this function if a user is asking about a topic that is not handled by the current agent."""
    return Result(agent=triage_agent)

def calculate(x,y,operator):
    print(f"DEBUG: Entering Calculate Function with arguments(" + x + "," + y +"," + operator + ")")
    x=float(x)
    y=float(y)
    if operator == '+':
        return x + y
    elif operator == '-':
        return x - y
    elif operator == '*':
        return x * y
    elif operator == '/':
        if y != 0:
            return x / y
        else:
            return "Error: Division by zero"
    else:
        return "Error: Invalid operator"
def web_search(query):
    print(f"DEBUG: Performing web search for: {query}")
    return tavily_client.search(query)

def print_account_details():
    user_id = context_variables.get("user_id", None)
    name = context_variables.get("name", None)
    print(f"Account Details: {name} {user_id}")
    return "Success"

# At the current time, your IDE may show errors on the “Result” class because the Swarm source
# code on the Github repository has not registered this class in the initialization (I'm not sure why),
# but you can easily add it to the __init__.py file in the root directory of the Swarm package:
#from .core import Swarm
#from .types import Agent, Response, Result
#__all__ = ["Swarm", "Agent", "Response", "Result"]

#Define the two agents with the instructions and functions.
triage_agent = Agent(
    name="Triage Agent",
    instructions=triage_agent_instructions
    )
triage_agent.functions.append(handoff_to_rag_agent)
triage_agent.functions.append(handoff_to_math_agent)
triage_agent.functions.append(handoff_to_search_agent)
triage_agent.functions.append(handoff_to_account_details_agent)

rag_agent = Agent(
    name="RAG Agent",
    instructions=rag_agent_instructions,
    functions=[query_rag]
    )
rag_agent.functions.append(transfer_back_to_main)

#agent_instances = [
#    create_agent(f"Agent {i}", agent_template.instructions)
#    for i in range(1, 4)  # Create 3 instances
#]

math_agent = Agent(
    name="Math Agent",
    instructions=math_agent_instructions,
    functions=[calculate]
    )
math_agent.functions.append(transfer_back_to_main)

search_agent = Agent(
    name="Search Agent",
    instructions=search_agent_instructions,
    functions=[web_search]
    )
search_agent.functions.append(transfer_back_to_main)

account_details_agent = Agent(
    name="Account Details Agent",
    instructions=account_details_agent_instructions,
    functions=[print_account_details]
    )
search_agent.functions.append(transfer_back_to_main)

#Initialize swarm client
client = Swarm()

def run_swarm_app():
    print("Welcome to the RAG Swarm App!")
    name = context_variables.get("name", "User")
    current_agent = triage_agent
    messages = []
    while True:
        user_input = input(f"{name}: ")
        if user_input.lower() == "exit":
            break
        messages.append({"role": "user", "content": user_input})
        response = client.run(
            agent=current_agent,
            messages=messages,
            )
        print(f"{response.agent.name}: {response.messages[-1]['content']}")
        messages = response.messages
        current_agent = response.agent

if __name__ == "__main__":
    run_swarm_app()
