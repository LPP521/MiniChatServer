# MiniChatServer
MiniChat 服务端

## 安装运行(Linux)
1. 克隆仓库到本地
```
git clone https://github.com/SYSUMiniChat/MiniChatServer.git
```

2. 安装`virtualenv`并激活
```
pip install virtualenv
virtualenv venv
source venv/bin/activate
```

3. 安装`Flask`和腾讯信鸽（`xinge_push`）等相关依赖
```
pip install -r requirements
```

4. 运行
```
python server.py 
```

> 运行前需要在 MiniChatServer 目录下创建一个 `server.conf` 配置文件

```
[xinge]
accessId = 腾讯信鸽 access id
secretKey = 腾讯信鸽 secret key

[email]
username = 邮箱账户
password = 邮箱密码

[mysql]
databaseUrl = 数据库 url

[minichat]
admin = 管理员账号
```