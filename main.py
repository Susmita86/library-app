import json
from typing import Dict

import pymongo
from flask import Flask, render_template, request, redirect, url_for
import certifi
import boto3
from botocore.exceptions import ClientError

def get_secret(secret_name: str, region_name: str) -> Dict[str,str]:
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as error:
        raise error
    secretString = get_secret_value_response['SecretString']
    secret_dict = json.loads(secretString)
    return secret_dict

app = Flask(__name__)

secret_name = "mongo_credentials"
region_name = "eu-west-1"
secret_dict = get_secret(secret_name, region_name)

username = secret_dict["username"]
password = secret_dict["password"]

# username = "admin-susmita"
# password = "susmi_mongouser123"

connection_string = f"mongodb+srv://{username}:{password}@cluster0.xl5s7ty.mongodb.net/library"
client = pymongo.MongoClient(connection_string, tlsCAFile=certifi.where())

db = client["library"]
collection = db["books"]

all_books = []

@app.route('/')
def home():
    print(client.list_database_names())
    return render_template("index.html", books=collection.find())
    # return render_template("index.html", books=all_books)

@app.route("/add", methods=["POST","GET"])
def add():
    if request.method == "POST":
        new_book = {
            "title":request.form["title"],
            "author":request.form["author"],
            "rating":request.form["rating"]
        }
        # all_books.append(new_book)
        collection.insert_one(new_book)

        return redirect(url_for('home'))
    return render_template("add.html")

if __name__ == "__main__":
    # app.run(debug=True)
    app.run(debug=True,host='0.0.0.0', port=80)
    print("Added CI CD to the project")











    # client = MongoClient(mongo_uri,
#                      port=27017,
#                      username="mongoadmin",
#                      password="password")
#
# db = client["library"]
# collection = db["books"]



