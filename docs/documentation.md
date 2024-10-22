# Rufus Documentation

## Introduction

**Rufus** is an intelligent web data extraction tool designed to prepare web data for Retrieval-Augmented Generation (RAG) agents. It intelligently crawls websites based on user-defined prompts, extracts relevant data, and synthesizes it into structured documents suitable for RAG systems.

## Components

### 1. Crawler

- **Purpose:** Navigates through the website starting from the base URL, following links up to a specified depth, and collects URLs to be scraped.
- **File:** `RufusClient/crawler.py`

### 2. Parser

- **Purpose:** Extracts relevant data (e.g., FAQs, pricing) from the fetched HTML content based on the user's instructions.
- **File:** `RufusClient/parser.py`

### 3. Synthesizer

- **Purpose:** Uses OpenAI's GPT models to synthesize the extracted data into a structured format (e.g., JSON) suitable for RAG systems.
- **File:** `RufusClient/synthesizer.py`

### 4. Client

- **Purpose:** Serves as the entry point, coordinating the crawling, parsing, and synthesizing processes.
- **File:** `RufusClient/client.py`

### 5. API

- **Purpose:** Provides a RESTful interface for developers to interact with Rufus.
- **File:** `api/main.py`

## Usage

### Using RufusClient Directly

1. **Import RufusClient:**

    ```python
    from RufusClient.client import RufusClient
    ```

2. **Initialize and Scrape:**

    ```python
    instructions = "Find information about HR policies and FAQs."
    client = RufusClient(user_prompt=instructions)
    documents = client.scrape("https://www.sfgov.com")
    print(documents)
    ```

### Using the API

1. **Start the API Server:**

    ```bash
    uvicorn api.main:app --reload
    ```

2. **Access API Documentation:**

    Open your browser and navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to access the interactive Swagger UI documentation. You can test API endpoints directly from here.

3. **Send a Scrape Request:**

    ```bash
    curl -X POST "http://127.0.0.1:8000/scrape" -H "Content-Type: application/json" -d '{"url": "https://www.sfgov.com", "instructions": "Find information about HR policies and FAQs."}'
    ```

## Testing

Run the test suite using PyTest:

```bash
pytest