from sanic import blueprints

from api.profile.api import api as profile_api
from api.partie.api import api as partie_api

api = blueprints.Blueprint.group(profile_api, partie_api, url_prefix='/api')
