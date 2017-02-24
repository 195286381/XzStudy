// const net = require('net');
// var count = 0; //当前在线连接数
// var user = {};

// var server = net.createServer(function(conn) {
//     count++; // 当有新连接,连接数+1;
//     console.log('新连接已经建立');
//     console.log('当前连接数为:' + count);
//     conn.write('欢迎进入我的聊天室.\n\r')
//     conn.write('请输入我设置的密码:\n\r')

//     conn.on('data', function(data) {
//         var str = data.toString().replace('\n\r', '');
//         console.log('你的输入是: ' + str);
//         if (str === '199011031015') {
//             conn.write('你猜对了我的密码\n\r');
//         } else {
//             conn.write('你猜错了,请从新输入:\n\r');
//         }
//     });

//     conn.on('close', function() { // 当有用户退出时,用户在线数量减1.
//         count--;
//     });

// }).listen(3002, function() {
//     console.log('-------------------------------------');
//     console.log('|                                   |');
//     console.log('|             IRC by xzzz           |');
//     console.log('|                                   |');
//     console.log('|                                   |');
//     console.log('-------------------------------------');
//     console.log('当前监听端口是3002, 开启IRC服务端成功');
// });



var net = require('net');
var connectionCounts = 0; // 当前连接数
var user = {};
var server = net.createServer(function(conn) {
    var hasName = false;
    connectionCounts++; //连接数+1
    conn.write(`当前连接人数为: ${connectionCounts}\n\r`);
    conn.write(`请输入你的名字:\n\r`)

    conn.on('data', function(data) { // 监听客户端传过来的数据.
        
        
        var str = data.toString();
        console.log(str);
    });

    conn.on('close', function() {
        console.log('close');
    })
});

server.listen(port, function() {
    console.log(`监听端口为: ${port}`);
});


function hasExist(user, conn) { // 判断是否连接已经赋予名字.
    var flag = flase;
    var namesAry = Object.keys(user);
    namesAry.forEach(function(ele) {
        if (user[ele] === conn) {
            flag = true;
        }
    })
    return false;
}

function hasName(user, name) { // 判断是否存在相同的名字
    var flag = false;
    var namesAry = Object.keys(user);
    namesAry.forEach(function(ele) {
        if (ele === name) {
            flag = true;
        }
    })
    return false;
