# 成功
SUCCESS = {'code': 200}

# 用户注册模块
USER_REGISTER_NAME_EXIST = {'code': 1000, 'msg': '用户名已存在'}
USER_REGISTER_INFO_INCOMPLETE = {'code': 1001, 'msg': '注册信息不完整'}
USER_REGISTER_PASSWORD_AUTHENTICATION_FAILED = {'code': 1002, 'msg': '两次输入的密码不同，请重新输入'}
USER_REGISTER_EMAIL_FORMAT_ERROR = {'code': 1003, 'msg': '请输入正确的邮箱'}
USER_REGISTER_TEL_FORMAT_ERROR = {'code': 1004, 'msg': '请输入正确的手机号码'}
USER_REGISTER_NAME_LENGTH_ERROR = {'code': 1005, 'msg': '用户名为5-20个字符'}

# 用户登录模块
USER_LOGIN_INFO_INCOMPLETE = {'code': 1100, 'msg': '请填写完整的登陆信息'}
USER_LOGIN_USERNAME_NOT_EXIST = {'code': 1101, 'msg': '用户名不存在'}
USER_LOGIN_PASSWORD_AUTHENTICATION_FAILED = {'code': 1102, 'msg': '密码输入错误'}