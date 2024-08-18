# 查询青岛校区宿舍电费
程序后台运行，每半小时自动查询一次
### 替换inquiry_settings.json的信息

"account"：校园卡上的账号(6位左右)<br/>

"building"：用以下值替换<br/>
{"buildingid": "1503975832", "building": "凤凰居 S1"}<br/>
{"buildingid": "1503975890", "building": "凤凰居 S2"}<br/>
{"buildingid": "1503975967", "building": "凤凰居 S5"}<br/>
{"buildingid": "1503975980", "building": "凤凰居 S6"}<br/>
{"buildingid": "1503975988", "building": "凤凰居 S7"}<br/>
{"buildingid": "1503975995", "building": "凤凰居 S8"}<br/>
{"buildingid": "1503976004", "building": "凤凰居 S9"}<br/>
{"buildingid": "1503976037", "building": "凤凰居 S10"}<br/>
{"buildingid": "1599193777", "building": "凤凰居 S11"}<br/>
{"buildingid": "1574231830", "building": "专家公寓 T1"}<br/>
{"buildingid": "1574231835", "building": "专家公寓 T3"}<br/>
<br/>

"sender"(发送方)默认使用QQ邮箱smtp服务，参考https://cloud.tencent.com/developer/article/2177098<br/>
"password"值为是smtp服务授权码<br/>
"receiver"为任意可接受信息的邮箱<br/>
### 开机自启教程
可以参考https://blog.csdn.net/qq_41007870/article/details/121036645<br/>
##### 自行部署环境并运行代码者
将start.bat放入自启动即可静默后台运行
##### 使用release的.exe直接运行程序者
将打包好的程序(.exe)创建快捷方式并放入startup

