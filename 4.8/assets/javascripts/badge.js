const on_click_badge_name = (text) => {
    const on_error = reason => {
        console.error("Copying text failed:", reason);
        iqwerty.toast.toast("Failed to copy text", options);
    };
    const options = {
        style: {
            main: {
                // Use red as a fallback, so that I will notice (default is light blue)
                "background": "var(--md-primary-fg-color, #2FA4E7)",
                "color": "white",
                "font-size": "20px",
                "font-weight": "bold",
            },
        },
        settings: {
            duration: 1500,
		},
    };
    console.log("Copying text:", text);
    try {
        navigator.clipboard.writeText(text).then(
            () => iqwerty.toast.toast(`Copied "${text}"`, options)
        ).catch(on_error);
    } catch (error) {
        on_error(error);
    }
}

// This is much less likely to cause escaping issues and does not require inline scripts
const register_badge_copy_commands = () => {
    // console.log("badge: registering copy command handlers");
    for (const badge of document.querySelectorAll("span[data-copy-base64]")) {
        // console.log("badge: copy", badge);
        const copy_base64 = badge.getAttribute("data-copy-base64");
        if (copy_base64) {
            const copy_ascii = atob(copy_base64);
            const copy_uint8 = Uint8Array.from(copy_ascii, x => x.codePointAt(0));
            const copy_unicode = new TextDecoder().decode(copy_uint8);
            badge.addEventListener("click", () => {
                on_click_badge_name(copy_unicode);
            });
        }
    }
}
window.addEventListener("load", register_badge_copy_commands);

// https://github.com/mlcheng/js-toast/ - MIT License - Copyright (c) 2016 Michael Cheng
!function(t){"use strict";function n(t,r){var e=r;for(var i in t)e.hasOwnProperty(i)?null!==t[i]&&t[i].constructor===Object&&(e[i]=n(t[i],e[i])):e[i]=t[i];return e}function r(t,n){Object.keys(n).forEach((function(r){t.style[r]=n[r]}))}var e=function(){var t,e,i={SHOW:{"-webkit-transition":"opacity 400ms, -webkit-transform 400ms",transition:"opacity 400ms, transform 400ms",opacity:"1","-webkit-transform":"translateY(-100%) translateZ(0)",transform:"translateY(-100%) translateZ(0)"},HIDE:{opacity:"0","-webkit-transform":"translateY(150%) translateZ(0)",transform:"translateY(150%) translateZ(0)"}},a={style:{main:{background:"rgba(0, 0, 0, .85)","box-shadow":"0 0 10px rgba(0, 0, 0, .8)","border-radius":"3px","z-index":"99999",color:"rgba(255, 255, 255, .9)","font-family":"sans-serif",padding:"10px 15px","max-width":"60%",width:"100%","word-break":"keep-all",margin:"0 auto","text-align":"center",position:"fixed",left:"0",right:"0",bottom:"0","-webkit-transform":"translateY(150%) translateZ(0)",transform:"translateY(150%) translateZ(0)","-webkit-filter":"blur(0)",opacity:"0"}},settings:{duration:4e3}},o=[];function s(t,s,c){var l=c||i;if(void 0!==f())o.push({text:t,options:s,transitions:l});else{var m=s||{};(function(t,n,i){!function(t,n){var e=document.createElement("div");"string"==typeof t&&(t=document.createTextNode(t));e.appendChild(t),d(e),r(f(),n)}(t,n.style.main);var a=f();document.body.insertBefore(a,document.body.firstChild),a.offsetHeight,r(a,i.SHOW),clearTimeout(e),0!==n.settings.duration&&(e=setTimeout((function(){return u(i)}),n.settings.duration))})(t,m=n(a,m),l)}return{hide:function(){return u(l)}}}function u(t){var n=f();r(n,t.HIDE),clearTimeout(e),n.addEventListener("transitionend",c,{once:!0})}function c(){var t=f();if(document.body.removeChild(t),d(void 0),o.length>0){var n=o.shift();s(n.text,n.options,n.transitions)}}function f(){return t}function d(n){t=n}return{toast:s}}();t.mergeOptions=n,t.stylize=r,t.toast=e}(this.iqwerty=this.iqwerty||{});
