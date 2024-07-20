import os
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify, request
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm = ChatOpenAI(api_key=os.getenv("OPEN_AI_KEY"))

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a world class blog and content writer."),
    ("user", "{input}")
])

output_parser = StrOutputParser()

chain = prompt | llm | output_parser



app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=['GET','POST'])
def generate():
    if request.method == 'POST':
        output = chain.invoke({"input": request.json.get('prompt')})
        print(output)   
    return jsonify(output)

if __name__ == "__main__":
    app.run(debug=True,port=8000)