""" Flask Application """
from flask import Flask, render_template
from src.tomboonedotcom.extensions import db
import src.tomboonedotcom.config as config

app: Flask = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['SITE_NAME'] = config.SITE_NAME
db.init_app(app)

with app.app_context():
    from src.tomboonedotcom.Models.Profile import Profile
    from src.tomboonedotcom.Models.Project import Project
    from src.tomboonedotcom.Models.Employer import Employer
    from src.tomboonedotcom.Models.Consulting import Consulting
    from src.tomboonedotcom.Models.Education import Education
    db.create_all()

    profile = db.session.execute(db.select(Profile)).fetchone()
    if profile is None:
        profile = Profile()
        db.session.add(profile)
        db.session.commit()


@app.route("/")
def index():
    """ Home Page """
    userprofile = db.session.execute(db.select(Profile)).scalar_one_or_none()
    return render_template("index.html", profile=userprofile, title="Home")


if __name__ == "__main__":
    app.run()
