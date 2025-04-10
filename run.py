from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPEN_API_KEY")
)

requesst = input("give me the ques:") 

completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system","content":"You are kind helpful assintant"}, 
        
        {
            "role":"user",
            "content": f"{requesst}"
        }
    ]
)

print(completion.choices[0].message.content)