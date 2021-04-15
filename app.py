from flask import Flask , render_template, request,redirect,url_for
import json
app = Flask(__name__)
import requests
from bs4 import BeautifulSoup
 
def get_suggestions(query):
    try:
        r = requests.get(f"https://www.google.com/search?q={query}",headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'})
        soup = BeautifulSoup(r.text,'html.parser')
        return soup.find("div",id="taw").find("b").text
    except:
        return False
@app.route("/")
def home(): 
    return render_template("index.html")

@app.route("/search")
def search():
    filtered_data = []
    query=str(request.args.get("q")).lower()
    if query.strip() != "" :
        with open('youtubeData.json','r') as f:
            data = json.load(f)
        for content in data["data"]:
            if query in content["title"].lower() or query in content["channelTitle"].lower():
                filtered_data.append(content)
 
        return render_template("results.html",data=filtered_data,query=query,suggestion=get_suggestions)
    else:
        return redirect(url_for("home"))
        
@app.route("/transcription/<string:video_id>")
def transcription(video_id):
     
    with open('youtubeData.json','r') as f:
            data = json.load(f)

    for content in data["data"]:
         
        if content["id"] == video_id:
            return render_template("transcription.html",content=content)
    
    return "404 not found :("

    


 