# Spacy Entity Extraction API

This provides a FastAPI-based API for extracting entities and nouns from text using the Spacy natural language processing library.

## Features

- Extract named entities from text
- Optional extraction of nouns
- Optional extraction of noun chunks
- Swagger documentation available at `/docs` endpoint

## Requirements

- Python 3.6+
- FastAPI
- Uvicorn
- Spacy
- Pydantic

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/SpacyAPI.git
   cd SpacyAPI
   ```

2. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

3. Download the Spacy model:
   ```
   python -m spacy download en_core_web_sm
   ```

## Usage

1. Start the server:

   ```
   python main.py
   ```

   The server will start on `http://0.0.0.0:4747`.

2. Access the Swagger documentation by navigating to `http://localhost:4747/docs` in your web browser.

3. Use the `/extract_entities` endpoint to extract entities from text. You can use the Swagger UI or send a POST request to `http://localhost:4747/extract_entities` with a JSON payload.

Example payload:

```json
{
  "text": "Apple Inc. is planning to open a new store in New York City.",
  "extract_nouns": true,
  "extract_noun_chunks": true
}
```

Example response:

```json
{
  "entities": [
    {
      "text": "Apple Inc.",
      "label": "ORG"
    },
    {
      "text": "New York City",
      "label": "GPE"
    }
  ],
  "nouns": ["Inc.", "store", "City"],
  "noun_chunks": ["Apple Inc.", "a new store", "New York City"]
}
```

## API Endpoints

### POST /extract_entities

Extract entities from the given text using Spacy.

**Request Body:**

- `text` (string, required): The input text to extract entities from
- `extract_nouns` (boolean, optional): Whether to extract nouns from the text
- `extract_noun_chunks` (boolean, optional): Whether to extract noun chunks from the text

**Response:**

- `entities` (array): List of extracted entities with their labels
- `nouns` (array, optional): List of extracted nouns (if requested)
- `noun_chunks` (array, optional): List of extracted noun chunks (if requested)

## Development

This project uses FastAPI for the web framework and Spacy for natural language processing. The main logic is contained in the `main.py` file.

To modify the API or add new features:

1. Edit the `main.py` file
2. Update the Swagger documentation by modifying the FastAPI app and endpoint descriptions
3. If you add new dependencies, update the `requirements.txt` file

## License

[MIT License](https://opensource.org/licenses/MIT)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
