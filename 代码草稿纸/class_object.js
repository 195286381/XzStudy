/**
 * create by Xzzzz in 14/08/2017
 */
;(function(name, factory, undefined) {
  var isBrowserEnv = typeof window === 'object';
  if (typeof module === 'object' && typeof module.exports === 'function') {
    module.exports = factory();
  } else if (typeof require === 'function') {
      require(factory)
  } else if (isBrowserEnv) {
      window[name] = factory();
  } else {
    throw new Error();
  }
})('__tools__', function() {
  var object = {
    Class: function() {
      var P = arguments[0];
      var c = typeof P.initilize === 'function' ? P.initilize : function() {};
      c.prototype = P;
      return c;
    }
  }
  return object;
});


/**
 * 浏览器环境DEMO
 */
// var Obj = __tools__.Class({
//   initilize: function(name, age) {
//     this.name = name;
//     this.age = age;
//   },
//   say: function() {
//     var name = this.name;
//     var age = this.age;
//     console.log(`My name is ${name}, I am ${age} years old!`)
//   }
// })
// var obj = new Obj('xzzzz', 24);
// obj.say();
