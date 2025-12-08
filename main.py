from groq import Groq
from dotenv import load_dotenv
import os


class ConversationAgent:
    def __init__(self):
        load_dotenv()
        self.client = Groq(api_key=os.environ["GROQ_KEY"])
        self.initiate_history()


    @staticmethod
    def read_file(file_path):
        with open(file_path , "r") as file:
            return file.read()


    def initiate_history(self):
        self.history = [
            {
                "role": "system",
                "content": ConversationAgent.read_file("./context.txt")
            }]


    def update_history(self, role, content):
         self.history.append(
                {
                    "role": role,
                    "content": content,
                })


    def ask_llm(self, user_interaction):

        self.update_history(role="user", content=user_interaction)

        response = self.client.chat.completions.create(
            messages=self.history,
            model="llama-3.3-70b-versatile"
        ).choices[0].message.content
        
        self.update_history(role="assistant", content=response)

        return response



if __name__ == "__main__":
    conversation_agent = ConversationAgent()
    conversation_agent.ask_llm(user_interaction="Quel âge as-tu ?")
    print(conversation_agent.history)
    print('-----')
    conversation_agent.ask_llm(user_interaction="Quelle était ma première question ?")
    print(conversation_agent.history)