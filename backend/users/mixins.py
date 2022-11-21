class CheckRequestMixin:
    """Миксин для проверки запроса."""

    def good_request(self, request):
        if not request or request.user.is_anonymous:
            return False


class GetIsFollowMixin:
    """
    Миксин проверяет запрос. После этого проверяет подписал ли пользователь
    на автора.
    """

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return request.user.follower.filter(following=obj).exists()
