#!/bin/bash
# 动态生成配置文件

# 配置文件名称
configFile='webgisBalance.ini'
filename="webgisBalance.conf"

# 读取配置文件
function readINI()
{
 SECTION=$1; ITEM=$2
 readIni=`awk -F '=' '/\['$SECTION'\]/{a=1}a==1&&$1~/'$ITEM'/{print $2;exit}' $configFile`
 echo ${readIni}
}

# 获取分组
function getGroups()
{
groups=$(readINI 'global' 'groups')
groups=${groups}',global'
echo ${groups//,/ }
}
        
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
function generateComment()
{
writeToFile "# 本文件由 webgisBalance.conf 自动生成, 请勿手动修改"
writeToFile "# create by zte/10191772"
}

# 向配置文件追加内容
function writeToFile() 
{
echo -e "$1" >> ${filename}
}

# 写 upstream 配置
function writeUpstream() 
{
group=$1
ips=$(readINI "$group" 'ips')
ipsAry=(${ips//,/ })
writeToFile "upstream $1 {"
for ip in ${ipsAry[@]}
do
writeToFile "  server $ip;";
done
writeToFile "}\n"
}

function writeServer()
{
# 获得监听端口
groupAry=($(getGroups))
port=$(readINI 'global' 'listenPort')
writeToFile 'server {'
writeToFile "  port: ${port};"
for group in ${groupAry[@]}
do
    if [ $group == 'global' ];then
        locationStrStart="  location {"
        locationStrEnd='  };'
        locationStrContent="    proxy_pass http://${group};"
        writeToFile "${locationStrStart}"
        writeToFile "${locationStrContent}"
        writeToFile "${locationStrEnd}"
    else
        provinceCode=$( readINI $group 'provinceCode' )
        # echo ${provinceCodeAry[@]}
        codeReg="${provinceCode//,/|}"
        # echo $codeReg
        locationStrStart="  location ~ /((${codeReg})m_)|((${codeReg})w_)|((${codeReg})d_)|((${codeReg})h_)/ {"
        locationStrEnd='  };'
        locationStrContent="    proxy_pass http://${group};"
        writeToFile "${locationStrStart}"
        writeToFile "${locationStrContent}"
        writeToFile "${locationStrEnd}"
    fi
done
writeToFile '}'
# 设置配置文件入口
}

#------------main-----------start

init

groupAry=($(getGroups))

# 设置upstream
for group in ${groupAry[@]}
do
writeUpstream $group
done

# 设置server
writeServer

#------------main-----------end