from app.app import app
from app.db import db

if __name__ == "__main__":
    db.init_app(app)
    app.run(debug=True)