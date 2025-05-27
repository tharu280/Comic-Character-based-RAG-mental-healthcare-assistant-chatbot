import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, AIMessage, SystemMessage


load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.7,
    google_api_key=google_api_key
)
chat_history = []

nephew_name = input("Uncle Iroh: What is your name my dear nephew? ")
intro_message = f"Your name is Iroh. You are speaking with your dear nephew {nephew_name}. Talk like Uncle Iroh from Avatar the Last Airbender."
system_message = SystemMessage(
    content=intro_message)
chat_history.append(system_message)
first_message = f"How are you, my dear nephew {nephew_name}?"
chat_history.append(AIMessage(content=first_message))
print(f"Uncle Iroh: {first_message}")
while True:

    query = input(f"Nephew {nephew_name}: ")
    if query.lower() == "exit":
        break
    chat_history.append(HumanMessage(content=query))

    result = model.invoke(chat_history)
    response = result.content
    chat_history.append(AIMessage(content=response))

    print(f"Uncle Iroh : {response}")
