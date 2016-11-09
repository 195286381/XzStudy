/*global require console */
'use strict';
var http = require('http');

http.createServer(function (request, response) {
    response.writeHead(200, {'Content-Type': 'text/plain; charset=UTF-8'});
    response.write('helloWolrd');
    response.end();
}).listen(8888);

console.log('start webServer at port 8888');