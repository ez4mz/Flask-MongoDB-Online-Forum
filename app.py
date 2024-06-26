#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Get MongoDB URI from environment variables
MONGO_URI = os.getenv('MONGO_URI')

# Connect to local MongoDB
try:
    client = MongoClient(MONGO_URI)
    db = client['forumapp'] 
    posts = db.posts
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

@app.route('/')
def home():
    docs = posts.find().sort("created_at", -1)
    return render_template('index.html', docs=docs)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post = {
            "title": title,
            "content": content,
            "created_at": datetime.datetime.utcnow(),
            "comments": []
        }
        posts.insert_one(post)
        return redirect(url_for('home'))
    return render_template('create.html')

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    post = posts.find_one({"_id": ObjectId(id)})
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        posts.update_one(
            {"_id": ObjectId(id)},
            {"$set": {"title": title, "content": content, "created_at": datetime.datetime.utcnow()}}
        )
        return redirect(url_for('home'))
    return render_template('edit.html', post=post)

@app.route('/delete/<id>')
def delete(id):
    posts.delete_one({"_id": ObjectId(id)})
    return redirect(url_for('home'))

@app.route('/post/<id>', methods=['GET', 'POST'])
def post_detail(id):
    post = posts.find_one({"_id": ObjectId(id)})
    if request.method == 'POST':
        comment_content = request.form['content']
        comment = {
            "content": comment_content,
            "created_at": datetime.datetime.utcnow()
        }
        posts.update_one(
            {"_id": ObjectId(id)},
            {"$push": {"comments": comment}}
        )
        return redirect(url_for('post_detail', id=id))
    return render_template('post_detail.html', post=post)

@app.route('/delete_comment/<post_id>/<comment_index>')
def delete_comment(post_id, comment_index):
    post = posts.find_one({"_id": ObjectId(post_id)})
    if post:
        comments = post.get('comments', [])
        if len(comments) > int(comment_index):
            comments.pop(int(comment_index))
            posts.update_one(
                {"_id": ObjectId(post_id)},
                {"$set": {"comments": comments}}
            )
    return redirect(url_for('post_detail', id=post_id))

@app.errorhandler(Exception)
def handle_error(e):
    return render_template('error.html', error=e)

if __name__ == "__main__":
    app.run(debug=True)
