'use strict'; // 设置全局严格模式
var c = {};

// object.defineProperty(obj, prop, descriptor); 为一个对象定义一个新的属性
// object.defineProperty(obj, descriptors); 为一个对象定义多个属性
Object.defineProperty(c, 'say', {
    writable: false,
    value: 'I say Hi.'
});

// 此时代码应该会报错, 因为你设置了 writable = false, 该属性为只读属性,不能修改
// TypeError: Cannot assign to read only property 'say' of #<Object>
c.say = 'I say Hi~~~';

// 在非严格模式下, 因为你设置了 writable = false, 该属性为只读属性 修改无效 输出依旧为之前的赋值
console.log(c.say);


