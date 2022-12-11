from components.Users import Users
from sanic.response import json
from sanic import blueprints
from sanic import exceptions

api = blueprints.Blueprint('profiles__api', url_prefix='/profile')

@api.route('/ping')
async def ping(request):
    return json({'ping': 'pong'})

@api.route('/create', methods=['POST'])
async def create_profile(request):
    """
    Create a new profile

    :return: json
    :rtype: json

    :Example:

    data = {
        'token': 'token',
        'name': 'name'
    }
    """
    data = request.json
    profile = Users.create(
        token=data['token'],
        name=data['name'],
    )
    return json(profile.to_dict())

@api.route('/get/<id:int>')
async def get_profile(request, id: int):
    """
    Get a profile

    :param id: profile id
    :type id: int
    :return: json
    :rtype: json
    """
    profile = Users.get(id)
    if profile:
        return json(profile.to_dict())
    else:
        raise exceptions.NotFound('Profile not found')