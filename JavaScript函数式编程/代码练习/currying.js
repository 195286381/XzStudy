function currying (fun) {
	var args = Array.prototype.slice.call(arguments,1);

	return function () {
		var newArgs = args.concat(Array.prototype.slice.call(arguments));

		return fun.apply(null, newArgs);
	}
}
