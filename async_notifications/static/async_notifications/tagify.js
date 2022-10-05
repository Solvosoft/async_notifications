(function(){
   document.addEventListener("DOMContentLoaded", function(event) {
    var inputs = document.querySelectorAll("input[data-widget=TagifySelect]");
    inputs.forEach(function(e,i ){
       var url = e.dataset['url'];

       var tagify = new Tagify(e, {whitelist:[],
        pattern: /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})*$/,
         dropdown: {
            searchKeys: ["value", "name"] //  fuzzy-search matching for those whitelist items' properties
         }
       }),
        controller;

        tagify.on('input', onInput)

        function onInput( e ){
            var value = e.detail.value
          tagify.whitelist = null // reset the whitelist
          // https://developer.mozilla.org/en-US/docs/Web/API/AbortController/abort
          controller && controller.abort()
          controller = new AbortController()
          // show loading animation and hide the suggestions dropdown
          tagify.loading(true).dropdown.hide()
          fetch(url+'?value=' + value, {signal:controller.signal})
            .then(RES => RES.json())
            .then(function(newWhitelist){
              tagify.whitelist = newWhitelist // update whitelist Array in-place
              tagify.loading(false).dropdown.show(value) // render the suggestions dropdown
            })
        }

    })
    })
})();