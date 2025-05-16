from typing import Dict, Any


def get_user_from_post(request) -> Dict[str, Any]:
    return {
        'username': request.POST.get('username', None),
        'password': request.POST.get('password', None),
    }


def set_active(ctx: Dict[str, Any], link: str):
    ctx['active'] = link
