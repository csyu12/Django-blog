import uuid

USER_KEY = 'uid'
TEN_YEARS = 60 * 60 * 24 * 365 * 10


"""
目的：统计用户访问量，在此中间件解决用户唯一ID问题
弊端：换个浏览器就可以刷新cookie，此时网站访问量就不准确了
"""


class UserIDMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        uid = self.generate_uid(request)        # 取uid
        request.uid = uid                       # 封装uid到request，方便view层业务代码需要使用
        response = self.get_response(request)   # 返回response时，设置cookie，httponly指只在服务端能访问
        response.set_cookie(USER_KEY, uid, max_age=TEN_YEARS, httponly=True)
        return response

    def generate_uid(self, request):
        # 辨别用户是否已经登陆过
        try:
            uid = request.COOKIES[USER_KEY]     # 取用户原cookie
        except KeyError:
            uid = uuid.uuid4().hex  # 若没有cookie，生成唯一uid，标记用户
        return uid


