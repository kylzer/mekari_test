
# Mekari Assignment Test

This is a challenge test from Mekari.  
An Fraud Knowledge Agent

# Requirements
- Docker
- Docker Compose
**NOTES** : .env is not ignored for test purpose
# Specification
For this challenge, I use Macbook Pro M1 with 8GB RAM and 512GB Storage.

That's the reason I don't use GPU on Docker Compose for Ollama.

# Model
- nomic-embed-text-v1.5 for Embedding
- GPT-OSS 20B for Generative


# Tool List
- fraud_knowledge


# Library & Frameworks
```
fastapi==0.115.9
langchain==0.3.25
langchain-openai==0.3.18
python-dotenv==1.1.0
rich==14.0.0
uvicorn==0.34.2
```

# Installation
Clone the project

```bash
  git clone https://github.com/kylzer/mekari_test.git
```

Go to the project directory

```bash
  cd mekari_test
```

Up Docker Container

```bash
  docker-compose -f docker-compose.yml up -d --build
```

Logging Container  
Gradio
```
docker logs -f mekari_test-gradio
```
Embedding Service Logs
```
  docker logs -f embedding_service
```
Weaviate Logs
```
  docker logs -f mekari_test-weaviate-1 
```

# Usage
```
1. Up Docker Container
2. Open Gradio in a browser
3. If there is no changes, you can access by open [Here](http://localhost:7860/)
4. You can do indexing or upsert the document first.
5. You can parse the .csv into .sql (if the table and headers is same, then it will concat)
6. After "Upserting Successful", you can try Retrieval
```

# Photo
TBD
# Video
TBD