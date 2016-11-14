## JavaScript静态代码检测工具-JSHint

javaScript的检测检测工具已经有很不少,由最初的jslint,到后来的JSHint JSCS ESLint,到最新的facebook的Flow等等.这里要介绍的是JSHint静态代码检测工具.

### [JSHint官网](http://jshint.com/docs/)里面有详尽的介绍.这里大致介绍一下快速安装并集成到sublime进行静态代码检测以及对应具体配置.

### 安装

##### 安装并配置node.js
这里首先需要安装**[node.js](https://nodejs.org/en/)**

公司的内网不能直接直接使用node.js下载模块,这里下载安装完成之后需要给node.js设置代理

C:\Users\10191772(工号)\\`.npmrc`文件下面加上如下代码:

```
registry=http://registry.npmjs.org
proxy=http://proxysz.zte.com.cn:80/
```

##### 安装JSHint
JSHint是作为node.js的一个模块来进行下载的. 这里进行全局安装JSHint模块

`$ npm install jshint -g`

安装完之后可以在命令行输入`jshint xxx.js`对代码进行检测.同时JSHint支持集成到各种IDE以及文本编辑工具.其中WebStorm自带JSHint的支持.这里讲一下SubLime Text集成JSHint静态代码检测.

##### 安装Sublime Text插件 
**[Sublime Text](:http://www.sublimetext.com/)** 安装插件 (~不会自行百度)
使用Package Control安装`SublimeLinter`和`SublimeLinter-jshint`插件
