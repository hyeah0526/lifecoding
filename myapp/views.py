from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt # csrf를 면제
import random

# 1. HttpResponse 임포트 시키고
# 2. def index(request) 함수를 정의하고
#    HttpResponse를 이용해서 응답을 하기위해 HttpResponse를 리턴
# 3. 다시 urls.py로 가기

# 하나의 글을 딕셔너리에 담고, 그 딕셔너리들을 리스트에 담기
nextId = 4
topics = [
    {'id':1, 'title':'routing2', 'body':'Routing is ..'},
    {'id':2, 'title':'view2', 'body':'view2 is ..'},
    {'id':3, 'title':'model2', 'body':'model2 is ..'}
]

def HTMLTemplate(articleTag, id=None):
    # 전역변수 설정
    global topics
    contextUI = ''

    if id != None:
        contextUI = f'''
            <li><form action="/delete/" method="post">
                    <input type="hidden" name="id" value={id}>
                    <input type="submit" value="delete">
                </form>
            </li>
            <li><a href="/update/{id}">update</a></li>
        '''
        
    ol = ''
    for topic in topics :
        ol += f'<li><a href="/read/{topic["id"]}">{topic["title"]}</a></li>'

    return f'''
        <html>
        <body>
            <h1><a href="/">Django</a></h1>
            <ol>
                {ol}
            </ol>
            {articleTag} 
            <ul>
                <li><a href="/create/">create</a></li>
                {contextUI}
            </ul>
        </body>
        </html>              
    '''

def index(request) :

    article = '''
    <h2>Welcome</h2>
    Hello, Django       
    '''
    # 클라이언트로 보내주기
    return HttpResponse(HTMLTemplate(article))

def read(request, id) :
    global topics
    article = ''
    for topic in topics :
        if topic['id'] == int(id):
            article = f'<h2>{topic["title"]}</h2>{topic["body"]}'

    return HttpResponse(HTMLTemplate(article, id))

@csrf_exempt #면제시키고 싶은 함수에다가 가져다 놓기
def create(request) :
    global nextId

    # 사용자의 방식이 get인지 post인지 디버깅
    print('request.method', request.method)

    if request.method == 'GET':
    
        article = '''
            <form action="/create/" method="post">
            <p><input type="text" name="title" placeholder="title"></p>
            <p><textarea name="body" placeholder="body"></textarea></p>
            <p><input type="submit"></p>
            </form>
        '''
        return HttpResponse(HTMLTemplate(article, id))
    
    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        newTopic = {"id":nextId, "title":title, "body":body}
        url = '/read/'+str(nextId)
        nextId = nextId+1
        topics.append(newTopic)
        return redirect(url)


@csrf_exempt
def delete(request):
    global topics

    if request.method == 'POST' :
        id = request.POST['id']
        newTopics = []
        for topic in topics :
            if topic['id'] != int(id):
                newTopics.append(topic)
        topics = newTopics

        return redirect('/')


@csrf_exempt
def update(request, id):
    global topics
    if request.method == 'GET':
        for topic in topics:
            if topic['id'] == int(id):
                selectedTopic = {
                    "title" : topic['title'],
                    "body" : topic['body']
                }
        article = f'''
            <form action="/update/{id}/" method="post">
            <p><input type="text" name="title" placeholder="title" value={selectedTopic["title"]}></p>
            <p><textarea name="body" placeholder="body">{selectedTopic["body"]}</textarea></p>
            <p><input type="submit"></p>
            </form>
        '''
        return HttpResponse(HTMLTemplate(article, id))
    
    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']

        for topic in topics :
            if topic['id'] == int(id):
                topic['title'] = title
                topic['body'] = body
        return redirect(f'/read/{id}')