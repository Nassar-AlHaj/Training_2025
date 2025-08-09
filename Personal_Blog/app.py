import os
import json
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "replace_with_a_secret"
ARTICLES_DIR = "articles"

if not os.path.exists(ARTICLES_DIR):
    os.makedirs(ARTICLES_DIR)

def load_articles():
    items = []
    for name in os.listdir(ARTICLES_DIR):
        if name.endswith(".json"):
            path = os.path.join(ARTICLES_DIR, name)
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                data["id"] = name.replace(".json", "")
                items.append(data)
    items.sort(key=lambda x: x.get("date",""), reverse=True)
    return items

def save_article_by_id(article_id, title, content, date):
    filename = f"{article_id}.json"
    path = os.path.join(ARTICLES_DIR, filename)
    data = {"title": title, "content": content, "date": date}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def create_article(title, content, date):
    existing = [int(x.replace(".json","")) for x in os.listdir(ARTICLES_DIR) if x.endswith(".json")]
    next_id = max(existing)+1 if existing else 1
    save_article_by_id(next_id, title, content, date)
    return str(next_id)

def delete_article_by_id(article_id):
    path = os.path.join(ARTICLES_DIR, f"{article_id}.json")
    if os.path.exists(path):
        os.remove(path)

@app.route("/")
def home():
    articles = load_articles()
    return render_template("home.html", articles=articles)

@app.route("/article/<id>")
def article_page(id):
    path = os.path.join(ARTICLES_DIR, f"{id}.json")
    if not os.path.exists(path):
        return "Article not found", 404
    with open(path, "r", encoding="utf-8") as f:
        article = json.load(f)
    return render_template("article.html", article=article, id=id)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("username") == "admin" and request.form.get("password") == "1234":
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        return "Invalid credentials", 401
    return render_template("login.html")

@app.route("/admin")
def admin_dashboard():
    if not session.get("admin"):
        return redirect(url_for("login"))
    articles = load_articles()
    return render_template("admin.html", articles=articles)

@app.route("/admin/new", methods=["GET", "POST"])
def new_article():
    if not session.get("admin"):
        return redirect(url_for("login"))
    if request.method == "POST":
        title = request.form.get("title","")
        content = request.form.get("content","")
        date = request.form.get("date","")
        create_article(title, content, date)
        return redirect(url_for("admin_dashboard"))
    return render_template("new_article.html")

@app.route("/admin/edit/<id>", methods=["GET", "POST"])
def edit_article(id):
    if not session.get("admin"):
        return redirect(url_for("login"))
    path = os.path.join(ARTICLES_DIR, f"{id}.json")
    if not os.path.exists(path):
        return "Article not found", 404
    if request.method == "POST":
        title = request.form.get("title","")
        content = request.form.get("content","")
        date = request.form.get("date","")
        save_article_by_id(id, title, content, date)
        return redirect(url_for("admin_dashboard"))
    with open(path, "r", encoding="utf-8") as f:
        article = json.load(f)
    return render_template("edit_article.html", article=article, id=id)

@app.route("/admin/delete/<id>")
def delete_article_route(id):
    if not session.get("admin"):
        return redirect(url_for("login"))
    delete_article_by_id(id)
    return redirect(url_for("admin_dashboard"))

@app.route("/logout")
def logout():
    session.pop("admin", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
