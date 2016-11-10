'use strict';
function Person (name, age, job) {
	this.name = name;
	this.age = age;
	this.job = job;
	this.sayName = function () {
		alert(this.name);
	};
}

var person_1 = new Person('zzw', 21, 'student');
var person_2 = new Person('zzz', 23, 'teacher');

/*
 * 相比工厂模式而言,造函数模式能胜过工厂模式的地方在于可以将它的实例标识为一种特定的类型
*/