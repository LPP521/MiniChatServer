# 服务器 API
MiniChat 服务器的接口

服务器地址：119.29.238.202:8000

返回信息均为`json`格式，例如：
```
{
    code: 0, 
    message: "登录成功"
}
```
> `code` 为0表示操作成功，非0表示操作失败，message为成功提示信息或错误原因

## 用户
1. 注册（`"/register", method="POST"`）
    * 参数
        - phone: 手机号
        - nickname： 昵称
        - password： 密码

2. 登录（`"/login", method="POST"`）
    * 参数
        - phone: 手机号
        - password： 密码

3. 登出（`"/logout", method="GET"`），只有已登录用户才能进行该操作 
    * 参数：无

4. 更改信息（`"/updateUser", method="POST"`），只有已登录用户才能进行该操作
    * 参数（不必携带全部参数，可以只是某一个或某几个）
        - nickname： 昵称
        - password： 密码
        - sex: 性别
        - city：地区
        - signature：个性签名
    
