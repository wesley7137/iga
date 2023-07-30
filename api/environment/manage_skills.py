import json
import chromadb
import openai
from dotenv import load_dotenv
import os
# Load the environment variables from the .env file
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
openai.api_key = api_key

client = chromadb.Client()

collection = client.get_or_create_collection("skills_vector_db")

def get_embedding(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']

def update_skills(name,path,description, filename='api/environment/skills_db.json'):
    
    new_object = {
        "name": name,
        "content": {
            "path": path,
            "description": description.split("\n")
        }
    }
    
    with open(filename, 'r') as f:
        data = json.load(f)
    
    data.append(new_object)
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)

    collection.add(
    embeddings=[
        get_embedding(description),
    ],
    metadatas=[
        {"description": description},
    ],
    documents=[name],
    ids=[name],
    )
    
    
    return new_object
    
def query_skills(query):
    query_result = collection.query(
            query_embeddings=[get_embedding(query)],
            n_results=1,
        )
    return query_result
    
def initialize_skills():
    with open('api/environment/skills_db.json', 'r') as f:
        data = json.load(f)
    return data


# test usage
# add_skill(new_object)
