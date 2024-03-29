import os
from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlunparse, urlencode

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden
from authapp.models import UserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('http',
                          'api.vk.com',
                          'method/users.get',
                          None,
                          urlencode(OrderedDict(
                              fields=','.join(('bdate', 'sex', 'about',
                                               'photo_200', 'personal')),
                              access_token=response['access_token'], v=5.131)),
                          None))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return
    data = resp.json()['response'][0]
    if data['sex'] == 1:
        user.userprofile.gender = UserProfile.FAMALE
    elif data['sex'] == 2:
        user.userprofile.gender = UserProfile.MALE
    else:
        pass
    if data['about']:
        user.userprofile.about = data['about']
    bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
    age = timezone.now().date().year - bdate.year
    user.age = age
    if age < 14:
        user.delete()
        raise AuthForbidden('social_core.backends.vk.VKOAuth2')
    if data['photo_200']:
        avatar_link = data['photo_200']
        photo_response = requests.get(avatar_link)
        path_avatar = f'users_image/{user.pk}.jpg'
        if os.path.exists(f'media/{path_avatar}'):
            pass
        else:
            with open(f'media/{path_avatar}', 'wb') as photo:
                photo.write(photo_response.content)
            user.image = path_avatar
    if data['personal']:
        user.userprofile.langs = data['personal']['langs'][0] if len(
            data['personal']['langs'][0]) > 0 else 'EN'
    user.save()
