/**
 * @fileoverview 描述页面信息
 * @author xzzzzz<195286381@qq.com>
 * @version v.0.0.1
 */


/**
 * @fileoverview
 * @param fun
 * @returns {Function}
 */

function addYourName() {
	var args = Array.prototype.slice.call(arguments, 1);
	var black = console.log('this is a error');
}

function currying (fun) {
	var args = Array.prototype.slice.call(arguments,1);

	return function () {
		var newArgs = args.concat(Array.prototype.slice.call(arguments));

		return fun.apply(null, newArgs);
	};
}
/**
 * @function 返回匿名函数求和
 * @returns {Function}
 */
function addYourName() {
	var args = Array.prototype.slice.call(arguments, 1);
	return function () {
		return args;
    };
}

/**
 * @func
 * @description 一个带参数的函数
 * @param {string} a
 * @param {string} black
 * @param {string} conso
 * @returns {string}
 */
function add(a, black, conso) {
	return 'hello';
}

