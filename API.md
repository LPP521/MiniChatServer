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
        - id: 邮箱
        - nickname： 昵称
        - password： 密码
        - code: 验证码

2. 登录（`"/login", method="POST"`）
    * 参数
        - id: 邮箱
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
        - avatar: 用户头像

5. 获取用户信息（`"/getUserInfo", method="GET"`）, 只有已登录用户才能进行该操作
    * 参数：无
    * 返回值
    ```
    {
        code: 0,
        message: {
            avatar: "/static/image/head.png",
            city: "未知城市",
            id: "12345678910",
            nickname: "caitzh",
            sex: "未知",
            signature: "什么都没留下"
        }
    }
    ```

6. 获取验证码（`"/getVerifycode/<id>", method=["GET"]`）
    * 参数： id（邮箱）

7. 检查验证码是否正确（`"/verifyCode", method=["POST"]`）
    * 参数： 
        - id： 邮箱
        - code： 验证码

8. 根据`id`查询用户（`"/query/<id>", method=["GET"]`）
    * 参数： id（邮箱）
    
9. 确定旧密码是否正确（`"/verifyOldPassword", method=["POST"]`）
    * 参数： password (旧密码)