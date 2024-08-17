@echo off
if "%1" == "h" goto begin
mshta vbscript:createobject("wscript.shell").run("""%~0"" h",0)(window.close)&&exit
:begin

:: 定义锁文件路径
set "lockfile=D:\Code\sdu-electric-charge-master\script.lock"

:: 检查锁文件是否存在
if exist "%lockfile%" (
    echo Script is already running.
    exit /b
)

:: 创建锁文件
echo %date% %time% > "%lockfile%"

:: 运行你的Python脚本
cd /d D:\Code\sdu-electric-charge-master
python main.py

:: 删除锁文件
del "%lockfile%"
