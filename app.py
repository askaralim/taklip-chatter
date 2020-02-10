from flask import Flask, render_template, request, jsonify

from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot.comparisons import LevenshteinDistance
from chatterbot.response_selection import get_random_response

import os
import logging
import json

# Enable info level logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

default_response = ["这个问题我目前还没有正确的答案",
                    "hmmm...目前的训练数据还不够丰富，请给我多点时间再学习研究一下",
                    "sorry 这个问题我没有理解",
                    "你难倒我了"]

taklip_bot = ChatBot('Taklip Bot',
                     read_only=True,
                     storage_adapter='chatterbot.storage.SQLStorageAdapter',
                     database_uri='sqlite:///database.sqlite3',
                     # database = "taklip_bot_db",
                     # database_uri = "mysql://root:root@localhost:3306/chatbot?charset=utf8",
                     database='tchatter.sqlite3',
                     logic_adapters=[
                         {
                             'import_path': 'chatterbot.logic.BestMatch',
                             'statement_comparison_function': LevenshteinDistance,
                             # "statement_comparison_function": SentimentComparison
                             # "statement_comparison_function": SynsetDistance
                             # "statement_comparison_function": JaccardSimilarity,
                             'response_selection_method': get_random_response,
                             'default_response': default_response,
                             'maximum_similarity_threshold': 0.90
                         }
                     ],
                     preprocessors=[
                         'chatterbot.preprocessors.clean_whitespace'
                     ],
                     )

trainer = ChatterBotCorpusTrainer(taklip_bot)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')

    return str(taklip_bot.get_response(userText))


@app.route("/chat")
def get_chat_response():
    userText = request.args.get('msg')

    response = taklip_bot.get_response(userText)

    response_data = response.serialize()

    return jsonify(response_data)


@app.route("/train")
def train():
    try:
        if os.path.exists("tchatter.sqlite3"):
            os.remove("tchatter.sqlite3")
        print("Old database removed. Training new database")
    except:
        print('No database found. Creating new database.')

    # for file in os.listdir('data'):
    #     print('Training using '+file)
    #     # convData = open('data/' + file).readlines()
    #     trainer.train('data/' + file)
    #     print("Training completed for "+file)

    trainer.train('data/brands.json')
    print("Training completed for brands.json")
    trainer.train('data/contents.json')
    print("Training completed for contents.json")
    trainer.train('data/terms.json')
    print("Training completed for terms.json")

    trainer.train(
        "chatterbot.corpus.taklip"
    )

    # return str("success")
    return jsonify({'message': 'success'})


if __name__ == "__main__":
    app.run()
