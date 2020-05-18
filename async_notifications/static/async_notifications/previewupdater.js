(function($){
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    function setCookie(cname, cvalue, exdays) {
      var d = new Date();
      d.setTime(d.getTime() + (exdays*24*60*60*1000));
      var expires = "expires="+ d.toUTCString();
      document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
    }

    function copyToClipboard(element) {
      var $temp = $("<input>");
      $("body").append($temp);
      $temp.val(element).select();
      document.execCommand("copy");
      $temp.remove();
    }

    function get_update_url(value){
        var data = $("#id_templatecontext").data('url');
        var ldata = data.split("/");
        ldata.pop();
        data = ldata.join("/");
        return data+"/"+value;
    }

    function update_context(value){
        var url = get_update_url(value);
        $.ajax({
            dataType: "json",
              url: url,
              type: "GET",
              data: {},
              success: function(data){
                var result = data['results'];
                $("#id_templatecontext").val(null).trigger('change');
                for( var x=0; x<result.length; x++){
                    var newOption = new Option(result[x].text, result[x].id, false, false);
                    $("#id_templatecontext").append(newOption);
                }
                $("#id_templatecontext").trigger('change');
              }
        });
    }


    function update_form_context(value){
        $(".loading").show();
        var url = get_update_url(value)+"/form";
        $.ajax({
              dataType: "json",
              url: url,
              type: "POST",
              headers: {'X-CSRFToken': csrftoken },
              data: {'recipient': $('#id_recipient').val()},
              success: function(data){
                $(".loading").hide();
                $(".datafilter").html(data['form']);
                $(".datafilter").find('select').select2({ width: '90%'});
              }
              });

    }

    function clean_filter_emails(){
        $(".limemfil").on('click', function(){
            $("#id_excludeemail").val("");
            $(".emailhide").removeClass('emailhide');
        });

    }

    function exclude_email_account(){
        $(".emailexc").on('click', function(){
            var data = $("#id_excludeemail").val().split(",");
            $(this).parent().addClass('emailhide');
            data.push($(this).data('text'));
            $("#id_excludeemail").val(data.join(","));
        });

    }

    function show_email_preview(){
        var value=$('select[name="template"]').find(":selected").val();
        var url = get_update_url(value)+"/preview";
        $.ajax({
              dataType: "json",
              url: url,
              type: "POST",
              headers: {'X-CSRFToken': csrftoken },
              data: {'recipient': $(".datafilter").find(':input').serialize()},
              success: function(data){

                    var html = '<p>Clic en <span class="emailexcinf">x</span> par excluir dirección de correo o <span class="limemfil">limpe filtros</span></p>';

                     html += '<ul class="emaillu">';
                    for (var x=0; x<data['emails'].length; x++){
                        html += '<li><span class="emailexc" data-text="'+data['emails'][x]+'">x</span> '+data['emails'][x]+'</li>';
                    }
                    html += '</ul>';

                    Swal.fire({
                      title: 'Detalle de correo ('+data['emails'].length+')',
                      html: html,
                      showCloseButton: true,
                      showCancelButton: true,
                      focusConfirm: false,
                      width: 950,
                    })
                    exclude_email_account();
                    clean_filter_emails();
              }
              });
    }


    $(document).ready(function(){
        $('select[name="template"]').select2();
        $('select[name="templatecontext"]').select2();


        $('select[name="templatecontext"]').change(function(){
            var value=$(this).find(":selected").val();
            copyToClipboard("{{"+value+"}}");
        });

        $('select[name="template"]').change(function(){
            var value=$(this).find(":selected").val();
            if(value == ""){
                value="0";
            }
            setCookie("template", value, 1);
            update_context(value);
            update_form_context(value);
        });
        var maxwidth=$("#content").width()-10;
        $("#id_message").css({'width': maxwidth });
        $('<style> .markItUp { width:'+maxwidth+'px; }</style>').appendTo( "head" );

        $('button[name="filterrecipient"]').on('click', function(){
        $('#id_recipient').val($(".datafilter").find(':input').serialize());
        toastr.success("Recuerde que hasta guardar el formulario se almacenarán los filtros",'Filtros creados',
            {"positionClass": "toast-top-center", "preventDuplicates": false})
        });
        $('button[name="showemails"]').on('click', function(){show_email_preview();  });


    });


})(django.jQuery);
