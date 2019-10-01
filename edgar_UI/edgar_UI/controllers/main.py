from flask import Blueprint, render_template

main_blueprint = Blueprint(
    'main',
    __name__,
    template_folder='../templates/main'
)

@main_blueprint.route("/")
def home():
    return render_template("index.html")
