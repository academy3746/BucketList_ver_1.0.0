from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

from pymongo import MongoClient

client = MongoClient('mongodb+srv://admin:1q2w3e4r!@cluster0.n5ejj.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta


# Applicable Variable
# 1. 버킷 리스트: bucket
# 1-1) 리스트 넘버: num
# 1-2) 리스트 갱신: done

@app.route('/')
def home():
    return render_template('index.html')


@app.route("/bucket", methods=["POST"])
def bucket_post():
    # CREATE TABLE
    bucket_receive = request.form['bucket_give']

    # num++
    bucket_list = list(db.buckets.find({}, {'_id': False}))
    count = len(bucket_list) + 1

    # INSERT INTO BUCKETS ('','','') VALUES (?,?,?)
    doc = {
        'bucket': bucket_receive,
        'num': count,
        'done': 0
    }
    db.buckets.insert_one(doc)

    return jsonify({'msg': '버킷리스트가 등록되었습니다. 화이팅!'})


@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    # UPDATE TABLE
    num_receive = request.form['num_give']
    db.buckets.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
    # int(num_receive): Type Conversion
    # ex) Integer.ParseInt(); in Java

    return jsonify({'msg': '목표를 달성하셨네요! 축하드려요~'})


@app.route("/bucket", methods=["GET"])
def bucket_get():
    # SELECT * FROM BUCKETS
    buckets_list = list(db.buckets.find({}, {'_id': False}))

    return jsonify({'buckets': buckets_list})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
