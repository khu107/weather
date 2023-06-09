from flask import Flask, render_template, request, jsonify

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import certifi


application = app = Flask(__name__)

# MongoDB 연결 설정
ca = certifi.where()
client = MongoClient('mongodb+srv://sparta:test@cluster0.j2oiwqp.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca)
db = client.dbsparta



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/mars', methods=['POST'])
def mars_post():
    in_receive = request.form['input_give']


    html = requests.get('https://search.naver.com/search.naver?sm=tab_sug.asiw&where=nexearch&query='+in_receive+'+%EB%82%A0%EC%94%A8')
    soup = BeautifulSoup(html.text, 'html.parser')

    local = soup.find('div', {'class':'title_area _area_panel'}).find('h2',{'class':'title'}).text
    temp = soup.find('div',{'class':'temperature_text'}).text.strip()[5:]
    cast = soup.find('span',{'class':'weather before_slash'}).text
    
    chekam = soup.select_one('#main_pack > section.sc_new.cs_weather_new._cs_weather > div._tab_flicking > div.content_wrap > div.open > div:nth-child(1) > div > div.weather_info > div > div._today > div.temperature_info > dl > div:nth-child(1)').text.strip()
    sp = soup.select_one('#main_pack > section.sc_new.cs_weather_new._cs_weather > div._tab_flicking > div.content_wrap > div.open > div:nth-child(1) > div > div.weather_info > div > div._today > div.temperature_info > dl > div:nth-child(2)').text.strip()
    namso = soup.select_one('#main_pack > section.sc_new.cs_weather_new._cs_weather > div._tab_flicking > div.content_wrap > div.open > div:nth-child(1) > div > div.weather_info > div > div._today > div.temperature_info > dl > div:nth-child(3)').text.strip()
    doc = {
        'local':local,
        'temp': temp,
        'cast': cast,
        'chekam': chekam,
        'sp':sp,
        'namso':namso
    }
    db.mars.insert_one(doc)
    
    return jsonify({'msg':'succsess'})


@app.route("/mars", methods=["GET"])
def mars_get():
        
    all_mars = list(db.mars.find({},{'_id':False}).sort('_id',-1).limit(1))
    return jsonify({'result': all_mars})



if __name__ == '__main__':
    # Flask 앱 실행
    app.run()
