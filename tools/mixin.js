/**
 * create by Xzzzzz in 15/8/2017
 */

/**
 * mixin
 * @param  {[type]} source  [description]
 * @param  {[type]} dest    [description]
 * @param  {[type]} options [description]
 * @return {[type]}         [description]
 */
function mixin(source, dest, options) {
  options = options || {};
  var isOverride = (options.override === false || options.override === true) ? options.override : true,
      prop;
  for (prop in dest) {
    if (dest.hasOwnProperty(prop)) {
      if (source[prop] === undefined || (source[prop] !== undefined && isOverride)) {
        source[prop] = dest[prop]
      }
    }
  }
}
