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

3. 安装`Flask`和腾讯信鸽（`xinge_push`）模块
```
pip install -r requirements
```

4. 运行
```
python server.py 
```