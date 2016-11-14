// 柯里化（Currying）是把接受多个参数的函数变换成接受一个单一参数(最初函数的第一个参数)的函数，
// 并且返回接受余下的参数且返回结果的新函数的技术

// 实现柯里化的Func
function  currying(func) {
	var args = Array.prototype.slice.call(arguments,1);
	
	return function () {
		var newArgs = args.concat(Array.prototype.slice.call(arguments));
		
		return func.apply(null, newArgs);
	}
}

function add() {
	var total = 0;

	for (var i = 0; i < arguments.length; i++) {
		total = total + arguments[i];
	}

	return total;
}

var addWithCurry = curryingFun(add, 1, 2, 4);

console.log(addWithCurry(123)); // => 130
