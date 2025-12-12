from flask import Flask, request, render_template, redirect, url_for
from datetime import datetime
import json
import os

app = Flask(__name__)

DATA_FILE = "posts.json"

# ------------------------------------------------------------
def load_posts():

    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except:
            return []
        
def save_posts(posts): #JSON 파일 저장하기
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(posts, f, ensure_ascii=False, indent=4)

posts = load_posts()
# ------------------------------------------------------------

# ------------------------------------------------------------
@app.route("/") #홈페이지
def home():
    return render_template("index.html", page="homepage")
# ------------------------------------------------------------

# ------------------------------------------------------------
@app.route("/post", methods=["GET", "POST"]) # 글 쓰기
def post():
    if request.method == "POST":
        posts = load_posts()

        title = request.form["title"] #제목값 가져오기
        content = request.form["content"] #내용값 가져오기
        mood = request.form["mood"] #감정값 가져오기

        #입력받은 글 저장하기
        posts.append({
            'id':len(posts)+1, #글의 id 저장(1부터 시작)
            'title':title, #글의 제목 저장
            'content':content, #글의 내용 저장
            'mood': mood, #글의 감정 저장
            'date' : datetime.now().strftime("%Y-%m-%d %H:%M") #글의 쓰인 저장
        })

        save_posts(posts) #JSON 파일 저장하기
        return redirect(url_for("postlist")) #목록 페이지로 이동
    
    return render_template("index.html", page="post")
# ------------------------------------------------------------

# ------------------------------------------------------------
@app.route("/postlist") # 글 목록
def postlist():
    posts = load_posts() # 최신 데이터 사용
    return render_template("index.html", page="postlist", posts=posts)
# ------------------------------------------------------------

# ------------------------------------------------------------
@app.route("/post/<int:post_id>") # 글 자세히 보기
def detailpost(post_id):
    posts = load_posts() # 최신 데이터 사용
    for p in posts:
        if p['id'] == post_id:
            return render_template("index.html", page="detail", post=p)
    return "글을 찾을 수 없습니다"
# ------------------------------------------------------------

# ------------------------------------------------------------
@app.route("/delete/<int:post_id>", methods=["POST"]) # 글 삭제
def delete_post(post_id):
    posts = load_posts() # 최신 데이터 사용
    posts = [p for p in posts if p['id'] != post_id] # 해당 ID 글 제외하기
    save_posts(posts) #JSON 파일 저장하기
    return redirect(url_for("postlist"))
# ------------------------------------------------------------

# ------------------------------------------------------------
@app.route("/edit/<int:post_id>", methods=["GET", "POST"]) # 글 수정
def editpost(post_id):
    posts = load_posts() # 최신 데이터 사용

    for p in posts:
        if p['id'] == post_id:
            if request.method == "POST":
                p['title'] = request.form['title']
                p['content'] = request.form['content']
                p['mood'] = request.form['mood']
                save_posts(posts) #JSON 파일 저장하기
                return redirect(url_for("postlist"))
            return render_template("index.html", page="edit", post=p)
        
        return "글을 찾을 수 없습니다"
# ------------------------------------------------------------

# ------------------------------------------------------------
@app.route("/search")
def search_by_date():
    posts = load_posts()
    target_date = request.args.get("date")

    if not target_date:
        return redirect(url_for("postlist"))

    filtered = [p for p in posts if p['date'].startswith(target_date)]
    return render_template("index.html", page="postlist", posts=filtered)
# ------------------------------------------------------------
    
if __name__ == "__main__":
    app.run(debug=True)
