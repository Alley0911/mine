#!/usr/bin/expect
set pwd "qhyu4290600"

spawn sudo service ssh --full-restart 
expect "*assword*" 
send "$pwd\r"
expect eof
# 我就是来添乱的
# 我就是再试一下
