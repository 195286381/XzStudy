/**
  * create by Xzzzzz in 16/08/2017
  */
// var PolylineShape = require('zrender/shape/Polyline');
// var CircleShape = require('zrender/shape/Circle');
// 画线canvas
var DrawCanvasTrack = DrawCanvasTrack || {}

DrawCanvasTrack = {
  _options: null,
  // 默认的信息窗
  _infoWindow: null,
  // 默认样式
  _defaultOptions: {
    style: {
      line: {
        strokeWidth: 5,
        strokeColor: 'yellow',
      },
      point: {
        strokeColor: 'red',
        pointRadius: 10,
      }
    },
    infowWindow: {
      formatter: function(e) {
        return '';
      }
    },
  },
  // 设置初始化标识位, 确保 init 函数只能执行一次
  _isInit: false,
  // 初始化
  init: function(dom, options) {
    // 设置初始化 flag 为 true
    this._isInit = true;

    this._options = $.extend({}, this._defaultOptions, options)
      // zrender初始化
    require(
      ['zrender', 'zrender/tool/color', 'zrender/shape/Circle', 'zrender/shape/Polyline'],
      function(zrender, color, CircleShape, PolylineShape) {}.bind(this)
    );

    this.zrender.init(dom)
      // 绑定map事件
      // 添加监听缩放的回调, 确保每一次地图的放大缩小, Canvas重绘.
    Map.events.unregister('zoomend', 'Map', DrawCanvasTrack.drawUserTrack);
    Map.events.register('zoomend', 'Map', DrawCanvasTrack.drawUserTrack);
    Map.events.unregister('zoomend', 'Map', DrawCanvasTrack.clear);
    Map.events.register('zoomend', 'Map', DrawCanvasTrack.clear);
  },
  // 画用户轨迹
  drawUserTrack: function() {
    // 若没有执行初始化操作,先执行初始化.
    if (!_isInit) {
      return;
    }
    var options = this._options;

    // 得到所有的点信息
    var pointInfos = options.pointInfos || [];
    if (points.length === 0) {
      return;
    }
    /* 绘制 */
    // 绘制连线
    var points = pointsInfo.map(function(pointInfo) {
      return point.lonlat;
    })

    this._drawLine(points);
    // 绘制点
    pointsInfo.forEach(function(pointInfo) {
      this._drawPoint(pointInfo)
    })
    this._render();
  },

  // 画线
  _drawLine: function(points) {
    var color = this._options.style.line.strokeColor;
    var width = this._options.style.line.strokeWidth;
    var scrrenPoints = points.map(function(point) {
      // 需要转换方法.
      return this._translateScreenPoint(point);
    })
    this.zr.addShape(new PolylineShape({
      style: {
        pointList: points,
        strokeColor: color,
        lineWidth: width,
      },
      hoverable: false, // default true
      draggable: false, // default false
      clickable: false, // default false
    }));
  },
  
  //
  _translateScreenPoint: function(lonlat) {
    return lonlat
  },

  // 画点
  _drawPoint: function(pointInfo) {
    var self = this;
    var radius = this._options.style.point.pointRadius;
    var color = this._options.style.point.strokeColor;
    var lonlat = pointInfo.lonlat;
    // 需要转换方法.
    var screenPoint = this._translateScreenPoint(lonlat);
    this.zr.addShape(new this.CircleShape({
      style: {
        x: screenPoint[0],
        y: screenPoint[1],
        r: radius,
        strokeColor: color, // getColor from default palette
      },
      hoverable: false, // default true
      draggable: false, // default false
      clickable: false, // default false
      // 监听鼠标在点上面的回调.
      onmouseover: function(e) {
        self._addInfoWindow(pointInfo);
      },
      onmouseout: function(e) {
        self._removeInfoWindow();
      }
    }));
  },

  // 添加信息框
  _addInfoWindow: function(pointInfo) {
    if (this._infoWindow === null) {
      return;
    }
    var $ele = $('<div id="userTrackInfoWindowContainer">' + this.options.window.formatter(pointInfo) + '</div>');
    $('body').append($ele);
    // 设置位置
    // $ele.css({
    //   top:,
    //   left:
    // })

  },

  // 移除信息框
  _removeInfoWindow: function() {
    $('#userTrackInfoWindowContainer').remove();
  },

  // 渲染
  _render: function() {
    this.zrender.render();
  },

  clear: function() {
    if (!_isInit) {
      return;
    }
    this.zrender.clear();
  }
}
