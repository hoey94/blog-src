---
layout: post
title: wangEditor粘贴图片上传
tags: 问题总结
date: 2018-03-27 00:00:00
categories: 前端
---
wangEditor粘贴图片上传功能

### 思路
使用paste.js辅助上传,开源的github地址 https://github.com/layerssss/paste.js/

如果需要的话可以试用提供的压缩工具对base64进行压缩后上传,在这边没压缩的图片10M,压缩完200KB,还是推荐一用。

1. 初始化富文本编辑器
2. 定位编辑器的textarea div框,为其绑定paste事件
3. 解析粘贴板中的数据,数据有可能不是image,所以要做判断
4. 转成base64编码，获取一个图
5. 压缩图片，封装FormData对象
6. 使用ajax提交数据到后台处理
7. 后台返回上传后的图片路径，路径可以是绝对路径也可以是相对路径,但必须是在浏览器的url中可以访问的
8. 在ajax success回调中动态为编辑器的textarea div框append一个<img>标签

注意初始化那块的代码，我这里业务需要在一个页面初始化多个Editor,所以我写在循环里了,需要根据代码，结合自身业务做适当修改

### 代码
#### workflow-collision.js
我主要的业务在这个js里面 

```javascript
function initTextarea(nodes,createBy){
	var currentUserId = BimBdip.currentUserid;
	var divId = "";
	var textId = "";
	var E = window.wangEditor
	var menu1 = [
	];
	if(gloubleVariable.status == '0' && currentUserId == createBy || typeof(createBy) == 'undefined'){
		menu1 = [
			'head',  // 标题
		    'bold',  // 粗体
		    'italic',  // 斜体
		    'underline',  // 下划线
		    'strikeThrough',  // 删除线
		    'foreColor',  // 文字颜色
		    'backColor',  // 背景颜色
		    'list',  // 列表
		    'justify',  // 对齐方式
		    'emoticon',  // 表情
		    'image',  // 插入图片
		    'undo',  // 撤销
		];
	}
	nodes.forEach((node,index)=>{
		divId = "twoDimesional-div-"+index;
		var editor = new E('#'+divId);
		textId = "twoDimesional-text-"+index;
		var $text = $('#' + textId);
		editor.customConfig.onchange = function (html) {
		// 监控变化，同步更新到 textarea
			$text.val(html)
		}
		editor.customConfig.uploadImgServer = publicJS.tomcat_url + '/workflow/uploadTwoDimesionalImgage.action';
		editor.customConfig.uploadFileName = 'files';
		editor.customConfig.menus = menu1;
		editor.create();
		$text.val(editor.txt.html());
		if(gloubleVariable.status == '0' && workflowCollision.currentListName != 'handle' && workflowCollision.currentListName != 'cc'){
			 editor.$textElem.attr('contenteditable', true);
		}else{
			 editor.$textElem.attr('contenteditable', false);
		}
		var selector = '.w-e-text:eq('+index+')';
		var a = $(selector);
		// 为每个节点框添加粘贴事件,依赖paste.js
		copyBindEvent(a[0]);
	})
}
/**
 * 绑定粘贴事件
 * @param _target需要绑定粘贴事件的js对象 
 * @returns
 */
function copyBindEvent(_target){
	_target.addEventListener('paste', function (event) {
		workflowCollision.operateEditorTarget = _target;
		// 获取浏览器类型
        var broswerType = GetBrowserType();
        if (broswerType == "Chrome") {

            var clipboard = event.clipboardData;
            var blob = null;
            for (var i = 0; i < event.clipboardData.items.length; i++) {
                if (clipboard.items[i].type.indexOf("image") != -1) {
                    blob = clipboard.items[i].getAsFile();
                    //转成base64编码，获取一个图片
                    var reader = new window.FileReader();
                    reader.readAsDataURL(blob);
                    reader.onloadend = function () {
                        // 压缩图片
                        discussCompress(reader.result);
                    }
                }
                else if (clipboard.items[i].type.indexOf("html") != -1) {
                    var html = $(event.clipboardData.getData("text/html"));
                    html.find("img").each(function () {
                        var canvas = document.createElement("canvas");
                        var context = canvas.getContext("2d");
                        var img = document.createElement("img");
                        var src = $(this).attr("src");
                        var _this = this;
                        img.src = src;
                        var imageS = new Image();
                        context.drawImage(img, 0, 0, img.width, img.height);
                        imageS.src = canvas.toDataURL("image/png");
                        // 压缩图片
                        discussCompress(imageS.src);
                    });
                }
            }
        }
        //阻止默认粘贴事件
//        event.originalEvent.preventDefault();
    });
}

// 图片压缩
function discussCompress(base64code){
	var fd = new FormData();
	//压缩图片
	compressImg(base64code,450,250,function(base64code){
	    var blob = dataURLToBlob(base64code);
	    if (blob !== null || blob !== undefined || blob !== '') {
	        fd.append("files",blob);
	        // 上传服务器
	        copyDoAjax(fd);
	    }else{
	        Dialog.alert("上传图片失败,请重试!");
	    }
	});
}

/**
 * 上传服务器
 * @param fd
 * @returns
 */
function copyDoAjax(fd) {
	var url = publicJS.tomcat_url + '/workflow/uploadTwoDimesionalImgage.action';
	$.ajax({
   		url:url,
   		type:'POST',
   		data:fd,
   		processData:false,
   		contentType:false,
   		dataType : "json",
  		//jsonp: "jsonpCallBack",
        success: function (data, status) {//操作成功后的操作！data是后台传过来的值
        	//console.log("上传图片成功");
        	//往富文本框添加图片 <img src="http://test-file.bimbdip.com/discuss/1522142071651.tmp" style="max-width:100%;">
        	var html = `<img src="${data.data}" style="max-width:100%;">`;
        	$(workflowCollision.operateEditorTarget).append(html);
        	
        },
        error: function (xhr, textStatus, errorThrown) {
        	alert("上传图片失败");
        }
    });
}

// 获取浏览器类型
function GetBrowserType() {
    var userAgent = navigator.userAgent;
    var isOpera = userAgent.indexOf("Opera") > -1;
    if (isOpera) {
        return "Opera"
    }
    ; //判断是否Opera浏览器
    if (userAgent.indexOf("Firefox") > -1) {
        return "FF";
    } //判断是否Firefox浏览器
    if (userAgent.indexOf("Chrome") > -1) {
        return "Chrome";
    }
    if (userAgent.indexOf("Safari") > -1) {
        return "Safari";
    } //判断是否Safari浏览器

    return "IE";//其他的就当IE吧
}
```
#### 压缩的相关库
megapix-image.js 开源库

