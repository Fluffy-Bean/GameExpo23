from flask import Flask, render_template
from flask_assets import Bundle
from website.extensions import db, migrate, assets
from website.config import INSTANCE_DIR, MIGRATION_DIR

app = Flask(__name__, instance_path=INSTANCE_DIR)
app.config.from_pyfile('config.py')

db.init_app(app)
migrate.init_app(app, db, directory=MIGRATION_DIR)
with app.app_context():
    db.create_all()

assets.init_app(app)
styles = Bundle('sass/styles.sass', filters='libsass, cssmin', output='gen/packed.css', depends='sass/*.sass')
assets.register('styles', styles)
scripts = Bundle('js/*.js', filters='jsmin', output='gen/packed.js')
assets.register('scripts', scripts)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')
