# Configuring the RAG Multi-Agent Application for Additional Users

At the November 12th, 2024 meeting of Agile Leadership Journey AI cohort Charlie Fleet demonstrated a retrieval augmented generation (RAG) multi agent application.  The application is based on an experimental framework, Swarm, provided by OpenAI.

The multi agent application is implemented in Python and uses Tavily for web search. After our meeting Charlie was kind enough to share the Github repository where the source is stored, and encouraged cohort participants to review and potentially refactor the end user parameters out of the main python script so it could easily be configured by other end users.

Charlie is using a Windows-based computer designed for gaming, so the machine has a discrete graphics processor and a healthy amount of RAM. From our discussion it was unclear the degree to which the system relied on the graphics processor, so my first experiment was to see whether I could replicate Charlie's Anaconda setup and get the application working on a Macbook.

## The Basic Process

Since the code 'as is' included specific directory paths on Charlie's computer, the process we followed to install, refactor and run the multi agent RAG application was:

1. Setup Anaconda and install required python packages
2. Fork & clone the [github repository](https://github.com/amikiste/Source) containing Charlie's agent code
3. Register, obtain API keys for [OpenAI](https://openai.com) and [Tavily](https://app.tavily.com/home), and purchase API tokens for OpenAI  
4. Fix the Swarm Result object defect by editing Swarm's __init__.py file
5. Extract user-specific parameters to a configuration file
6. Edit the main script to use the configuration files
7. Load some PDF files into the PDF source directory so they can be converted to an Index
8. Load and run the script in a Python IDE

## Test Machine Configuration

Since I travel frequently, like to do data science work while on the road, and am relatively frugal with respect to purchasing computer equipment, I travel with a 2019-era Macbook Pro 16. It  has 64Gb of RAM, a 2.4 Ghz Intel i9 processor with 8 cores ant 16 threads, an AMD Radeon 5500 GPU, and 2TB of disk space. Since Apple's move to their own silicon, high end Macbooks based the Intel platform can be purchased for less than $1,300 as of late 2024.  

## Six Easy Pieces? ...or not  

Downloading and installing Anaconda, no problem. Forking & cloning Charlie's Github repository, easy peasy. Registering & generating API keys, piece of cake. Installing required python packages with pip? That's where my troubles began.

## The "not so easy pieces"

When I tried to install Swarm from a terminal window command line, I received an error message about a package dependency conflict between the `tenacity` (needs version < 9) and `instructor` packages (needs version > 9). My default setup had `tenacity` version 9 installed so I had to uninstall it and replace it with an earlier version.

After resolving the package dependency conflict, my next challenge was "which IDE to use?" As an experienced R user, I've been working in RStudio for over 8 years. One of its best features is its integration with Git / Github. One can create an R project in the root directory of a git repository, and it's very easy to make small changes and frequently commit them to the repository. I've done some basic python programming, but it always seemed to be easier to do my work in R. Therefore, my introduction to Anaconda was a rude awakening.  

Why?the Anaconda Navigator presents 10 different options for development environments, including RStudio! Not wanting to confuse myself by attempting to run Charlie's python script in RStudio, I decided to shut down Anaconda and use Visual Studio Code directly.  

Once Visual Studio loaded, I observed packages used in Charlie's RAG application weren't accessible in the IDE. From a terminal window command line I could use `pip show` to confirm installation of the required packages, and I hypothesized that I needed to run VS Code within Anaconda to get access to these packages.

## Success At Last!

Once I had a working Anaconda / Visual Studio setup, I noticed that Charlie used a package called `dotenv` and a specific function, `load_dotenv()` to load environment variables from a configuration file called `.env`.   Rather than building custom code to track the user parameters I could simply assign them in the `.env` file, load them with `load_dotenv()` and access them wherever needed in Charlie's script.

I extracted the following variables into a template file so they could be published to Git / Github and referenced without potentially overwriting an end user's actual `.env` file.

    OPENAI_API_KEY="Secret OpenAI Key"
    TAVILY_API_KEY="Secret TAVILY Key"
    WEATHER_API_KEY="Secret Weather Key"
    FIREWORKS_API_KEY="a Fireworks API key goes here"
    INDEX_PERSIST_DIR="./ragStorage"
    SOURCE_PDF_DIR="./ragInputDocs"

The variables creating the RAG index persistent storage location and source PDF file location are configured to use relative pathing from the repository root directory, so a new end user can keep the content associated with the multi-agent RAG application in the repository tree, rather than random locations on the user's local storage.

Finally I created a `.gitignore` file to keep certain files from being pushed to the remote repository, especially the `.env` file since once it's configured it contains keys that should not be published to a private remote repository, let alone a public one.

Now, to download, configure, and run the application, all one needs to do is:

1. Setup Anaconda and install required python packages
2. Fork & clone the [github repository](https://github.com/amikiste/Source) containing Charlie's agent code
3. Register, obtain API keys for [OpenAI](https://openai.com) and [Tavily](https://app.tavily.com/home), and purchase API tokens for OpenAI  
4. Fix the Swarm Result object defect by editing Swarm's `__init__.py` file (see below for help finding the file)
5. Copy .env.template to .env and edit the content
6. Copy some PDF files into the PDF source directory that is listed in your .env file so they can be converted to an Index
7. Load an IDE within Anaconda, and select your IDE's version of "run python file in Terminal"

If one edits the environment variables, loads the script in an IDE from the Anaconda Navigator, and runs it in a terminal session, it will generate output that looks like this:

![](./images/configuringRAGAgent-01.png)

## Finding the Install Location of Swarm

To complete step 4 above, one needs to know the location of Swarm on the local computer. There are at least two techniques for this. 
First, from a terminal window, `pip <packagename> show` will print descriptive information about a package, including the directory into which the package was installed. Second, within a Python script one can import a package, and then use `print()` as follows:

    import swarm
    print(swarm.__file__)