## JavaScript静态代码检测工具-JSHint的使用

javaScript的静态检测工具已经有很不少,由最初的JSLint，到后来的JSHint JSCS ESLint,到最新的facebook的Flow等等.这里要介绍的是JSHint静态代码检测工具.

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

### 配置
##### 在Sublime Text 3配置JSHint配置
在Sublime Text 的 preferences-> package settings -> sublimeLinter -> settings-User里面填入如下配置:
```
{
    "user": {
        "debug": false,
        "delay": 0.25,
        "error_color": "D02000",
        "gutter_theme": "Packages/SublimeLinter/gutter-themes/Circle/Circle.gutter-theme",
        "gutter_theme_excludes": [],
        "lint_mode": "background",
        "linters": {
            "jshint": {
                "@disable": false,
                "args": [
                    "--config",
                    "C:\\Users\\10191772\\.jshintrc"
                ],
                "excludes": []
            }
        },
        "mark_style": "outline",
        "no_column_highlights_line": false,
        "passive_warnings": false,
        "paths": {
            "linux": [],
            "osx": [],
            "windows": []
        },
        "python_paths": {
            "linux": [],
            "osx": [],
            "windows": []
        },
        "rc_search_limit": 3,
        "shell_timeout": 10,
        "show_errors_on_save": false,
        "show_marks_in_minimap": true,
        "syntax_map": {
            "html (django)": "html",
            "html (rails)": "html",
            "html 5": "html",
            "javascript (babel)": "javascript",
            "magicpython": "python",
            "php": "html",
            "python django": "python",
            "pythonimproved": "python"
        },
        "warning_color": "DDB700",
        "wrap_find": true
    }
}
```

JSHint通过`.jshintrc`文件配置验证规则，该文件应放置在验证目标文件的某个祖先目录中。SublimeLinter同时支持指定`.jshintrc`位置，覆盖“沿着父文件夹查找”的规则。通过在SublimeLinter的配置文件中合并如下内容达到这个目的。
```
  "jshint": {
                "@disable": false,
                "args": [
                    "--config",
                    "C:\\Users\\10191772\\.jshintrc"
                ],
                "excludes": []
            }
```

在`"user->linters->jshint->args"`数组的第二个填入存放.jshintrc配置文件的文件路径，这样JSHint会读取该路径下的配置进行静态检测。

![](https://github.com/195286381/file/blob/master/images/20161114/jshint_error.jpg?raw=true)
