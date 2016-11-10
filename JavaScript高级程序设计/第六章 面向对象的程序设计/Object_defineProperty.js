'use strict';
var c = {};

Object.defineProperty(c, 'say', {
    writable: false,
    value: 'I say Hi.'
});

// 此时代码应该会报错, 因为你设置了 writable = false 该属性为只读属性,不能修改
// TypeError: Cannot assign to read only property 'say' of #<Object>
c.say = 'I say Hi~~~';
