# -*- coding: utf-8 -*-
import urllib.request
import json
import datetime
from bs4 import BeautifulSoup
from flask import Flask
from datetime import datetime
from slack import WebClient
from slackeventsapi import SlackEventAdapter
from slack.web.classes.blocks import *
from slack.web.classes.elements import *
SLACK_TOKEN = "xoxb-678328595426-691902285110-YJGDK7VAcCdQvytUkTuUH8rn"
SLACK_SIGNING_SECRET = "be811fd50804ee0229e873f334534991"
app = Flask(__name__)
slack_events_adaptor = SlackEventAdapter(SLACK_SIGNING_SECRET, "/listening", app)
slack_web_client = WebClient(token=SLACK_TOKEN)

# 영화배우 필모 함수
def _moviestar_filmo(text):
    name = urllib.parse.quote(text)
    ServiceKey = "9a5fa7cc90bd2b3ebb0feb3d6749ae1b"
    url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?key=9a5fa7cc90bd2b3ebb0feb3d6749ae1b&peopleNm=" + name + ""
    movieJson = urllib.request.urlopen(url)
    starData = json.loads(movieJson.read())
    string = ""
    index = 0
    string += "*#필모그라피 정보*\n"
    for i in range(len(starData["peopleListResult"]["peopleList"])):
        if starData["peopleListResult"]["peopleList"][i]["repRoleNm"] == '배우':
            if index == 1:
                string += "*동명이인이 있는데 찾으시는 분이 이분인가요?*\n "
            elif index > 2:
                string += "*혹은*\n"
            string += starData["peopleListResult"]["peopleList"][i]["filmoNames"] + "\n"
            index += 1
    string += ' `#' + text + "` `#필모그라피`" + " `#MovieBot`"
    if len(starData["peopleListResult"]["peopleList"]) == 0:
        string = ""
        string = ":no_entry_sign:* 해당 배우의 검색결과가 없어요*!\n        *다시 입력해주세요~*"
    return string

#영화감독필모 함수
def _director_filmo(text):
    name = urllib.parse.quote(text)
    ServiceKey = "9a5fa7cc90bd2b3ebb0feb3d6749ae1b"
    url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/people/searchPeopleList.json?key=9a5fa7cc90bd2b3ebb0feb3d6749ae1b&peopleNm=" + name + ""
    movieJson = urllib.request.urlopen(url)
    starData = json.loads(movieJson.read())
    string = ""
    index = 0
    string += ' *#' + text + " 필모그라피*\n"
    for i in range(len(starData["peopleListResult"]["peopleList"])):
        if starData["peopleListResult"]["peopleList"][i]["repRoleNm"] == '감독':
            if index == 1:
                string += "*동명이인이 있는데 찾으시는 분이 이분인가요?*\n "
            elif index > 2:
                string += "*혹은*\n"
            string += starData["peopleListResult"]["peopleList"][i]["filmoNames"] + "\n"
            index += 1
    string += ' `#' + text + "` `#필모그라피`" + " `#MovieBot`"
    if len(starData["peopleListResult"]["peopleList"]) == 0:
        string = ""
        string = ":no_entry_sign:* 해당 감독의 검색결과가 없어요*!\n        *다시 입력해주세요~*"
    return string


# 박스오피스 순위 함수
def _boxoffice_ranking(text):
    time = ""
    time += str(datetime.today().year)
    if datetime.today().month < 10:
        time += '0'
    time += str(datetime.today().month)
    time += str(datetime.today().day - 1)
    stime = urllib.parse.quote(time)
    ServiceKey = "9a5fa7cc90bd2b3ebb0feb3d6749ae1b"
    url = "http://www.kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key=9a5fa7cc90bd2b3ebb0feb3d6749ae1b&targetDt=" + stime + ""
    movieJson = urllib.request.urlopen(url)
    movieData = json.loads(movieJson.read())
    string = "*#박스오피스 순위*\n"
    for i in range(10):
        string += str(i + 1) + "위 "
        string += movieData["boxOfficeResult"]["dailyBoxOfficeList"][i]["movieNm"] + " /"
        string += movieData["boxOfficeResult"]["dailyBoxOfficeList"][i]["audiAcc"] + "명 \n"
    string += "`#박스오피스` `#MovieBot`"
    return string

#영화 리뷰 함수
def _movie_review(text):
    client_id = "qjUBJerjSuAHujGwA_Tn"  # 애플리케이션 등록시 발급 받은 값 입력
    client_secret = "nVJc1cIHBB"  # 애플리케이션 등록시 발급 받은 값 입력

    text = urllib.parse.quote(text)

    url = "https://openapi.naver.com/v1/search/movie?query=" + text + "&display=3&sort=count"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read().decode('utf-8')
        result = json.loads(response_body)
        item = result['items'][0]
        print(item['link'])
        url2 = item['link']
        source_code = urllib.request.urlopen(url2).read()
        soup = BeautifulSoup(source_code, 'html.parser')
        reples=[]

        for div_tag in soup.find_all('div', class_='score_result'):
            for h_tag in div_tag.find_all(class_='score_reple'):
                for p_tag in h_tag.find_all('p'):
                    reples.append(p_tag.get_text().strip())
        print(reples)
        reple_string=''
        for reple in reples:
            reple_string += str('*  ' + reple + '\n')
        print(reple_string)
        first_item_image = ImageElement(
            image_url=item["image"],
            alt_text='이미지 없음'
        )
        list2 = []
        if float(item['userRating']) > 0.0 and float(item['userRating']) <= 3.0:
            emo = ':angry:'
        elif float(item['userRating']) > 3.0 and float(item['userRating']) <= 7.0:
            emo = ':thinking_face:'
        elif float(item['userRating']) > 7.0 and float(item['userRating']) <= 9.0:
            emo = ':relaxed:'
        else:
            emo = ':heart_eyes:'
        head_section = SectionBlock(
            text=' *' + item['title'].replace('<b>', '').replace('</b>', '') + '    :   ' + item['userRating']
                 + ' *' + '   ' + emo + '\n\n' + reple_string + '\n' + "`#리뷰` `#MovieBot`",
            accessory=first_item_image
        )
        list2.append(head_section)
    else:
        print("Error Code:" + rescode)
    return list2


