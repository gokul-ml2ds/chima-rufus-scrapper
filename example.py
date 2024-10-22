# example.py
from RufusClient.client import RufusClient
import json

def main():
    instructions = "Get information about variance."
    client = RufusClient(user_prompt=instructions)
    documents = client.scrape("https://medium.com/@rbhatia46/essential-probability-statistics-concepts-before-data-science-bb787b7a5aef")
    print(json.dumps(documents, indent=4))

if __name__ == "__main__":
    main()