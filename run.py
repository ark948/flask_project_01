from source import create_app, db
from source.utils import is_username_available
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
        'u_check': is_username_available,
    }

if __name__ == "__main__":
    app.run(debug=False)
