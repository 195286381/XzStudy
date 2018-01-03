#!/bin/bash

# Program:
# 生成负载均衡配置文件
# History:
# 2018/01/04 by 朱智伟/10191772


# 生成文件名
filename='webgisBalance.conf'

# 初始化
function init() {
    if [ -e ${filename} ]; then
        echo "删除旧的配置文件: ${filename}"
        rm -rf ${filename}
    fi
    echo "创建配置文件: ${filename}"
    touch ${filename}
    generateComment
}

# 生成文件注释
generateComment()
{
writeToFile "# 本文件由 webgisBalance.conf 自动生成, 请勿手动修改"
writeToFile "# create by zte/10191772"
}

readConfig() 
{
echo "test function"
}

# 向配置文件追加内容
writeToFile() 
{
echo "$1" >> ${filename}
}

# 写 upstream 配置
writeUpstream() 
{
writeToFile "upstream $1 {"
writeToFile "  server $2"
writeToFile "}"
}

# 写 server 配置
writeServer() 
{
    writeToFile "server webgisBalance {"
    writeToFile ""
    writeToFile "}"
}


#------------ main ------------ start
echo "开始执行脚本: $0"
init
writeUpstream "webgisBalance" "10.9.233.68:26180"
writeToFile "  upstream"
echo "生成配置文件内容: ${filename}"
# writeToFile ${info};
echo "执行脚本完毕: $0" && exit 0 #------------ main ------------ end
