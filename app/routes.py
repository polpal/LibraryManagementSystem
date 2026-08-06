from flask import Blueprint, render_template

main = Blueprint("main", __name__)


@main.route("/")
def home():
    return render_template("index.html")


@main.route("/books")
def books():
    return render_template("books.html")


@main.route("/members")
def members():
    return render_template("members.html")


@main.route("/about")
def about():
    return render_template("about.html")