#평점, 줄거리 함수
def _movie_grade(text):
    client_id = "qjUBJerjSuAHujGwA_Tn"  # 애플리케이션 등록시 발급 받은 값 입력
    client_secret = "nVJc1cIHBB"  # 애플리케이션 등록시 발급 받은 값 입력

    text = urllib.parse.quote(text)

    url = "https://openapi.naver.com/v1/search/movie?query=" + text + "&display=3&sort=count"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if rescode == 200:
        response_body = response.read().decode('utf-8')
        result = json.loads(response_body)
        item = result['items'][0]
        print(item['link'])
        url2 = item['link']
        source_code = urllib.request.urlopen(url2).read()
        soup = BeautifulSoup(source_code, 'html.parser')
        sumarry=[]

        for span_tag in soup.find_all('div', class_='story_area'):
            for h_tag in span_tag.find_all('h5'):
                sumarry.append(h_tag.get_text().strip())
            for p_tag in span_tag.find_all('p'):
                sumarry.append(p_tag.get_text().strip().replace('\r', '').replace('\xa0', ''))
        first_item_image = ImageElement(
            image_url=item["image"],
            alt_text='이미지 없음'
        )
        list2 = []
        if float(item['userRating']) > 0.0 and float(item['userRating']) <= 3.0:
            emo = ':angry:'
        elif float(item['userRating']) > 3.0 and float(item['userRating']) <= 7.0:
            emo = ':thinking_face:'
        elif float(item['userRating']) > 7.0 and float(item['userRating']) <= 9.0:
            emo = ':relaxed:'
        else:
            emo = ':heart_eyes:'

        if len(sumarry) > 1:
            text2 = ' *' + item['title'].replace('<b>', '').replace('</b>', '') + '    :   ' + item['userRating'] + \
                    ' *' + '   ' + emo + '\n\n' + ' _' + sumarry[0] + ' _' + '\n' + sumarry[1] + "\n`#평점` `#MovieBot`"
        else:
            text2 = ' *' + item['title'].replace('<b>', '').replace('</b>', '') + '    :   ' + item['userRating'] + \
                    ' *' + '   ' + emo + '\n\n' + ' _' + sumarry[0] + ' _' + "\n`#평점` `#MovieBot`"

        head_section = SectionBlock(
            text=text2,
            accessory=first_item_image
        )
        list2.append(head_section)
    else:
        print("Error Code:" + rescode)
    return list2


@slack_events_adaptor.on("app_mention")
def app_mentioned(event_data):
    channel = event_data["event"]["channel"]
    text = event_data["event"]["text"]
    input = []
    input = text.split()
    index = 0
    if len(input) == 2:
        if input[1] == '랭킹':
            message = _boxoffice_ranking(input[1])
            index = 1
        else:
            message = ":pushpin: *MovieBot 멘션 안내*\n박스오피스_ `@movieBot 랭킹`\n영화 리뷰_ `@movieBot 영화제목 리뷰`\n" \
                      "영화평점_ `@movieBot 영화제목 평점`\n배우 필모_ `@movieBot 배우 배우이름`\n"\
                  + "감독 필모_ `@movieBot 감독 감독이름`\n*순서로 멘션해주세요!*"
    else:
        if input[1] == '감독':
            message = _director_filmo(input[2])
            index = 1
        elif input[1] == '배우':
            message = _moviestar_filmo(input[2])
            index = 1
        elif input[2] == '평점':
            message = _movie_grade(input[1])
            index = 2
        elif input[2] == '리뷰':
            message = _movie_review(input[1])
            index = 2
        else:
            message = ":pushpin: *MovieBot 멘션 안내*\n박스오피스_ `@movieBot 랭킹`\n영화 리뷰_ `@movieBot 영화제목 리뷰`\n" \
                      "영화평점_ `@movieBot 영화제목 평점`\n배우 필모_ `@movieBot 배우 배우이름`\n"\
                  + "감독 필모_ `@movieBot 감독 감독이름`\n*순서로 멘션해주세요!*"
    if index == 2:
        slack_web_client.chat_postMessage(
            channel=channel,
            blocks=extract_json(message)
        )
    else:
        slack_web_client.chat_postMessage(
            channel=channel,
            text=message
        )
@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"
if __name__ == '__main__':
    app.run('127.0.0.1', port=8701)
