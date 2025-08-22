from rest_framework import permissions


class ResponsePermission(permissions.BasePermission):
    """
    - List (GET /requests/<id>/responses/): только автор запроса или админ
    - Create (POST /requests/<id>/responses/): любой аутентифицированный, кроме автора запроса

    - Retrieve (GET /requests/<id>/responses/<pk>/): автор запроса или автор отклика или админ
    - Update/Delete: автор отклика или админ
    """

    def has_permission(self, request, view):
        user = request.user

        # есть объект юзера или аутентифиц.
        if not user or not user.is_authenticated:
            return False

        request_id = view.kwargs.get("request_id")

        if request_id is not None:
            # GET (list): автор запроса или админ
            if request.method in permissions.SAFE_METHODS:
                help_request = view.get_help_request()
                return help_request.author_id == user.id or user.is_staff

            # POST (create): всем аутент., кроме автора
            help_request = view.get_help_request()
            if help_request.author_id == user.id:
                return False
            return True
        return True

    def has_object_permission(self, request, view, obj):
        user = request.user

        if request.method in permissions.SAFE_METHODS:
            # GET (object): автор запроса или автор отклика или админ
            return (
                obj.help_request.author_id == user.id
                or obj.responder_id == user.id
                or user.is_staff
            )

        # UPDATE/DELETE (object): автор отклика или админ
        return obj.responder_id == user.id or user.is_staff
