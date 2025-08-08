from flask import Blueprint

# Main API blueprint, all routes are prefixed with /api
api = Blueprint("api", __name__, url_prefix="/api")

# Import route modules to register them
from . import users
from . import sources
from . import individuals
from . import relationships
from . import research
