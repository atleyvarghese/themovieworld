if (self.CavalryLogger) { CavalryLogger.start_js(["zdC4C"]); }

__d("XLynxAsyncCallbackController",["XController"],(function a(b,c,d,e,f,g){f.exports=c("XController").create("/si/linkclick/ajax_callback/",{lynx_uri:{type:"String"}})}),null);
__d("isLinkshimURI",["isBonfireURI","isFacebookURI","isMessengerDotComURI"],(function a(b,c,d,e,f,g){"use strict";function h(i){var j=i.getPath();if((j==="/l.php"||j.indexOf("/si/ajax/l/")===0||j.indexOf("/l/")===0||j.indexOf("l/")===0)&&(c("isFacebookURI")(i)||c("isMessengerDotComURI")(i)||c("isBonfireURI")(i)))return true;return false}f.exports=h}),null);
__d("FBLynx",["$","AsyncSignal","AsyncRequest","BanzaiODS","XLynxAsyncCallbackController","Event","isLinkshimURI","LinkshimHandlerConfig","Parent","Random","URI"],(function a(b,c,d,e,f,g){"use strict";__p&&__p();function h(k){if(!c("isLinkshimURI")(k))return null;var l=k.getQueryData().u;if(!l)return null;return l}function i(k){if(!k)return null;var l=new(c("URI"))(k);if(!c("isLinkshimURI")(l))return null;return l.addQueryData("sig",Math.floor(c("Random").random()*65535+65536)).toString()}var j={alreadySetup:false,setupDelegation:function k(){__p&&__p();var l=arguments.length<=0||arguments[0]===undefined?false:arguments[0];if(document.body==null){if(l)return;setTimeout(function(){j.setupDelegation(true)},100);return}if(j.alreadySetup)return;j.alreadySetup=true;var m=function m(event){__p&&__p();var n=j.getMaybeLynxLink(event.target);if(!n)return;var o=n[0],p=n[1];switch(o){case"async":case"asynclazy":j.logAsyncClick(p);break;case"origin":j.originReferrerPolicyClick(p);break;case"hover":j.hoverClick(p);break}};c("Event").listen(document.body,"click",m);if(c("LinkshimHandlerConfig").middle_click_requires_event)c("Event").listen(document.body,"mouseup",function(event){if(event.button==1)m(event)});c("Event").listen(document.body,"mouseover",function(event){var n=j.getMaybeLynxLink(event.target);if(!n)return;var o=n[0],p=n[1];switch(o){case"async":case"asynclazy":case"origin":case"hover":j.mouseover(p);break}});c("Event").listen(document.body,"contextmenu",function(event){var n=j.getMaybeLynxLink(event.target);if(!n)return;var o=n[0],p=n[1];switch(o){case"async":case"hover":case"origin":j.contextmenu(p);break;case"asynclazy":break}});c("Event").listen(document.body,"mousedown",function(event){var n=j.getMaybeUseSigLink(event.target);if(!n)return;j.mousedownForSig(n)})},getMaybeLynxLink:function k(l){var m=c("Parent").byAttribute(l,"data-lynx-mode");if(m instanceof HTMLAnchorElement){var n=m.getAttribute("data-lynx-mode");switch(n){case"async":case"asynclazy":case"hover":case"origin":return[n,m];default:return null}}return null},getMaybeUseSigLink:function k(l){var m=c("Parent").byAttribute(l,"data-lynx-use-sig");if(m instanceof HTMLAnchorElement)return m;return null},logAsyncClick:function k(l){j.swapLinkWithUnshimmedLink(l);var m=l.getAttribute("data-lynx-uri");if(!m)return;var n=c("XLynxAsyncCallbackController").getURIBuilder().getURI();if(c("LinkshimHandlerConfig").post_request_click_log)new(c("AsyncRequest"))(n).setData({lynx_uri:m}).setErrorHandler(function(){c("BanzaiODS").bumpEntityKey("linkshim","click_log.post.fail")}).send();else new(c("AsyncSignal"))(n,{lynx_uri:m}).send()},originReferrerPolicyClick:function k(l){var m=c("$")("meta_referrer");m.content=c("LinkshimHandlerConfig").switched_meta_referrer_policy;j.logAsyncClick(l);setTimeout(function(){m.content=c("LinkshimHandlerConfig").default_meta_referrer_policy},100)},hoverClick:function k(l){j.revertSwapIfLynxURIPresent(l)},mouseover:function k(l){j.swapLinkWithUnshimmedLink(l)},contextmenu:function k(l){j.revertSwapIfLynxURIPresent(l)},swapLinkWithUnshimmedLink:function k(l){var m=l.href,n=h(new(c("URI"))(m));if(!n)return;l.setAttribute("data-lynx-uri",m);l.href=n},revertSwapIfLynxURIPresent:function k(l){var m=l.getAttribute("data-lynx-uri");if(!m)return;l.removeAttribute("data-lynx-uri");l.href=m},mousedownForSig:function k(l){var m=i(l.getAttribute("data-lynx-uri"));if(m)l.setAttribute("data-lynx-uri",m);var n=i(l.href);if(n)l.href=n}};f.exports=j}),null);