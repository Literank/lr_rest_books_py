from functools import wraps
from flask import request, jsonify
from books.domain.gateway import PermissionManager
from books.domain.model.user import UserPermission

TOKEN_PREFIX = "Bearer "


def perm_check(perm_manager: PermissionManager, allow_perm: UserPermission):
    def middleware(view_func):
        @wraps(view_func)
        def wrapped_view(*args, **kwargs):
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                return jsonify({"error": "Token is required"}), 401

            token = auth_header.replace(TOKEN_PREFIX, "", 1)
            try:
                has_perm = perm_manager.has_permission(token, allow_perm)
            except Exception as e:
                return jsonify({"error": f"{e}"}), 401
            if not has_perm:
                return jsonify({"error": "Unauthorized"}), 401
            return view_func(*args, **kwargs)
        return wrapped_view
    return middleware
