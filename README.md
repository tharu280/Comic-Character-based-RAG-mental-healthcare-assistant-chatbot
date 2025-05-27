# Comic-Character-based-RAG-mental-healthcare-assistant-chatbot

# Uncle Iroh Chatbot 

A conversational chatbot API inspired by **Uncle Iroh** from *Avatar: The Last Airbender*.  
This chatbot uses Google Gemini generative AI, FAISS vector stores, and HuggingFace embeddings via LangChain to provide wise, gentle, and poetic responses in the style of Uncle Iroh.

---

## Features

- **Multi-user support:** Separate chatbot instances for each user to maintain individual conversation context.
- **Contextual memory:** Remembers the last 6 messages to maintain coherent conversations.
- **Knowledge retrieval:** Uses FAISS vector stores with three distinct knowledge bases:
  - Iroh’s teachings and philosophy
  - Emotional and mental well-being insights
  - Rational and scientific ideas
- **Personalized prompt templates:** Emulates Uncle Iroh’s gentle, poetic, and wise tone.
- **FastAPI backend:** Lightweight and scalable REST API for easy integration.

---

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Google API key with access to Gemini-1.5-flash model
- FAISS vector store indexes for knowledge bases (`vdbs/iroh`, `vdbs/mental`, `vdbs/philosophy`)
- `.env` file containing your Google API key as `GOOGLE_API_KEY`

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/uncle-iroh-chatbot.git
cd uncle-iroh-chatbot
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

Create a `.env` file in the root directory and add:

```
GOOGLE_API_KEY=your_google_api_key_here
```

5. Ensure that FAISS vector stores are downloaded or generated and placed in the `vdbs/` directory.

---

## Usage

Run the FastAPI server locally with:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.

### API Endpoint

- **POST** `/chat`

#### Request body JSON schema:

```json
{
  "user_name": "YourName",
  "message": "Hello, Uncle Iroh!"
}
```

#### Response JSON schema:

```json
{
  "reply": "Uncle Iroh's thoughtful response..."
}
```

---

## Project Structure

- `main.py` — FastAPI app and endpoint definitions
- `UncleIrohChatbot` class — encapsulates chatbot initialization, retrieval, memory, and prompt logic
- `vdbs/` — local FAISS vector store directories (required)
- `.env` — environment variables

---

## How It Works

1. **Initialization:** Loads Google API key and sets up the Gemini chat model.
2. **Embeddings & Retrieval:** Uses HuggingFace embeddings to query FAISS vector stores for relevant documents across three categories.
3. **Memory:** Maintains a window of recent conversation turns for context.
4. **Prompt Construction:** Combines retrieved knowledge and conversation history into a prompt styled after Uncle Iroh.
5. **Generation:** Sends prompt to Google Gemini and parses output.
6. **Multi-user Management:** Maintains separate chatbot instances keyed by user name for parallel conversations.

---

## Customization

- Adjust the memory window size by changing `k` in `ConversationBufferWindowMemory`.
- Update prompt templates to tweak Uncle Iroh’s persona or add more context.
- Add additional knowledge bases by extending the FAISS retrievers and prompt logic.

---

## Troubleshooting

- **Missing API key:** Ensure your `.env` file includes a valid `GOOGLE_API_KEY`.
- **Vector store not found:** Make sure the FAISS indexes are correctly downloaded/created in `vdbs/`.
- **Performance issues:** The Google Gemini model may incur latency depending on your network.

---

## License

This project is licensed under the MIT License.

---

## Contact

For questions or contributions, please open an issue or submit a pull request.

---

*“Sharing tea with a fascinating stranger is one of life’s true delights.” — Uncle Iroh*