```javascript
/**
 * Mega pixel image rendering library for iOS6 Safari
 *
 * Fixes iOS6 Safari's image file rendering issue for large size image (over mega-pixel),
 * which causes unexpected subsampling when drawing it in canvas.
 * By using this library, you can safely render the image with proper stretching.
 *
 * Copyright (c) 2012 Shinichi Tomita <shinichi.tomita@gmail.com>
 * Released under the MIT license
 */
(function() {

  /**
   * Detect subsampling in loaded image.
   * In iOS, larger images than 2M pixels may be subsampled in rendering.
   */
  function detectSubsampling(img) {
    var iw = img.naturalWidth, ih = img.naturalHeight;
    if (iw * ih > 1024 * 1024) { // subsampling may happen over megapixel image
      var canvas = document.createElement('canvas');
      canvas.width = canvas.height = 1;
      var ctx = canvas.getContext('2d');
      ctx.drawImage(img, -iw + 1, 0);
      // subsampled image becomes half smaller in rendering size.
      // check alpha channel value to confirm image is covering edge pixel or not.
      // if alpha value is 0 image is not covering, hence subsampled.
      return ctx.getImageData(0, 0, 1, 1).data[3] === 0;
    } else {
      return false;
    }
  }

  /**
   * Detecting vertical squash in loaded image.
   * Fixes a bug which squash image vertically while drawing into canvas for some images.
   */
  function detectVerticalSquash(img, iw, ih) {
    var canvas = document.createElement('canvas');
    canvas.width = 1;
    canvas.height = ih;
    var ctx = canvas.getContext('2d');
    ctx.drawImage(img, 0, 0);
    var data = ctx.getImageData(0, 0, 1, ih).data;
    // search image edge pixel position in case it is squashed vertically.
    var sy = 0;
    var ey = ih;
    var py = ih;
    while (py > sy) {
      var alpha = data[(py - 1) * 4 + 3];
      if (alpha === 0) {
        ey = py;
      } else {
        sy = py;
      }
      py = (ey + sy) >> 1;
    }
    var ratio = (py / ih);
    return (ratio===0)?1:ratio;
  }

  /**
   * Rendering image element (with resizing) and get its data URL
   */
  function renderImageToDataURL(img, options, doSquash) {
    var canvas = document.createElement('canvas');
    renderImageToCanvas(img, canvas, options, doSquash);
    return canvas.toDataURL("image/jpeg", options.quality || 0.8);
  }

  /**
   * Rendering image element (with resizing) into the canvas element
   */
  function renderImageToCanvas(img, canvas, options, doSquash) {
    var iw = img.naturalWidth, ih = img.naturalHeight;
    if (!(iw+ih)) return;
    var width = options.width, height = options.height;
    var ctx = canvas.getContext('2d');
    ctx.save();
    transformCoordinate(canvas, ctx, width, height, options.orientation);
    var subsampled = detectSubsampling(img);
    if (subsampled) {
      iw /= 2;
      ih /= 2;
    }
    var d = 1024; // size of tiling canvas
    var tmpCanvas = document.createElement('canvas');
    tmpCanvas.width = tmpCanvas.height = d;
    var tmpCtx = tmpCanvas.getContext('2d');
    var vertSquashRatio = doSquash ? detectVerticalSquash(img, iw, ih) : 1;
    var dw = Math.ceil(d * width / iw);
    var dh = Math.ceil(d * height / ih / vertSquashRatio);
    var sy = 0;
    var dy = 0;
    while (sy < ih) {
      var sx = 0;
      var dx = 0;
      while (sx < iw) {
        tmpCtx.clearRect(0, 0, d, d);
        tmpCtx.drawImage(img, -sx, -sy);
        ctx.drawImage(tmpCanvas, 0, 0, d, d, dx, dy, dw, dh);
        sx += d;
        dx += dw;
      }
      sy += d;
      dy += dh;
    }
    ctx.restore();
    tmpCanvas = tmpCtx = null;
  }

  /**
   * Transform canvas coordination according to specified frame size and orientation
   * Orientation value is from EXIF tag
   */
  function transformCoordinate(canvas, ctx, width, height, orientation) {
    switch (orientation) {
      case 5:
      case 6:
      case 7:
      case 8:
        canvas.width = height;
        canvas.height = width;
        break;
      default:
        canvas.width = width;
        canvas.height = height;
    }
    switch (orientation) {
      case 2:
        // horizontal flip
        ctx.translate(width, 0);
        ctx.scale(-1, 1);
        break;
      case 3:
        // 180 rotate left
        ctx.translate(width, height);
        ctx.rotate(Math.PI);
        break;
      case 4:
        // vertical flip
        ctx.translate(0, height);
        ctx.scale(1, -1);
        break;
      case 5:
        // vertical flip + 90 rotate right
        ctx.rotate(0.5 * Math.PI);
        ctx.scale(1, -1);
        break;
      case 6:
        // 90 rotate right
        ctx.rotate(0.5 * Math.PI);
        ctx.translate(0, -height);
        break;
      case 7:
        // horizontal flip + 90 rotate right
        ctx.rotate(0.5 * Math.PI);
        ctx.translate(width, -height);
        ctx.scale(-1, 1);
        break;
      case 8:
        // 90 rotate left
        ctx.rotate(-0.5 * Math.PI);
        ctx.translate(-width, 0);
        break;
      default:
        break;
    }
  }

  var URL = window.URL && window.URL.createObjectURL ? window.URL :
            window.webkitURL && window.webkitURL.createObjectURL ? window.webkitURL :
            null;

  /**
   * MegaPixImage class
   */
  function MegaPixImage(srcImage) {
    if (window.Blob && srcImage instanceof Blob) {
      if (!URL) { throw Error("No createObjectURL function found to create blob url"); }
      var img = new Image();
      img.src = URL.createObjectURL(srcImage);
      this.blob = srcImage;
      srcImage = img;
    }
    if (!srcImage.naturalWidth && !srcImage.naturalHeight) {
      var _this = this;
      srcImage.onload = srcImage.onerror = function() {
        var listeners = _this.imageLoadListeners;
        if (listeners) {
          _this.imageLoadListeners = null;
          for (var i=0, len=listeners.length; i<len; i++) {
            listeners[i]();
          }
        }
      };
      this.imageLoadListeners = [];
    }
    this.srcImage = srcImage;
  }

  /**
   * Rendering megapix image into specified target element
   */
  MegaPixImage.prototype.render = function(target, options, callback) {
    if (this.imageLoadListeners) {
      var _this = this;
      this.imageLoadListeners.push(function() { _this.render(target, options, callback); });
      return;
    }
    options = options || {};
    var imgWidth = this.srcImage.naturalWidth, imgHeight = this.srcImage.naturalHeight,
        width = options.width, height = options.height,
        maxWidth = options.maxWidth, maxHeight = options.maxHeight,
        doSquash = !this.blob || this.blob.type === 'image/jpeg';
    if (width && !height) {
      height = (imgHeight * width / imgWidth) << 0;
    } else if (height && !width) {
      width = (imgWidth * height / imgHeight) << 0;
    } else {
      width = imgWidth;
      height = imgHeight;
    }
    if (maxWidth && width > maxWidth) {
      width = maxWidth;
      height = (imgHeight * width / imgWidth) << 0;
    }
    if (maxHeight && height > maxHeight) {
      height = maxHeight;
      width = (imgWidth * height / imgHeight) << 0;
    }
    var opt = { width : width, height : height };
    for (var k in options) opt[k] = options[k];

    var tagName = target.tagName.toLowerCase();
    if (tagName === 'img') {
      target.src = renderImageToDataURL(this.srcImage, opt, doSquash);
    } else if (tagName === 'canvas') {
      renderImageToCanvas(this.srcImage, target, opt, doSquash);
    }
    if (typeof this.onrender === 'function') {
      this.onrender(target);
    }
    if (callback) {
      callback();
    }
    if (this.blob) {
      this.blob = null;
      URL.revokeObjectURL(this.srcImage.src);
    }
  };

  /**
   * Export class to global
   */
  if (typeof define === 'function' && define.amd) {
    define([], function() { return MegaPixImage; }); // for AMD loader
  } else if (typeof exports === 'object') {
    module.exports = MegaPixImage; // for CommonJS
  } else {
    this.MegaPixImage = MegaPixImage;
  }

})();

```

