""" Flask Application """
import os

from flask import Flask, render_template

from tomboonedotcom.extensions import db
import tomboonedotcom.config as config

app: Flask = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI  # database connection
app.config['SECRET_KEY'] = config.SECRET_KEY  # Flask secret key
app.config['SITE_NAME'] = config.SITE_NAME  # site name

# Configure images folder based on environment
if os.path.exists('/mnt/tbcdata/images'):
    # Production: use mounted Azure storage
    app.config['IMAGES_FOLDER'] = '/mnt/tbcdata/images'
else:
    # Development: use local static folder
    app.config['IMAGES_FOLDER'] = os.path.join(app.static_folder, 'images')

db.init_app(app)  # initialize app database

with app.app_context():  # Import SQLAlchemy models
    from tomboonedotcom.Models import Profile
    # noinspection PyUnusedImports
    from tomboonedotcom.Models import Project
    # noinspection PyUnusedImports
    from tomboonedotcom.Models import Employer
    # noinspection PyUnusedImports
    from tomboonedotcom.Models import Consulting
    # noinspection PyUnusedImports
    from tomboonedotcom.Models import Education

    db.create_all()  # Create tables

    profile: Profile = db.session.execute(db.select(Profile)).fetchone()  # fetch profile

    if profile is None:  # if no profile, create one
        profile: Profile = Profile()
        db.session.add(profile)
        db.session.commit()


@app.route("/")
def index():
    """ Home Page """
    userprofile: Profile = db.session.execute(db.select(Profile)).scalar_one_or_none()  # get the profile
    return render_template(  # return the formatted profile
        template_name_or_list="index.html",  # template
        profile=userprofile,  # profile
        title=app.config['SITE_NAME']
    )


if __name__ == "__main__":
    app.run()
