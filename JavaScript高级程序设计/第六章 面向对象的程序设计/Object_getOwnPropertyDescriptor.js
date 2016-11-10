'use strict'; // 使用严格模式
var foo = {};

// 属性描述不能作为缺省值,会报错 TypeError: Property description must be an object: undefined
// Object.defineProperty(foo, 'prop_1'); 

Object.defineProperty(foo, 'prop_2', {});
Object.defineProperty(foo, 'prop_3', {
    writable: false,
    enumerable: true,
    configurable: true,
    value: 'this is prop_3'
});
var descriptor_2 = Object.getOwnPropertyDescriptor(foo, 'prop_2');
var descriptor_3 = Object.getOwnPropertyDescriptor(foo, 'prop_3');

// 未设置属性的默认值 
console.log(descriptor_2.writable); // false
console.log(descriptor_2.enumerable); // false
console.log(descriptor_2.configurable); // false
console.log(descriptor_2.value); // undefined

console.log(descriptor_3.writable); // false
console.log(descriptor_3.enumerable); // true
console.log(descriptor_3.configurable); // true
console.log(descriptor_3.value); // 'this is prop_3'

