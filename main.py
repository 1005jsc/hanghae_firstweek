import hashlib

import datetime

import jwt as jwt
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

from pymongo import MongoClient

# client = MongoClient('mongodb+srv://test:sparta@cluster0.3aflzmk.mongodb.net/?retryWrites=true&w=majority')
client = MongoClient('mongodb+srv://test:sparta@cluster0.toyvm3n.mongodb.net/Cluster0?retryWrites=true&w=majority')
# db = client.dbsparta_plus_week4

db = client.dbsparta_first_week_project

SECRET_KEY = 'sparta'


# 메인페이지
@app.route('/')
def home():
    return render_template('index.html')


# 상세페이지
@app.route('/detail')
def detail():
    return render_template('detail.html')


# 글올리는 페이지
@app.route('/add')
def add():
    return render_template('contentAdd.html')


# 가입페이지
@app.route('/sign')
def sign():
    return render_template('sign.html')


# 로그인페이지
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/sign_in', methods=['POST'])
def sign_in():
    if 'username_give' == None:
        username_receive = request.form.get('username_give', None)
        return
    else:
        username_receive = request.form['username_give']

    if 'password_give' == None:
        password_receive = request.form.get('password_give', None)
        return
    else:
        password_receive = request.form['password_give']

    print(username_receive, password_receive,)

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    print(pw_hash)

    if result is not None:
        import datetime
        payload = {
            'id': username_receive,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode('utf-8')

        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디/비밀번호가 일치하지 않습니다.'})


# 회원가입 서버 저장
@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    nickname_receive = request.form['nickname_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,  # 아이디
        "password": password_hash,  # 비밀번호
        "nickname": nickname_receive
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


# 아이디 중복 검사하는 부분
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give']
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})

# 재신이 추가한 부분


# 재신이 만든 api들

# 3 응원받기 내용 받아오기 (완료)

@app.route("/users", methods=["GET"])
def comment_get():
    all_users = list(db.comments.find({}, {'_id': False}))
    print(all_users)
    return {'users': all_users}




# 4 응원받기 올리기 (완료)


@app.route("/users/comments/insert", methods=["POST"])
def comment_insert():
    date = request.form['date']
    title = request.form['title']
    content = request.form['content']
    commentid = request.form['commentid']
    userid = request.form['userid']
    nickname = request.form['nickname']
    print(id, title)
    comment = {
        'date': date,
        'title': title,
        'content': content,
        'commentid': commentid,
        'userid': userid,
        'nickname': nickname,
    }

    db.comments.insert_one(comment)
    return "success"


# 응원받기 내용 하나 받아오기
@app.route("/users/comment", methods=["POST"])
def comment_pick_one():
    yes = request.form['commentid']

    user = db.comments.find_one({'commentid': yes })


    newUser={
        'date': user['date'],
        'title': user['title'],
        'content': user['content'],
        'commentid': user['commentid'],
        'userid': user['userid'],
        'nickname': user['nickname']
    }

    print(newUser)
    return jsonify({'user': newUser})




# 5 응원받기 내용 고치기


# @app.route("/users/comments/update", methods=["POST"])
# def comment_insert():
#
#     return "success"



# 6 응원받기 내용 삭제하기

@app.route("/users/comments/delete", methods=["DELETE"])
def comment_delete():
    db.comments.delete_one({'name': 'bobby'})
    return "success"



# 7 유저 응원글 올리기

@app.route("/users/comments/cheerups/insert", methods=["POST"])
def cheerup_insert():
    # db.comments.delete_one({'name': 'bobby'})
    return "success"

# 8 유저 응원글 지우기

@app.route("/users/comments/cheerups/delete", methods=["DELETE"])
def cheerup_delete():
    db.comments.delete_one({'name': 'bobby'})
    return "success"


# 9 유저 응원글 받기

@app.route("/users/comments/cheerups", methods=["GET"])
def cheerup_one_get():
    all_cheerups = list(db.comments.cheerups.find({}, {'_id': False}))
    print(all_cheerups)
    return {'users': all_cheerups}






# 6 응원받기 삭제하기












if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
