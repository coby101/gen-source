from app import create_app, db
from flask_migrate import Migrate
import os

app = create_app()

# Initialize database migrations
migrate = Migrate(app, db)

if __name__ == '__main__':
    debug = os.getenv("FLASK_ENV", "production") == "development"
    app.run(debug=debug, host='0.0.0.0', port=5000)
