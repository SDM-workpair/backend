# from fastapi import HTTPException, Response, Request
# import copy
# from datetime import datetime, timedelta
# import uuid
# from starlette import status
# from exception.apiexception import ApiResponse, ApiException

# class RoleRequired:
#     def __init__(
#         self,
#         guest,
#         roles,
#         redirect_url: str = None,
#         expire_minutes: int = 30,
#         clear_interval: int = 60,
#     ):
#         self.sessions = {}
#         self.roles = roles
#         self.guest = guest
#         self.redirect_url = redirect_url
#         self.expire_minutes = expire_minutes
#         self.userclass = type(self.guest)
#         self.last_clear_time = datetime.utcnow()
#         self.interval = timedelta(minutes=clear_interval)


#     def __clear_overstayed(self):
#         now = datetime.utcnow()
#         if (now - self.last_clear_time) < self.interval:
#             return
#         self.last_clear_time = now
#         self.sessions = { k: v for k, v in self.sessions.items() if v['exp'] < now }


#     def __create_token(self, response: Response, user=None):
#         # print(self.sessions)
#         self.__clear_overstayed()
#         authorization = str(uuid.uuid1())
#         response.set_cookie(key="authorization", value=authorization)
#         if not user:
#             user = copy.deepcopy(self.guest)
#         self.sessions[authorization] = {
#             "user": user,
#             "exp": datetime.utcnow() + timedelta(minutes=self.expire_minutes)
#         }
#         return self.sessions[authorization]

#     def __update_exp(self, authorization):
#         exp = datetime.utcnow() + timedelta(minutes=self.expire_minutes)
#         self.sessions[authorization]["exp"] = exp
#         return self.sessions[authorization]

#     def __verify_roles(self, user, roleids):
#         if isinstance(roleids, list):
#             return user.roleid in roleids
#         return user.roleid == roleids


#     def login(self, response: Response, user):
#         # assert type(user) == type(self.guest)
#         current_session = self.__create_token(response, user)
#         return current_session['user']

#     def logout(self, request: Request):
#         authorization = request.cookies.get("authorization", None)
#         try:
#             current_session = self.sessions.pop(authorization)
#             return current_session['user']
#         except :
#             raise ApiException(code=1005, message="当前未登录，登出发生错误")

#     def __call__(self, *roles, **kwargs):
#         login_only = kwargs.get("login_only", False)
#         roles = [ self.roles[x] for x in roles ]
#         if login_only:
#             roles = list(self.roles.values())
#         async def func(request: Request, response: Response) -> self.userclass:
#             authorization = request.cookies.get("authorization", None)
#             if not authorization or authorization not in self.sessions:
#                 current_session = self.__create_token(response)
#             else:
#                 ntime = datetime.utcnow()
#                 session = self.sessions.get(authorization, None)
#                 if session['exp'] < ntime:
#                     self.sessions.pop(authorization)
#                     current_session = self.__create_token(response)
#                 else:
#                     current_session = self.__update_exp(authorization)
#             current_user = current_session['user']
#             if not roles or self.__verify_roles(current_user, roles):
#                 return current_session['user']
#             else:
#                 raise ApiException(
#                     code=1004, message="权限不足"
#                 )
#         return func
