function Parent() {
	
};

function Child() {
	
};

Parent.prototype = new Child();
Parent.prototype.say = function () {
	console.log('this is Parent say');
};
Child.prototype.say = function () {
	console.log('this is Child say');
};
Child.prototype.cry = function () {
	console.log('this is Child cry');
};

var person = new Parent();
person.say(); // this is Parent say
person.cry(); // this is Child cry