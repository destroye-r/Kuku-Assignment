[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![Python Version](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)

[![Ollama](https://img.shields.io/badge/Ollama-black?style=flat&logo=ollama&logoColor=white)](https://ollama.com/)


# IPC Legal Chatbot

## Overview

- The IPC Legal Chatbot is a sophisticated Streamlit-based application designed to democratize access to legal information, specifically concerning the Indian Penal Code (IPC). It empowers users to quickly find simple and accurate explanations of IPC sections through an intuitive chat interface.

- At its core, this chatbot utilizes a Retrieval-Augmented Generation (RAG) pipeline. This cutting-edge architecture combines the precision of information retrieval with the generative power of Large Language Models (LLMs). It leverages FAISS for efficient similarity search, Sentence-Transformers for converting text into meaningful embeddings, and Ollama to run the powerful Llama 3.1 model locally for generating concise and relevant legal explanations.

- Data Coverage: The chatbot's knowledge base specifically covers IPC sections ranging from **121A to 511.**

## Features

- Intelligent IPC Explanations: Get simple, easy-to-understand explanations for complex Indian Penal Code sections.

- Retrieval-Augmented Generation (RAG): Combines efficient document retrieval with advanced LLM generation for highly accurate and contextual answers.

- Local LLM Integration: Powered by the Llama 3.1 model, run locally via Ollama, ensuring data privacy and reducing reliance on cloud APIs.

- FAISS for Vector Search: Utilizes Facebook AI Similarity Search (FAISS) for lightning-fast retrieval of relevant IPC sections from your knowledge base.

- Sentence Embeddings: Employs Sentence-Transformers to create dense vector representations of legal texts and user queries.

- Interactive Streamlit UI: A clean and user-friendly web interface for a seamless conversational experience.

- Dynamic Data Handling: Automatically generates and caches FAISS index and metadata on the first run, optimizing subsequent performance.

- Comprehensive Logging: Detailed logging (to console and file) for monitoring and debugging, configured via logging_config.yaml.

## Getting Started

You have multiple options to run the IPC Legal Chatbot: an Automated Setup (highly recommended for ease), a Manual Setup for more control, or a Docker Deployment for containerization.

**Prerequisites**

Ensure you have the following installed on your system:

- Git: For cloning the repository.

[Download & Install Git](https://git-scm.com/downloads)

- Python 3.8+: The application requires Python 3.8 or a newer version.

[Download Python](https://www.python.org/downloads/)

- Ollama: This is crucial for running the llama 3.1 LLM locally.

[Install Ollama](https://ollama.com/download) - Follow the official instructions for your operating system.

- Docker: (Only if you choose Docker Deployment) For building and running the containerized application.

[Install Docker Engine](https://docs.docker.com/engine/install/) 

## 1. Clone the Repository

Begin by cloning the project repository to your local machine:

```
git clone https://github.com/ashankgupta/ipc_legal_chatbot.git
cd ipc_legal_chatbot
```

## 2. Set Up Ollama and Llama 3.1 Model

- The chatbot relies on the Llama 3.1 model running via Ollama.

- Ensure Ollama is running: Make sure the Ollama server is active in your background. You can usually start it by simply installing it or running ollama serve if it's not set to auto-start.

- Download the llama 3.1 model: Pull the specific model required by the application:

```
ollama run llama3.1
```
- This command will download the model if it's not already present and then start an interactive session. You can simply close this session (/bye) once the download is complete.

## Running the Application

You have three options to run the IPC Legal Chatbot:

### Option A: Automated Setup (Recommended for Ease)

This is the simplest way to get started. These scripts will handle repository cloning, Ollama installation (if missing), Llama 3.1 model download, Python virtual environment setup, dependency installation (using uv for speed), and finally launch the application.

#### For Linux / macOS users:

Download the install.sh file from the latest GitHub Release of this repository.

- Open your terminal, navigate to the download directory.

- Make the script executable:
```
chmod +x install.sh
```
Run the script:
```
./install.sh
```

#### For Windows users:

- Download the install.bat file from the latest GitHub Release of this repository.

- Locate the downloaded file in File Explorer.

- Double-click on install.bat to run it.

- Important Note: For best results, ensure Git and Python 3.8+ are already installed and accessible in your system's PATH. The .bat script relies on these being pre-installed.

### Option B: Manual Setup (Local Development)

Choose this option if you prefer manual control or if the automated script encounters issues.

- Install uv (Fast Python Package Manager):
```
pip install uv

Ensure uv is in your system's PATH. This is typically managed by pip.
```

Install Python Dependencies:

#### Create and activate a virtual environment (recommended)
```
python3 -m venv venv
source venv/bin/activate  # On Linux/macOS
venv\Scripts\activate   # On Windows
```

#### Install Python packages from requirements.txt
```
uv pip install -r requirements.txt
```
#### Run the Streamlit application:
```
streamlit run app.py
```

Your application should open in your default web browser at http://localhost:8501.


### Option C: Run with Docker (Recommended for Deployment)

Using Docker encapsulates all dependencies and ensures a consistent environment, making it ideal for deployment.

Build the Docker Image:
Navigate to the root directory of your project (where the Dockerfile is located) and run the following command:
```
docker build -t ipc_legal_chatbot .
```
This command will:

- Build the Docker image named ipc_legal_chatbot.

- Install all necessary system packages and Python dependencies.

- Copy your application code into the image.


Run the Docker Container:
Once the image is built, you can run the application using:

```
docker run -p 8501:8501 legal_chatbot
```

- docker run: Starts a new container from the legal_chatbot image.
- -p 8501:8501: Maps port 8501 of your local machine to port 8501 inside the container, where Streamlit is running.

After running the command, open your web browser and navigate to http://localhost:8501. You should see the IPC Legal Chatbot interface.

## Project Structure

```
ipc_legal_chatbot/
├── app.py                      # Main Streamlit application entry point
├── src/                        # Source code for modular components
│   ├── __init__.py             # Python package initializer
│   ├── data_processing.py      # Handles loading, parsing, and chunking of legal data
│   ├── rag_pipeline.py         # Implements the core Retrieval-Augmented Generation logic
│   ├── utils.py                # Contains various utility functions
│   └── config.py               # Stores configuration settings and constants
├── data/                       # Directory for legal data and generated artifacts
│   ├── legal_data.jsonl        # The raw legal knowledge base (JSON Lines format)
│   ├── ipc_faiss.index         # (Auto-generated) FAISS index for efficient retrieval
│   └── ipc_metadata.json       # (Auto-generated) Metadata associated with the FAISS index
├── requirements.txt            # Lists all Python dependencies
├── .env                        # Environment variables (e.g., API keys, model paths)
├── logging_config.yaml         # Configuration file for Python's logging module
├── Dockerfile                  # Docker instructions to build the container image
├── .dockerignore               # Specifies files/directories to exclude from Docker build context
└── README.md                   # This comprehensive project documentation
```

## Usage

- Open the App: Access the application in your web browser (typically at http://localhost:8501).

- Enter Your Query: Type a question or statement related to Indian Penal Code sections into the input field. Examples:

```
"What is IPC section 302?"

"Explain crimes against children under IPC."

"What are the punishments for theft?"
```

- Get Explanations: The chatbot will process your query, retrieve the most relevant IPC sections from its knowledge base, and generate a simplified explanation using the llama 3.1 model

## Dependencies

- Python 3.8+

- Streamlit: For the interactive web interface.

- Sentence-Transformers: For generating embeddings.

- FAISS-CPU: For efficient vector similarity search.

- PyTorch (CPU): Underlying framework for Sentence-Transformers.

- Ollama Python Library: To interact with the local Ollama server.

- Other utilities: langchain, pydantic, etc.

Refer to requirements.txt for the complete and exact list of Python dependencies.

## Frequently Asked Questions (FAQs)

#### Q What is the IPC Legal Chatbot, and what kind of information does it provide?

```
The IPC Legal Chatbot is an AI-powered Streamlit application designed to simplify sections of the Indian Penal Code (IPC). It gives you clear, concise, and contextual explanations for IPC sections, specifically covering 121A to 511. It's a tool for quick understanding, not a substitute for professional legal advice.
```

#### Q Why do I need to install Ollama separately? Can't the chatbot just work on its own?

```
The chatbot uses llama 3.1, a powerful Large Language Model (LLM), to generate its explanations. Ollama is crucial because it lets you run this LLM directly on your local machine. This keeps your data private and usually gives you faster responses without needing external cloud services. Your chatbot connects to your local Ollama server, which hosts the llama 3.1 model
```

#### Q How can I update the legal data the chatbot uses, or add new IPC sections?

```
You can update the chatbot's knowledge by modifying or replacing the legal_data.jsonl file located in the data/ directory of your project. The application is designed to automatically re-generate its FAISS index (ipc_faiss.index) and metadata (ipc_metadata.json) when it detects changes or missing files in data/ on startup. After updating legal_data.jsonl, simply restart the application (or rebuild/rerun your Docker container) for the changes to take effect.
```

## Notes

- Data Format: Ensure that legal_data.jsonl is correctly formatted with legal sections that the RAG pipeline can effectively process.

- Index Generation: The ipc_faiss.index and ipc_metadata.json files are automatically created and cached in the data/ directory upon the first run of the application. This significantly speeds up subsequent startups.

- Configuration: Adjust environment variables in the .env file for custom model paths, logging levels, or other application-specific settings.

- Logging: Application logs are configured via logging_config.yaml and are outputted to ipc_legal_chatbot.log as well as the console, aiding in debugging and monitoring.

## Contributing

- Contributions, issues, and feature requests are highly welcome! Feel free to check the issues page.

## License

- This project is open-source and available under the MIT License.

