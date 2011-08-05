(function(b){var E={hintText:"Type in a search term",noResultsText:"No results",searchingText:"Searching...",deleteText:"&times;",tokenLimit:null,allowCustomEntry:!1,preventDuplicates:!1,searchColumns:["name"],parseName:null,escapeHTML:!0,searchDelay:300,minChars:1,makeSortable:!1,animateDropdown:!0,method:"GET",contentType:"json",queryParam:"q",jsonContainer:null,prePopulate:null,processPrePopulate:!1,tokenDelimiter:",",tokenQuote:"'",tokenQuoteEscaped:"\\'",tokensFormatter:null,onResult:null,onAdd:null,
onDelete:null},F={tokenList:"token-input-list",tokenListFocused:"token-input-focus",token:"token-input-token",tokenDelete:"token-input-delete-token",selectedToken:"token-input-selected-token",highlightedToken:"token-input-highlighted-token",draggedToken:"token-input-dragged-token",draggedClone:"token-input-dragged-clone",dropdown:"token-input-dropdown",dropdownItem:"token-input-dropdown-item",dropdownItem2:"token-input-dropdown-item2",selectedDropdownItem:"token-input-selected-dropdown-item",inputToken:"token-input-input-token",
insertBefore:"token-input-insert-before",insertAfter:"token-input-insert-after"},k={BEFORE:0,AFTER:1,END:2},h={BACKSPACE:8,TAB:9,ENTER:13,ESCAPE:27,SPACE:32,PAGE_UP:33,PAGE_DOWN:34,END:35,HOME:36,LEFT:37,UP:38,RIGHT:39,DOWN:40,DELETE:46,NUMPAD_ENTER:108,COMMA:188},y={init:function(h,r){var a=b.extend({},E,r||{});return this.each(function(){b(this).data("tokenInputObject",new b.TokenList(this,h,a))})},clear:function(){this.data("tokenInputObject").clear();return this},add:function(b){this.data("tokenInputObject").add(b);
return this},remove:function(b){this.data("tokenInputObject").remove(b);return this}};b.fn.tokenInput=function(b){return y[b]?y[b].apply(this,Array.prototype.slice.call(arguments,1)):y.init.apply(this,arguments)};b.TokenList=function(l,r,a){function v(c){var d;M++;d="u"+M;var e;e=a.parseName?a.parseName(c):"<p>"+N(c.name)+"</p>";e=b("<li>"+e+"</li>").addClass(a.classes.token).insertBefore(o).attr("data-uniqueid",d);a.makeSortable&&y(e);b("<span>"+a.deleteText+"</span>").addClass(a.classes.tokenDelete).appendTo(e).click(function(){z(b(this).parent());
return!1});b.data(e.get(0),"tokeninput",c);A[d]=c;G();s++;b.map(A,function(b){return b.id});t+=1;return e}function B(c){var d=typeof c==="string"?{name:c}:c[0]?b.data(c.get(0),"tokeninput"):c;if(!d)return!1;c=a.onAdd;if(t>0&&a.preventDuplicates){var e=null;j.children().each(function(){var a=b(this),c=b.data(a.get(0),"tokeninput");if(c){if(c.id&&c.id===d.id)return e=a,!1;if(!c.id&&c.name===d.name)return e=a,!1}});if(e){u(e);o.insertAfter(e);f.focus();return}}v(d);f.val("");a.tokenLimit!==null&&t>=
a.tokenLimit?f.hide():f.focus();p();b.isFunction(c)&&c.call(m,d)}function y(c){c.bind("mousedown",function(){var c=b(this);O=c;P=window.setTimeout(function(){if(g!=c){g&&n(b(g),k.END);u(c);var e=b(c).position();b(c).clone().appendTo("body").addClass(a.classes.draggedClone).css({top:e.top,left:e.left});c.addClass(a.classes.draggedToken);w=!0}},200);b(document).one("mouseup",function(){window.clearTimeout(P);if(w==!0&&(w=!1,b("li."+a.classes.draggedClone).remove(),b("li."+a.classes.draggedToken).removeClass(a.classes.draggedToken),
g&&n(b(g),k.END),x)){var e=x;e&&c.get(0)!=e.get(0)&&(Q(c,e)?c.insertAfter(e):c.insertBefore(e));U()}});return!1}).bind("mouseover",function(){w&&(x=b(this),Q(O,x)?x.addClass(a.classes.insertAfter):x.addClass(a.classes.insertBefore))}).bind("mouseout",function(){w&&(b(this).removeClass(a.classes.insertBefore),b(this).removeClass(a.classes.insertAfter))}).bind("mouseup",function(){b(this).removeClass(a.classes.insertBefore);b(this).removeClass(a.classes.insertAfter)});b("body").mousemove(function(c){w&&
b("li."+a.classes.draggedClone).css({top:c.pageY,left:c.pageX})})}function Q(c,a){E();c=b.data(c.get(0),"tokeninput");a=b.data(a.get(0),"tokeninput");if(c&&a)return a.index>c.index}function E(){var c=0;j.find("li").each(function(){var a=b.data(this,"tokeninput");if(a)a.index=c;c++})}function U(){var c=[],a=[];j.find("li").each(function(){var e=b.data(this,"tokeninput");e&&(c.push(e.id),a.push(e))});A=a;G()}function u(c){c.addClass(a.classes.selectedToken);g=c.get(0);f.val("").css("color","transparent");
p()}function n(c,b){c.removeClass(a.classes.selectedToken);g=null;f.css("color","");b===k.BEFORE?(o.insertBefore(c),s--):b===k.AFTER?(o.insertAfter(c),s++):(o.appendTo(j),s=t);f.focus()}function z(c){var d=b.data(c.get(0),"tokeninput"),e=a.onDelete,H=c.prevAll().length;H>s&&H--;var h=b(c).attr("data-uniqueid");c.remove();g=null;f.focus().css("color","");delete A[h];G();H<s&&s--;t-=1;a.tokenLimit!==null&&f.show().val("").focus();b.isFunction(e)&&e.call(m,d)}function V(c){var d=[],e=RegExp(a.tokenQuote,
"gi");b.each(c,function(c,b){d.push(b.id?b.id:a.tokenQuote+b.name.replace(e,a.tokenQuoteEscaped)+a.tokenQuote)});return d.join(a.tokenDelimiter)}function G(){m.val((a.tokensFormatter||V)(A))}function p(){q.hide().empty();i=null}function C(){q.css({position:"absolute",top:b(j).offset().top+b(j).outerHeight(),left:b(j).offset().left,zindex:999,width:b(j).width()}).show()}function W(a,b){for(var e=a.toString().removeDiacritics().toLowerCase().replace(/[<>]+/g,""),g=b.toString().removeDiacritics().toLowerCase().replace(/[<>]+/g,
""),e=e.replace(RegExp(g,"g"),"<"+g+">"),g=0,f="",h=0;h<e.length;h++){var i=a.charAt(g),l=e.charAt(h);l==="<"?f+="<b>":l===">"?f+="</b>":(g+=1,f+=i)}return f}function I(c,d){if(d&&d.length){q.empty();var e=b("<ul>").appendTo(q).mouseover(function(a){D(b(a.target).closest("li"))}).mousedown(function(a){B(b(a.target).closest("li"));return!1}).hide();b.each(d,function(d,g){var f;f=a.parseName?a.parseName(g):g.name;f=b("<li>"+W(N(f),c)+"</li>").appendTo(e);d%2?f.addClass(a.classes.dropdownItem):f.addClass(a.classes.dropdownItem2);
a.allowCustomEntry==!1&&d===0&&D(f);b.data(f.get(0),"tokeninput",g)});C();a.animateDropdown?e.slideDown("fast"):e.show()}else a.noResultsText&&!a.allowCustomEntry?(q.html("<p>"+a.noResultsText+"</p>"),C()):p()}function D(c){c&&(i&&J(b(i)),c.addClass(a.classes.selectedDropdownItem),i=c.get(0))}function J(b){b.removeClass(a.classes.selectedDropdownItem);i=null}function N(c){if(!a.escapeHTML)return c;return b("<p></p>").text(c).html()}function R(){var c=f.val();if(a.tokenLimit!==null&&t>=a.tokenLimit)return!1;
c&&c.length&&(g&&n(b(g),k.AFTER),c.length>=a.minChars?(a.searchingText&&(q.html("<p>"+a.searchingText+"</p>"),C()),clearTimeout(S),S=setTimeout(function(){X(c)},a.searchDelay)):p())}function X(c){var d=K.get(c.toLowerCase());if(d)I(c.toLowerCase(),d);else if(a.url){var e={data:{}};a.url.indexOf("?")>-1?(d=a.url.split("?"),e.url=d[0],d=d[1].split("&"),b.each(d,function(a,b){var c=b.split("=");e.data[c[0]]=c[1]})):e.url=a.url;e.data[a.queryParam]=c;e.type=a.method;e.dataType=a.contentType;if(a.crossDomain)e.dataType=
"jsonp";e.success=function(d){b.isFunction(a.onResult)&&(d=a.onResult.call(m,d));K.add(c,a.jsonContainer?d[a.jsonContainer]:d);f.val().toLowerCase()===c.toLowerCase()&&I(c,a.jsonContainer?d[a.jsonContainer]:d)};b.ajax(e)}else a.local_data&&(d=b.grep(a.local_data,function(d){var e=!1;b(a.searchColumns).each(function(a,b){d[b].toString().toLowerCase().removeDiacritics().indexOf(c.toString().toLowerCase().removeDiacritics())>-1&&(e=!0)});return e}),b.isFunction(a.onResult)&&(d=a.onResult.call(m,d)),
K.add(c,d),I(c,d))}if(typeof r==="string"){if(a.url=r,a.crossDomain===void 0)a.crossDomain=a.url.indexOf("://")===-1?!1:location.href.split(/\/+/g)[1]!==a.url.split(/\/+/g)[1]}else if(typeof r==="function")a.sourceFunction=r;else if(typeof r==="object")a.local_data=r;a.classes?a.classes=b.extend({},F,a.classes):a.theme?(a.classes={},b.each(F,function(b,d){a.classes[b]=d+"-"+a.theme})):a.classes=F;var A={},t=0,K=new b.TokenList.Cache,S,L,f=b('<input type="text"  autocomplete="off">').css({outline:"none"}).focus(function(){if((a.tokenLimit===
null||a.tokenLimit!==t)&&a.hintText)q.html("<p>"+a.hintText+"</p>"),C();b(f).is(":visible")&&j.addClass(a.classes.tokenListFocused)}).blur(function(){g&&n(b(g));j.removeClass(a.classes.tokenListFocused);p()}).bind("keyup keydown blur update",function(){if(L!==(L=f.val())){var a=L.replace(/&/g,"&amp;").replace(/\s/g," ").replace(/</g,"&lt;").replace(/>/g,"&gt;");T.html(a);f.width(T.width()+30)}}).keydown(function(c){var d,e;switch(c.keyCode){case h.LEFT:case h.RIGHT:case h.UP:case h.DOWN:if(b(this).val())return d=
null,a.allowCustomEntry==!0?(c.keyCode===h.DOWN?b(i).length?b(i).next().length?d=b(i).next():J(b(i)):d=b(q).find("li:first-child"):c.keyCode===h.UP&&(b(i).length?b(i).prev().length?d=b(i).prev():J(b(i)):d=b(q).find("li:last-child")),d!=null&&D(d)):(c.keyCode===h.DOWN?d=b(i).next():c.keyCode===h.UP&&(d=b(i).prev()),d&&d.length&&D(d)),c.keyCode===h.LEFT||c.keyCode===h.RIGHT?!0:!1;else if(d=o.prev(),e=o.next(),d.length&&d.get(0)===g||e.length&&e.get(0)===g)c.keyCode===h.LEFT||c.keyCode===h.UP?n(b(g),
k.BEFORE):n(b(g),k.AFTER);else if((c.keyCode===h.LEFT||c.keyCode===h.UP)&&d.length)g&&n(b(g)),u(b(d.get(0)));else if((c.keyCode===h.RIGHT||c.keyCode===h.DOWN)&&e.length)g&&n(b(g)),u(b(e.get(0)));break;case h.BACKSPACE:d=o.prev();if(b(this).val().length)b(this).val().length===1?p():setTimeout(function(){R()},5);else return g?z(b(g)):d.length&&u(b(d.get(0))),!1;break;case h.DELETE:e=o.next();b(this).val().length||(g?z(b(g)):e.length&&u(b(e.get(0))));break;case h.TAB:case h.ENTER:case h.NUMPAD_ENTER:case h.COMMA:if(c.keyCode==
h.TAB&&!b(f).val().length)return p(),!0;i&&B(b(i));a.allowCustomEntry==!0&&b.trim(b(f).val())!=""&&B(b(f).val());return!1;case h.ESCAPE:return p(),!0;default:String.fromCharCode(c.which)&&setTimeout(function(){R()},5)}}),M=0;l.type="hidden";var m=b(l).val("").focus(function(){f.focus()}).blur(function(){f.blur()});f.attr({tabindex:m.attr("tabindex")});var g=null,s=0,i=null,j=b("<ul />").addClass(a.classes.tokenList+" "+m.attr("class")).click(function(a){if((a=b(a.target).closest("li"))&&a.get(0)&&
b.data(a.get(0),"tokeninput")){f.focus();var d=g;g&&n(b(g),k.END);d===a.get(0)?n(a,k.END):u(a)}else g&&n(b(g),k.END),f.focus()}).mouseover(function(c){(c=b(c.target).closest("li"))&&g!==this&&c.addClass(a.classes.highlightedToken)}).mouseout(function(c){(c=b(c.target).closest("li"))&&g!==this&&c.removeClass(a.classes.highlightedToken)}).insertBefore(m),o=b("<li />").addClass(a.classes.inputToken).appendTo(j).append(f),q=b("<div>").addClass(a.classes.dropdown).appendTo("body").hide(),T=b("<tester/>").insertAfter(f).css({position:"absolute",
top:-9999,left:-9999,width:"auto",fontSize:f.css("fontSize"),fontFamily:f.css("fontFamily"),fontWeight:f.css("fontWeight"),letterSpacing:f.css("letterSpacing"),whiteSpace:"nowrap"}),w=!1,P,O,x;m.val("");l=a.prePopulate||m.data("pre");a.processPrePopulate&&b.isFunction(a.onResult)&&(l=a.onResult.call(m,l));l&&l.length&&(b.each(l,function(b,d){if(a.tokenLimit==null||a.tokenLimit>=b+1)v(d);else return!1}),l.length>=a.tokenLimit&&a.tokenLimit!=null&&(f.hide(),p()));this.clear=function(){j.children("li").each(function(){b(this).children("input").length===
0&&z(b(this))})};this.add=function(a){B(a)};this.remove=function(a){j.children("li[data-uniqueid]").each(function(){var d=b(this).data("tokeninput"),e=!0,f;for(f in a)if(a[f]!==d[f]){e=!1;break}e&&z(b(this))})}};String.prototype.removeDiacritics=function(){if(!this)return"";for(var b={"\u1e9a":"a","\u00c1":"a","\u00e1":"a","\u00c0":"a","\u00e0":"a","\u0102":"a","\u0103":"a","\u1eae":"a","\u1eaf":"a","\u1eb0":"a","\u1eb1":"a","\u1eb4":"a","\u1eb5":"a","\u1eb2":"a","\u1eb3":"a","\u00c2":"a","\u00e2":"a",
"\u1ea4":"a","\u1ea5":"a","\u1ea6":"a","\u1ea7":"a","\u1eaa":"a","\u1eab":"a","\u1ea8":"a","\u1ea9":"a","\u01cd":"a","\u01ce":"a","\u00c5":"a","\u00e5":"a","\u01fa":"a","\u01fb":"a","\u00c4":"a","\u00e4":"a","\u01de":"a","\u01df":"a","\u00c3":"a","\u00e3":"a","\u0226":"a","\u0227":"a","\u01e0":"a","\u01e1":"a","\u0104":"a","\u0105":"a","\u0100":"a","\u0101":"a","\u1ea2":"a","\u1ea3":"a","\u0200":"a","\u0201":"a","\u0202":"a","\u0203":"a","\u1ea0":"a","\u1ea1":"a","\u1eb6":"a","\u1eb7":"a","\u1eac":"a",
"\u1ead":"a","\u1e00":"a","\u1e01":"a","\u023a":"a","\u2c65":"a","\u01fc":"a","\u01fd":"a","\u01e2":"a","\u01e3":"a","\u1e02":"b","\u1e03":"b","\u1e04":"b","\u1e05":"b","\u1e06":"b","\u1e07":"b","\u0243":"b","\u0180":"b","\u1d6c":"b","\u0181":"b","\u0253":"b","\u0182":"b","\u0183":"b","\u0106":"c","\u0107":"c","\u0108":"c","\u0109":"c","\u010c":"c","\u010d":"c","\u010a":"c","\u010b":"c","\u00c7":"c","\u00e7":"c","\u1e08":"c","\u1e09":"c","\u023b":"c","\u023c":"c","\u0187":"c","\u0188":"c","\u0255":"c",
"\u010e":"d","\u010f":"d","\u1e0a":"d","\u1e0b":"d","\u1e10":"d","\u1e11":"d","\u1e0c":"d","\u1e0d":"d","\u1e12":"d","\u1e13":"d","\u1e0e":"d","\u1e0f":"d","\u0110":"d","\u0111":"d","\u1d6d":"d","\u0189":"d","\u0256":"d","\u018a":"d","\u0257":"d","\u018b":"d","\u018c":"d","\u0221":"d","\u00f0":"d","\u00c9":"e","\u018f":"e","\u018e":"e","\u01dd":"e","\u00e9":"e","\u00c8":"e","\u00e8":"e","\u0114":"e","\u0115":"e","\u00ca":"e","\u00ea":"e","\u1ebe":"e","\u1ebf":"e","\u1ec0":"e","\u1ec1":"e","\u1ec4":"e",
"\u1ec5":"e","\u1ec2":"e","\u1ec3":"e","\u011a":"e","\u011b":"e","\u00cb":"e","\u00eb":"e","\u1ebc":"e","\u1ebd":"e","\u0116":"e","\u0117":"e","\u0228":"e","\u0229":"e","\u1e1c":"e","\u1e1d":"e","\u0118":"e","\u0119":"e","\u0112":"e","\u0113":"e","\u1e16":"e","\u1e17":"e","\u1e14":"e","\u1e15":"e","\u1eba":"e","\u1ebb":"e","\u0204":"e","\u0205":"e","\u0206":"e","\u0207":"e","\u1eb8":"e","\u1eb9":"e","\u1ec6":"e","\u1ec7":"e","\u1e18":"e","\u1e19":"e","\u1e1a":"e","\u1e1b":"e","\u0246":"e","\u0247":"e",
"\u025a":"e","\u025d":"e","\u1e1e":"f","\u1e1f":"f","\u1d6e":"f","\u0191":"f","\u0192":"f","\u01f4":"g","\u01f5":"g","\u011e":"g","\u011f":"g","\u011c":"g","\u011d":"g","\u01e6":"g","\u01e7":"g","\u0120":"g","\u0121":"g","\u0122":"g","\u0123":"g","\u1e20":"g","\u1e21":"g","\u01e4":"g","\u01e5":"g","\u0193":"g","\u0260":"g","\u0124":"h","\u0125":"h","\u021e":"h","\u021f":"h","\u1e26":"h","\u1e27":"h","\u1e22":"h","\u1e23":"h","\u1e28":"h","\u1e29":"h","\u1e24":"h","\u1e25":"h","\u1e2a":"h","\u1e2b":"h",
H:"h","\u0331":"h","\u1e96":"h","\u0126":"h","\u0127":"h","\u2c67":"h","\u2c68":"h","\u00cd":"i","\u00ed":"i","\u00cc":"i","\u00ec":"i","\u012c":"i","\u012d":"i","\u00ce":"i","\u00ee":"i","\u01cf":"i","\u01d0":"i","\u00cf":"i","\u00ef":"i","\u1e2e":"i","\u1e2f":"i","\u0128":"i","\u0129":"i","\u0130":"i",i:"i","\u012e":"i","\u012f":"i","\u012a":"i","\u012b":"i","\u1ec8":"i","\u1ec9":"i","\u0208":"i","\u0209":"i","\u020a":"i","\u020b":"i","\u1eca":"i","\u1ecb":"i","\u1e2c":"i","\u1e2d":"i",I:"i","\u0131":"i",
"\u0197":"i","\u0268":"i","\u0134":"j","\u0135":"j",J:"j","\u030c":"j","\u01f0":"j","\u0237":"j","\u0248":"j","\u0249":"j","\u029d":"j","\u025f":"j","\u0284":"j","\u1e30":"k","\u1e31":"k","\u01e8":"k","\u01e9":"k","\u0136":"k","\u0137":"k","\u1e32":"k","\u1e33":"k","\u1e34":"k","\u1e35":"k","\u0198":"k","\u0199":"k","\u2c69":"k","\u2c6a":"k","\u0139":"a","\u013a":"l","\u013d":"l","\u013e":"l","\u013b":"l","\u013c":"l","\u1e36":"l","\u1e37":"l","\u1e38":"l","\u1e39":"l","\u1e3c":"l","\u1e3d":"l","\u1e3a":"l",
"\u1e3b":"l","\u0141":"l","\u0142":"l","\u0141":"l","\u0323":"l","\u0142":"l","\u0323":"l","\u013f":"l","\u0140":"l","\u023d":"l","\u019a":"l","\u2c60":"l","\u2c61":"l","\u2c62":"l","\u026b":"l","\u026c":"l","\u026d":"l","\u0234":"l","\u1e3e":"m","\u1e3f":"m","\u1e40":"m","\u1e41":"m","\u1e42":"m","\u1e43":"m","\u0271":"m","\u0143":"n","\u0144":"n","\u01f8":"n","\u01f9":"n","\u0147":"n","\u0148":"n","\u00d1":"n","\u00f1":"n","\u1e44":"n","\u1e45":"n","\u0145":"n","\u0146":"n","\u1e46":"n","\u1e47":"n",
"\u1e4a":"n","\u1e4b":"n","\u1e48":"n","\u1e49":"n","\u019d":"n","\u0272":"n","\u0220":"n","\u019e":"n","\u0273":"n","\u0235":"n",N:"n","\u0308":"n",n:"n","\u0308":"n","\u00d3":"o","\u00f3":"o","\u00d2":"o","\u00f2":"o","\u014e":"o","\u014f":"o","\u00d4":"o","\u00f4":"o","\u1ed0":"o","\u1ed1":"o","\u1ed2":"o","\u1ed3":"o","\u1ed6":"o","\u1ed7":"o","\u1ed4":"o","\u1ed5":"o","\u01d1":"o","\u01d2":"o","\u00d6":"o","\u00f6":"o","\u022a":"o","\u022b":"o","\u0150":"o","\u0151":"o","\u00d5":"o","\u00f5":"o",
"\u1e4c":"o","\u1e4d":"o","\u1e4e":"o","\u1e4f":"o","\u022c":"o","\u022d":"o","\u022e":"o","\u022f":"o","\u0230":"o","\u0231":"o","\u00d8":"o","\u00f8":"o","\u01fe":"o","\u01ff":"o","\u01ea":"o","\u01eb":"o","\u01ec":"o","\u01ed":"o","\u014c":"o","\u014d":"o","\u1e52":"o","\u1e53":"o","\u1e50":"o","\u1e51":"o","\u1ece":"o","\u1ecf":"o","\u020c":"o","\u020d":"o","\u020e":"o","\u020f":"o","\u01a0":"o","\u01a1":"o","\u1eda":"o","\u1edb":"o","\u1edc":"o","\u1edd":"o","\u1ee0":"o","\u1ee1":"o","\u1ede":"o",
"\u1edf":"o","\u1ee2":"o","\u1ee3":"o","\u1ecc":"o","\u1ecd":"o","\u1ed8":"o","\u1ed9":"o","\u019f":"o","\u0275":"o","\u1e54":"p","\u1e55":"p","\u1e56":"p","\u1e57":"p","\u2c63":"p","\u01a4":"p","\u01a5":"p",P:"p","\u0303":"p",p:"p","\u0303":"p","\u02a0":"q","\u024a":"q","\u024b":"q","\u0154":"r","\u0155":"r","\u0158":"r","\u0159":"r","\u1e58":"r","\u1e59":"r","\u0156":"r","\u0157":"r","\u0210":"r","\u0211":"r","\u0212":"r","\u0213":"r","\u1e5a":"r","\u1e5b":"r","\u1e5c":"r","\u1e5d":"r","\u1e5e":"r",
"\u1e5f":"r","\u024c":"r","\u024d":"r","\u1d72":"r","\u027c":"r","\u2c64":"r","\u027d":"r","\u027e":"r","\u1d73":"r","\u00df":"s","\u015a":"s","\u015b":"s","\u1e64":"s","\u1e65":"s","\u015c":"s","\u015d":"s","\u0160":"s","\u0161":"s","\u1e66":"s","\u1e67":"s","\u1e60":"s","\u1e61":"s","\u1e9b":"s","\u015e":"s","\u015f":"s","\u1e62":"s","\u1e63":"s","\u1e68":"s","\u1e69":"s","\u0218":"s","\u0219":"s","\u0282":"s",S:"s","\u0329":"s",s:"s","\u0329":"s","\u00de":"t","\u00fe":"t","\u0164":"t","\u0165":"t",
T:"t","\u0308":"t","\u1e97":"t","\u1e6a":"t","\u1e6b":"t","\u0162":"t","\u0163":"t","\u1e6c":"t","\u1e6d":"t","\u021a":"t","\u021b":"t","\u1e70":"t","\u1e71":"t","\u1e6e":"t","\u1e6f":"t","\u0166":"t","\u0167":"t","\u023e":"t","\u2c66":"t","\u1d75":"t","\u01ab":"t","\u01ac":"t","\u01ad":"t","\u01ae":"t","\u0288":"t","\u0236":"t","\u00da":"u","\u00fa":"u","\u00d9":"u","\u00f9":"u","\u016c":"u","\u016d":"u","\u00db":"u","\u00fb":"u","\u01d3":"u","\u01d4":"u","\u016e":"u","\u016f":"u","\u00dc":"u","\u00fc":"u",
"\u01d7":"u","\u01d8":"u","\u01db":"u","\u01dc":"u","\u01d9":"u","\u01da":"u","\u01d5":"u","\u01d6":"u","\u0170":"u","\u0171":"u","\u0168":"u","\u0169":"u","\u1e78":"u","\u1e79":"u","\u0172":"u","\u0173":"u","\u016a":"u","\u016b":"u","\u1e7a":"u","\u1e7b":"u","\u1ee6":"u","\u1ee7":"u","\u0214":"u","\u0215":"u","\u0216":"u","\u0217":"u","\u01af":"u","\u01b0":"u","\u1ee8":"u","\u1ee9":"u","\u1eea":"u","\u1eeb":"u","\u1eee":"u","\u1eef":"u","\u1eec":"u","\u1eed":"u","\u1ef0":"u","\u1ef1":"u","\u1ee4":"u",
"\u1ee5":"u","\u1e72":"u","\u1e73":"u","\u1e76":"u","\u1e77":"u","\u1e74":"u","\u1e75":"u","\u0244":"u","\u0289":"u","\u1e7c":"v","\u1e7d":"v","\u1e7e":"v","\u1e7f":"v","\u01b2":"v","\u028b":"v","\u1e82":"w","\u1e83":"w","\u1e80":"w","\u1e81":"w","\u0174":"w","\u0175":"w",W:"w","\u030a":"w","\u1e98":"w","\u1e84":"w","\u1e85":"w","\u1e86":"w","\u1e87":"w","\u1e88":"w","\u1e89":"w","\u1e8c":"x","\u1e8d":"x","\u1e8a":"x","\u1e8b":"x","\u00dd":"y","\u00fd":"y","\u1ef2":"y","\u1ef3":"y","\u0176":"y","\u0177":"y",
Y:"y","\u030a":"y","\u1e99":"y","\u0178":"y","\u00ff":"y","\u1ef8":"y","\u1ef9":"y","\u1e8e":"y","\u1e8f":"y","\u0232":"y","\u0233":"y","\u1ef6":"y","\u1ef7":"y","\u1ef4":"y","\u1ef5":"y","\u028f":"y","\u024e":"y","\u024f":"y","\u01b3":"y","\u01b4":"y","\u0179":"z","\u017a":"z","\u1e90":"z","\u1e91":"z","\u017d":"z","\u017e":"z","\u017b":"z","\u017c":"z","\u1e92":"z","\u1e93":"z","\u1e94":"z","\u1e95":"z","\u01b5":"z","\u01b6":"z","\u0224":"z","\u0225":"z","\u0290":"z","\u0291":"z","\u2c6b":"z","\u2c6c":"z",
"\u01ee":"z","\u01ef":"z","\u01ba":"z","\uff12":"2","\uff16":"6","\uff22":"B","\uff26":"F","\uff2a":"J","\uff2e":"N","\uff32":"R","\uff36":"V","\uff3a":"Z","\uff42":"b","\uff46":"f","\uff4a":"j","\uff4e":"n","\uff52":"r","\uff56":"v","\uff5a":"z","\uff11":"1","\uff15":"5","\uff19":"9","\uff21":"A","\uff25":"E","\uff29":"I","\uff2d":"M","\uff31":"Q","\uff35":"U","\uff39":"Y","\uff41":"a","\uff45":"e","\uff49":"i","\uff4d":"m","\uff51":"q","\uff55":"u","\uff59":"y","\uff10":"0","\uff14":"4","\uff18":"8",
"\uff24":"D","\uff28":"H","\uff2c":"L","\uff30":"P","\uff34":"T","\uff38":"X","\uff44":"d","\uff48":"h","\uff4c":"l","\uff50":"p","\uff54":"t","\uff58":"x","\uff13":"3","\uff17":"7","\uff23":"C","\uff27":"G","\uff2b":"K","\uff2f":"O","\uff33":"S","\uff37":"W","\uff43":"c","\uff47":"g","\uff4b":"k","\uff4f":"o","\uff53":"s","\uff57":"w"},h="",a=0;a<this.length;a++)h+=b[this.charAt(a)]||this.charAt(a);return h};b.TokenList.Cache=function(h){var k=b.extend({max_size:500},h),a={},v=0;this.add=function(b,
h){v>k.max_size&&(a={},v=0);a[b]||(v+=1);a[b]=h};this.get=function(b){return a[b]}}})(jQuery);