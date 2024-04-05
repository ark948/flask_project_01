from source import create_app, db
from source.auth.utils import check_username_availability
import sqlalchemy as sa
import sqlalchemy.orm as so
from source.models.user import User

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'sa': sa,
        'so': so,
        'db': db,
        'User': User,
        'chu': check_username_availability,
    }

if __name__ == "__main__":
    app.run(debug=False)
