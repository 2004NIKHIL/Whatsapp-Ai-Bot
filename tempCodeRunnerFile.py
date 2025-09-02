from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from dotenv import load_dotenv
from langchain_groq import ChatGroq
import os





load_dotenv()
llm = ChatGroq(
    groq_api_key=os.getenv("GROQ_API_KEY"),  # .env me variable ka naam
    model="llama-3.3-70b-versatile")


def main():
    tools =[]
    agent_executor = create_react_agent(llm, tools)  # ✅ Groq llm use karo



    print("Welcome! I'm your AI Assistant. Type 'quit' to exit.") 
    print("You can ask me to perfrom calculations or you can talk to me.")

    while True:
        user_input = input("\nYou : ").strip()
        if user_input == "quit":
            break

        print("\nAssistant: ",end="")
        for chunk in agent_executor.stream(
            {"messages": [HumanMessage(content=user_input)]}


        ):
            if "agent" in chunk and "messages" in chunk["agent"]:
                for message in chunk["agent"]["messages"]:
                    print(message.content,end="")
        print()

if __name__== "__main__":
    main()
