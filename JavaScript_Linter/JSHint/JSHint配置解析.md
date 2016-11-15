### JSHint配置详解
JSHint是可配置的 官网的具体配置链接 =>   **`http://jshint.com/docs/options/`**

jSHint的配置选项有三种:
* 增强参数(Enforcing Options)
* 松弛参数(Relaxing Options)
* 环境参数(Enviroments)

**如下我常用的配置选项：**


`.jshintrc文件配置`
```
{
  	// 增强参数
	"bitwise": true, // true 禁止位运算符位运算符在JS中很少使用，性能也较差，出现&也很可能是想写&&
	"camelcase": true, // true 强制使用驼峰命名(camelCase)或全大写下划线命名(UPPER_CASE)这是条最佳实践
	"curly": true, // true 控制语句使用花括号 {} 来明确代码块
	"eqeqeq": true, // true 强制用===, !==代替==, !=
	"forin": true, // true 强制在for in循环中使用Object.prototype.hasOwnProperty()来过滤原型链中的属性
	"freeze": true, // true 禁止复写原生对象(如Array, Date)的原型
	"immed": true, // true 匿名函数调用必须 (function() { ... }());
	"latedef": true, // true 变量定义前禁止使用
	"newcap": true, // true 强制构造函数首字母大写
	"noarg": true, // true 禁止使用arguments.caller和arguments.callee
	"noempty": true, // true 禁止使用空的代码块
	"nonew": true, // true 禁止把构造函数当普通函数调用
	"undef": true, // true 禁止使用不在全局变量列表中的未定义的变量
	"unused": false, // false 禁止定义变量却不使用
 	// 松弛参数
	"asi": false // fasle 允许分号补全
	"boss": false // false 允许在if，for，while语句中使用赋值
	"shadow": inner // inner ~~ check for variables defined in the same scope only
	"sub": true // true 允许使用person['name']
	"supernew": false // false 允许new function() {...}和new Object;
	// 环境参数
   	"browser": true, // 浏览器全局变量
    "devel": true, // 控制台全局变量
    "jquery": true, // Jquery全局变量
    "nonstandard": true,
    "typed": true,
    "worker": true,
    "globalstrict": true
 }
 ```
