This source code allows a user to run an OpenAI Swarm agent connecting to multiple agents and functionality.

It offers these key features:

1. Creation of main agent
2. Creation of sub agents for multiple functions
3. Example of a RAG creation and retrieval
4. Example of a web search using Tavily
5. Example of a local calculate function
6. Example of a local config data request
7. Continuous user input until you exit

#################################
#Required Packages to download in console
##################################

1. pip install git+https://github.com/openai/swarm.git
2. pip install tavily-python
3. pip install llama-index llama-index-embeddings-fireworks
4. pip install docx2txt
5. pip install torch transformers python-pptx Pillow
6. pip install python-dotenv

#################################
#Bug Resolution
##################################

At the current time, your IDE may show errors on the “Result” class because the Swarm source code on the Github repository has not registered this class in the initialization (I'm not sure why),  but you can easily add it to the __init__.py file in the root directory of the Swarm package:

1. from .core import Swarm
2. from .types import Agent, Response, Result
3. __all__ = ["Swarm", "Agent", "Response", "Result"]

# Configuring the Application for a New User

A more detailed discussion of how to configure this application to run in a local user's Anaconda environment is accessible at [Configuring the RAG Multi-Agent Application for New Users](./configuringNewUsers.md).
