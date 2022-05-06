# OlivOSLive
bilibili直播监控广播插件(基于OlivOS)  
需要安装 `mySQL`及`pymysql`   
`mySQL`官网https://www.mysql.com/cn/  
pymysql请用pip命令`pip install pymysql`  
连接数据库的用户名及密码可在源码的`DBUSER`，`DBPASS`修改   
自己的`bothash`请自行在`69`行更换   
推送文案自定义在`67`行  
推送到自定义群聊内，请在`112`行`plugin_event.send()`内两个逗号间填入群号  
例如`plugin_event.send('group',252994683 , tmp_live_reply)`  
添加房间指令：`直播添加 [uid]` ps:不需要输入'[]'  
注意是主播的`uid`  
目前平台仅支持`qq`
