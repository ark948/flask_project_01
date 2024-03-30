from app import create_app, db
import sqlalchemy as sa
import sqlalchemy.orm as so
from app.models.user import User
import os

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'sa': sa,
        'so': so,
        'db': db,
        'User': User,
    }

if __name__ == "__main__":
    app.run(debug=False)
