# OlivOSLive
bilibili直播监控广播插件(基于OlivOS)  
需要安装 `mySQL`及`pymysql`   
`mySQL`官网https://www.mysql.com/cn/  
pymysql请用pip命令`pip install pymysql`  
连接数据库的用户名及密码可在源码的`DBUSER`，`DBPASS`修改   
自己的`bothash`请自行在`69`行更换   
推送文案自定义在`67`行  
推送到自定义群聊内，请在`112`行`plugin_event.send()`内两个逗号间填入群号  
例如`plugin_event.send('group', 252994683, tmp_live_reply)`  
添加房间指令：`直播添加 [uid]` ps:不需要输入'[]'  
注意是主播的`uid`  
目前平台仅支持`qq`  
ps:因为担心两个线程同时读取数据所可能产生的问题，我使用了python的`threading`库中的`Lock()`来控制两个线程对于同一个数据库的访问，  
所以当你发送直播添加的指令的时候，轮询线程可能正在占用`Lock()`,所以指令执行在已经存在的数据越多的情况下执行延迟越大(因为要等另一个线程关闭数据库)  
（如果正好遇到`save`事件。。可能会添加失败）