compress-image.js 对开源库做了简单封装

```javascript
//************压缩图片************************************************************
/**
 * 压缩图片
 * @param base64code //被压缩图片的base64编码
 * @param maxWidth //压缩后图片最大宽度
 * @param maxHeight //压缩后图片的最大高度
 * @param callback(dataUrl) 压缩回调方法,参数为压缩后的url，若压缩失败，则返回"";
 * @returns
 */
function compressImg(base64code,maxWidth,maxHeight,callback) {
    //var base64code = "";
    var image = new Image();
    image.src = base64code;
    var dataURL = "";
    imgLoad(image, function() {
        //解决canvas无法读取画布问题
        image.setAttribute('crossOrigin', 'anonymous');
        var mpImg = new MegaPixImage(image);
        //console.log('加载完毕')
        var resCanvas2 =document.createElement("canvas");
        if(isIOS()){
        	mpImg.render(resCanvas2, {maxWidth: maxWidth, maxHeight: maxHeight, orientation: 4});
        }else{
        	mpImg.render(resCanvas2, {maxWidth: maxWidth, maxHeight: maxHeight, orientation: 0});
        }
        dataURL = resCanvas2.toDataURL("image/jpeg");
        callback(dataURL);
    });
   // return dataURL;
}
function imgLoad(img, callback) {
    var timer = setInterval(function() {
        if (img.complete) {
            callback(img)
            clearInterval(timer)
        }
    }, 50)
}
//********************************************************************************************
function isIOS(){
	var userAgentInfo = navigator.userAgent;    
	var Agents = new Array("iPhone","iPad", "iPod"); /*"Android",  */
	var flag = false;  
	var v=0  
	for ( v = 0; v < Agents.length; v++){    
	    if (userAgentInfo.indexOf(Agents[v]) > 0) { 
	    	flag = true; break; 
	   	}    
	}    
	return flag;
}
//********************************************************************************************
function dataURLToBlob(dataURL) {
    var BASE64_MARKER = ';base64,';
    var parts, contentType, raw;
    if (dataURL.indexOf(BASE64_MARKER) == -1) {
        parts = dataURL.split(',');
        contentType = parts[0].split(':')[1];
        raw = decodeURIComponent(parts[1]);

        return new Blob([raw], {type: contentType});
    }

    parts = dataURL.split(BASE64_MARKER);
    contentType = parts[0].split(':')[1];
    raw = window.atob(parts[1]);
    var rawLength = raw.length;

    var uInt8Array = new Uint8Array(rawLength);

    for (var i = 0; i < rawLength; ++i) {
        uInt8Array[i] = raw.charCodeAt(i);
    }

    return new Blob([uInt8Array], {type: contentType});
}
```

