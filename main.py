import os
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate
from langchain.schema import SystemMessage, HumanMessage
from langchain.memory import ConversationBufferWindowMemory
from langchain_core.runnables import RunnableMap
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, HumanMessagePromptTemplate

app = FastAPI()


class ChatRequest(BaseModel):
    user_name: str
    message: str


class UncleIrohChatbot:
    def __init__(self, nephew_name: str):
        load_dotenv()
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        if not self.google_api_key:
            raise ValueError(
                "Missing GOOGLE_API_KEY in environment variables.")

        self.model = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.7,
            google_api_key=self.google_api_key
        )

        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.retriever_iroh = FAISS.load_local(
            "vdbs/iroh", self.embedding_model, allow_dangerous_deserialization=True
        ).as_retriever(search_type="similarity", search_kwargs={"k": 1})

        self.retriever_mental = FAISS.load_local(
            "vdbs/mental", self.embedding_model, allow_dangerous_deserialization=True
        ).as_retriever(search_type="similarity", search_kwargs={"k": 3})

        self.retriever_philosophy = FAISS.load_local(
            "vdbs/philosophy", self.embedding_model, allow_dangerous_deserialization=True
        ).as_retriever(search_type="similarity", search_kwargs={"k": 3})

        self.memory = ConversationBufferWindowMemory(
            k=6,
            return_messages=True,
            memory_key="history",
            input_key="question"
        )

        self.prompt = ChatPromptTemplate.from_messages([
            SystemMessage(content="""
You are Uncle Iroh from Avatar: The Last Airbender—gentle, wise, loving, and poetic. Speak with warmth and calm, using metaphor and gentle humor. Your words carry the wisdom of a lifetime and a soothing presence.

Keep your response thoughtful and not too long. Focus on providing comfort and insight with gentle simplicity, like a sip of perfectly brewed tea.
"""),
            MessagesPlaceholder(variable_name="history"),
            HumanMessagePromptTemplate.from_template("""
You may draw on the following wisdom if the conversation calls for deeper guidance:

- Iroh’s teachings and philosophy:
{iroh}

- Emotional support and mental well-being insights:
{mental}

- Rational or scientific ideas:
{philosophy}

If the user's message is light-hearted or casual, you may respond with kindness and simplicity, without referencing the additional context.

Question:
{question}
""")
        ])

        self.chain = (
            RunnableMap({
                "iroh": lambda x: "\n".join([doc.page_content for doc in self.retriever_iroh.invoke(x["question"])]),
                "mental": lambda x: "\n".join([doc.page_content for doc in self.retriever_mental.invoke(x["question"])]),
                "philosophy": lambda x: "\n".join([doc.page_content for doc in self.retriever_philosophy.invoke(x["question"])]),
                "question": lambda x: x["question"],
                "history": lambda x: self.memory.load_memory_variables(x)["history"]
            })
            | self.prompt
            | self.model
            | StrOutputParser()
        )

        intro_message = f"Your name is Iroh. You are speaking with your dear nephew {nephew_name}. Talk like Uncle Iroh from Avatar the Last Airbender."
        self.memory.chat_memory.add_message(
            SystemMessage(content=intro_message))
        first_message = f"How are you, my dear nephew {nephew_name}?"
        self.memory.chat_memory.add_message(HumanMessage(content="..."))
        self.memory.chat_memory.add_message(
            SystemMessage(content=first_message))

    def ask(self, query: str) -> str:
        start = time.time()
        result = self.chain.invoke({"question": query})
        self.memory.save_context({"question": query}, {"output": result})
        end = time.time()
        print(f"[Latency] {end - start:.2f} seconds")
        return result


bots = {}


@app.post("/chat")
def chat(req: ChatRequest):
    user = req.user_name.strip()
    message = req.message.strip()
    if not user or not message:
        raise HTTPException(
            status_code=400, detail="user_name and message are required")

    if user not in bots:
        bots[user] = UncleIrohChatbot(nephew_name=user)

    bot = bots[user]
    response = bot.ask(message)
    return {"reply": response}
