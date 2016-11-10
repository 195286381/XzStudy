/*global alert*/
'use strict';
function createPerson(name, age, job) {
	var p = new Object();
	
	p.name = name;
	p.age = age;
	p.job = job;
	p.sayName = function () {
		console.log(this.name);
	};
	return  p;
}

var person_1 = createPerson('zzw', 21, 'student');
var person_2 = createPerson('zzz', 23, 'teacher');

/*
 * 工厂模式解决了创建多个相似对象的问题,却没有解决对象识别的问题
*/