#### 粘贴库
paste.js 开源项目
```javascript
// 源地址 https://github.com/layerssss/paste.js/
(function() {
  var $, Paste, createHiddenEditable, dataURLtoBlob, isFocusable;

  $ = window.jQuery;

  $.paste = function(pasteContainer) {
    var pm;
    if (typeof console !== "undefined" && console !== null) {
      console.log("DEPRECATED: This method is deprecated. Please use $.fn.pastableNonInputable() instead.");
    }
    pm = Paste.mountNonInputable(pasteContainer);
    return pm._container;
  };

  $.fn.pastableNonInputable = function() {
    var el, j, len, ref;
    ref = this;
    for (j = 0, len = ref.length; j < len; j++) {
      el = ref[j];
      if (el._pastable || $(el).is('textarea, input:text, [contenteditable]')) {
        continue;
      }
      Paste.mountNonInputable(el);
      el._pastable = true;
    }
    return this;
  };

  $.fn.pastableTextarea = function() {
    var el, j, len, ref;
    ref = this;
    for (j = 0, len = ref.length; j < len; j++) {
      el = ref[j];
      if (el._pastable || $(el).is(':not(textarea, input:text)')) {
        continue;
      }
      Paste.mountTextarea(el);
      el._pastable = true;
    }
    return this;
  };

  $.fn.pastableContenteditable = function() {
    var el, j, len, ref;
    ref = this;
    for (j = 0, len = ref.length; j < len; j++) {
      el = ref[j];
      if (el._pastable || $(el).is(':not([contenteditable])')) {
        continue;
      }
      Paste.mountContenteditable(el);
      el._pastable = true;
    }
    return this;
  };

  dataURLtoBlob = function(dataURL, sliceSize) {
    var b64Data, byteArray, byteArrays, byteCharacters, byteNumbers, contentType, i, m, offset, ref, slice;
    if (sliceSize == null) {
      sliceSize = 512;
    }
    if (!(m = dataURL.match(/^data\:([^\;]+)\;base64\,(.+)$/))) {
      return null;
    }
    ref = m, m = ref[0], contentType = ref[1], b64Data = ref[2];
    byteCharacters = atob(b64Data);
    byteArrays = [];
    offset = 0;
    while (offset < byteCharacters.length) {
      slice = byteCharacters.slice(offset, offset + sliceSize);
      byteNumbers = new Array(slice.length);
      i = 0;
      while (i < slice.length) {
        byteNumbers[i] = slice.charCodeAt(i);
        i++;
      }
      byteArray = new Uint8Array(byteNumbers);
      byteArrays.push(byteArray);
      offset += sliceSize;
    }
    return new Blob(byteArrays, {
      type: contentType
    });
  };

  createHiddenEditable = function() {
    return $(document.createElement('div')).attr('contenteditable', true).attr('aria-hidden', true).attr('tabindex', -1).css({
      width: 1,
      height: 1,
      position: 'fixed',
      left: -100,
      overflow: 'hidden'
    });
  };

  isFocusable = function(element, hasTabindex) {
    var fieldset, focusableIfVisible, img, map, mapName, nodeName;
    map = void 0;
    mapName = void 0;
    img = void 0;
    focusableIfVisible = void 0;
    fieldset = void 0;
    nodeName = element.nodeName.toLowerCase();
    if ('area' === nodeName) {
      map = element.parentNode;
      mapName = map.name;
      if (!element.href || !mapName || map.nodeName.toLowerCase() !== 'map') {
        return false;
      }
      img = $('img[usemap=\'#' + mapName + '\']');
      return img.length > 0 && img.is(':visible');
    }
    if (/^(input|select|textarea|button|object)$/.test(nodeName)) {
      focusableIfVisible = !element.disabled;
      if (focusableIfVisible) {
        fieldset = $(element).closest('fieldset')[0];
        if (fieldset) {
          focusableIfVisible = !fieldset.disabled;
        }
      }
    } else if ('a' === nodeName) {
      focusableIfVisible = element.href || hasTabindex;
    } else {
      focusableIfVisible = hasTabindex;
    }
    focusableIfVisible = focusableIfVisible || $(element).is('[contenteditable]');
    return focusableIfVisible && $(element).is(':visible');
  };

  Paste = (function() {
    Paste.prototype._target = null;

    Paste.prototype._container = null;

    Paste.mountNonInputable = function(nonInputable) {
      var paste;
      paste = new Paste(createHiddenEditable().appendTo(nonInputable), nonInputable);
      $(nonInputable).on('click', (function(_this) {
        return function(ev) {
          if (!isFocusable(ev.target, false)) {
            return paste._container.focus();
          }
        };
      })(this));
      paste._container.on('focus', (function(_this) {
        return function() {
          return $(nonInputable).addClass('pastable-focus');
        };
      })(this));
      return paste._container.on('blur', (function(_this) {
        return function() {
          return $(nonInputable).removeClass('pastable-focus');
        };
      })(this));
    };

    Paste.mountTextarea = function(textarea) {
      var ctlDown, paste, ref, ref1;
      if ((typeof DataTransfer !== "undefined" && DataTransfer !== null ? DataTransfer.prototype : void 0) && ((ref = Object.getOwnPropertyDescriptor) != null ? (ref1 = ref.call(Object, DataTransfer.prototype, 'items')) != null ? ref1.get : void 0 : void 0)) {
        return this.mountContenteditable(textarea);
      }
      paste = new Paste(createHiddenEditable().insertBefore(textarea), textarea);
      ctlDown = false;
      $(textarea).on('keyup', function(ev) {
        var ref2;
        if ((ref2 = ev.keyCode) === 17 || ref2 === 224) {
          ctlDown = false;
        }
        return null;
      });
      $(textarea).on('keydown', function(ev) {
        var ref2;
        if ((ref2 = ev.keyCode) === 17 || ref2 === 224) {
          ctlDown = true;
        }
        if ((ev.ctrlKey != null) && (ev.metaKey != null)) {
          ctlDown = ev.ctrlKey || ev.metaKey;
        }
        if (ctlDown && ev.keyCode === 86) {
          paste._textarea_focus_stolen = true;
          paste._container.focus();
          paste._paste_event_fired = false;
          setTimeout((function(_this) {
            return function() {
              if (!paste._paste_event_fired) {
                $(textarea).focus();
                return paste._textarea_focus_stolen = false;
              }
            };
          })(this), 1);
        }
        return null;
      });
      $(textarea).on('paste', (function(_this) {
        return function() {};
      })(this));
      $(textarea).on('focus', (function(_this) {
        return function() {
          if (!paste._textarea_focus_stolen) {
            return $(textarea).addClass('pastable-focus');
          }
        };
      })(this));
      $(textarea).on('blur', (function(_this) {
        return function() {
          if (!paste._textarea_focus_stolen) {
            return $(textarea).removeClass('pastable-focus');
          }
        };
      })(this));
      $(paste._target).on('_pasteCheckContainerDone', (function(_this) {
        return function() {
          $(textarea).focus();
          return paste._textarea_focus_stolen = false;
        };
      })(this));
      return $(paste._target).on('pasteText', (function(_this) {
        return function(ev, data) {
          var content, curEnd, curStart;
          curStart = $(textarea).prop('selectionStart');
          curEnd = $(textarea).prop('selectionEnd');
          content = $(textarea).val();
          $(textarea).val("" + content.slice(0, curStart) + data.text + content.slice(curEnd));
          $(textarea)[0].setSelectionRange(curStart + data.text.length, curStart + data.text.length);
          return $(textarea).trigger('change');
        };
      })(this));
    };

    Paste.mountContenteditable = function(contenteditable) {
      var paste;
      paste = new Paste(contenteditable, contenteditable);
      $(contenteditable).on('focus', (function(_this) {
        return function() {
          return $(contenteditable).addClass('pastable-focus');
        };
      })(this));
      return $(contenteditable).on('blur', (function(_this) {
        return function() {
          return $(contenteditable).removeClass('pastable-focus');
        };
      })(this));
    };

    function Paste(_container, _target) {
      this._container = _container;
      this._target = _target;
      this._container = $(this._container);
      this._target = $(this._target).addClass('pastable');
      this._container.on('paste', (function(_this) {
        return function(ev) {
          var clipboardData, file, item, j, k, len, len1, reader, ref, ref1, ref2, ref3, text;
          if (ev.currentTarget !== ev.target) {
            return ev.preventDefault();
          }
          _this._paste_event_fired = true;
          if (((ref = ev.originalEvent) != null ? ref.clipboardData : void 0) != null) {
            clipboardData = ev.originalEvent.clipboardData;
            if (clipboardData.items) {
              ref1 = clipboardData.items;
              for (j = 0, len = ref1.length; j < len; j++) {
                item = ref1[j];
                if (item.type.match(/^image\//)) {
                  reader = new FileReader();
                  reader.onload = function(event) {
                    return _this._handleImage(event.target.result);
                  };
                  try {
                    reader.readAsDataURL(item.getAsFile());
                  } catch (error) {}
                  ev.preventDefault();
                  break;
                }
                if (item.type === 'text/plain') {
                  item.getAsString(function(string) {
                    return _this._target.trigger('pasteText', {
                      text: string
                    });
                  });
                }
              }
            } else {
              if (-1 !== Array.prototype.indexOf.call(clipboardData.types, 'text/plain')) {
                text = clipboardData.getData('Text');
                setTimeout(function() {
                  return _this._target.trigger('pasteText', {
                    text: text
                  });
                }, 1);
              }
              _this._checkImagesInContainer(function(src) {
                return _this._handleImage(src);
              });
            }
          }
          if (clipboardData = window.clipboardData) {
            if ((ref2 = (text = clipboardData.getData('Text'))) != null ? ref2.length : void 0) {
              setTimeout(function() {
                _this._target.trigger('pasteText', {
                  text: text
                });
                return _this._target.trigger('_pasteCheckContainerDone');
              }, 1);
            } else {
              ref3 = clipboardData.files;
              for (k = 0, len1 = ref3.length; k < len1; k++) {
                file = ref3[k];
                _this._handleImage(URL.createObjectURL(file));
              }
              _this._checkImagesInContainer(function(src) {});
            }
          }
          return null;
        };
      })(this));
    }

    Paste.prototype._handleImage = function(src) {
      var loader;
      if (src.match(/^webkit\-fake\-url\:\/\//)) {
        return this._target.trigger('pasteImageError', {
          message: "You are trying to paste an image in Safari, however we are unable to retieve its data."
        });
      }
      loader = new Image();
      loader.crossOrigin = "anonymous";
      loader.onload = (function(_this) {
        return function() {
          var blob, canvas, ctx, dataURL;
          canvas = document.createElement('canvas');
          canvas.width = loader.width;
          canvas.height = loader.height;
          ctx = canvas.getContext('2d');
          ctx.drawImage(loader, 0, 0, canvas.width, canvas.height);
          dataURL = null;
          try {
            dataURL = canvas.toDataURL('image/png');
            blob = dataURLtoBlob(dataURL);
          } catch (error) {}
          if (dataURL) {
            return _this._target.trigger('pasteImage', {
              blob: blob,
              dataURL: dataURL,
              width: loader.width,
              height: loader.height
            });
          }
        };
      })(this);
      loader.onerror = (function(_this) {
        return function() {
          return _this._target.trigger('pasteImageError', {
            message: "Failed to get image from: " + src,
            url: src
          });
        };
      })(this);
      return loader.src = src;
    };

    Paste.prototype._checkImagesInContainer = function(cb) {
      var img, j, len, ref, timespan;
      timespan = Math.floor(1000 * Math.random());
      ref = this._container.find('img');
      for (j = 0, len = ref.length; j < len; j++) {
        img = ref[j];
        img["_paste_marked_" + timespan] = true;
      }
      return setTimeout((function(_this) {
        return function() {
          var k, len1, ref1;
          ref1 = _this._container.find('img');
          for (k = 0, len1 = ref1.length; k < len1; k++) {
            img = ref1[k];
            if (!img["_paste_marked_" + timespan]) {
              cb(img.src);
              $(img).remove();
            }
          }
          return _this._target.trigger('_pasteCheckContainerDone');
        };
      })(this), 1);
    };

    return Paste;

  })();

}).call(this);

```


