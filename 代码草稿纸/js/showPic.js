/**
 * @author xzzzzz<195286381@qq.com>
 */

/**
 * 显示一张图片
 * @param  {object} whichPic -elementObject
 * @return {boolean} -始终返回false,阻止默认的事件行为
 */
function showPic(whichPic) {
    var source = whichPic.getAttribute('src');
    var placeholer = document.getElementById('placeholder');
    placeholder.setAttribute('src', source);
    return false;
}

function changeText(whichPic) {
    var text = whichPic.document.getAttribute('title');
    var textEle = document.getElementById('textEle');
    textEle.setAttribute('value', text);
}

// function console.log('addYourName') {

// }

function countBodyChildren() {
    var body = document.getElementsByTagName('body')[0];
    var nums = body.childNodes.length;
    console.log(nums);
    var eleNum = 0;
    body.childNodes.forEach( function(element) {
        if (element.nodeType === 1) {
            eleNum += 1;
        }
    });
    console.log('eleNum: ' + eleNum);
}

window.onload = countBodyChildren();