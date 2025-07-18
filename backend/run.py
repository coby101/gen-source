from app.models import create_app, db
from flask_migrate import Migrate
from app import migrate

app = create_app()

# Initialize database migrations
migrate.init_app(app, db)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
