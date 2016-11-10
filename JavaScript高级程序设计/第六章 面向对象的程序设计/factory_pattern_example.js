function createPerson(name, age, job) {
	var p = new Object();
	
	o.name = name;
	o.age = age;
	o.job = job;
	o.sayName = function () {
		alert(this.name);
	}
	return  p;
}

var person_1 = createPerson('zzw', 21, 'student');
var person_2 = createPerson('zzz', 23, 'teacher');