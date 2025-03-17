
function send_email_on_server(arraydata){
    let url = document.object_urls.send_email //.replace('0', data.id);
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ items: arraydata })
    })
    .then(response => response.json())
    .then(data => {
        if(data.result){
            Swal.fire({
                title: gettext("Email Sent"),
                icon: "success"
            });
        }else{
            Swal.fire({
                title: gettext("Error sending email"),
                icon: "error"
            })
            }
    })
    .catch(error => {Swal.fire({
        title: gettext("Error sending email"),
        icon: "error"
    });} );
}



datatable_inits = {
    columns: [
        {data: "id", name: "id", title: gettext("Id"), type: "string", visible: false},
        {data: "subject", name: "subject", title: gettext("Subject"), type: "string", visible: true},
        {data: "create_datetime", name: "create_datetime", title: gettext("Create time"), type: "date",  render: DataTable.render.datetime(),
        "dateformat":  document.datetime_format, visible: true},
        {data: "enqueued", name: "enqueued", title: gettext("Enqueued"), type: "boolean", render: yesnoprint, visible: true},
        {data: "sent", name: "sent", title: gettext("Sent"), type: "boolean", render: yesnoprint, visible: true},
        {data: "problems", name: "problems", title: gettext("Problems"), type: "boolean", render: yesnoprint, visible: true},
        {data: "actions", name: "actions", title: gettext("Actions"), type: "string", visible: true }
    ],
    events: {
        filter: function(data){
            return data;
        }
    },
    addfilter: true
}

var obj_modalids = {
    create: "#create_obj_modal",
    update: "#update_obj_modal",
    detail: "#detail_obj_modal",
    destroy: "#delete_obj_modal",
}
var obj_actions = {
table_actions: [{
    action: (e, dt, node, config) => { send_email_on_server( get_selected_items(dt, dt.context[0].nTable)); },
    text:  '<i class="fa fa-eye" aria-hidden="true"></i>',
    titleAttr: gettext('Apply selected action'),
    className: "btn btn-success"
                                                    }],  //table_actions
object_actions: [  {
    'name': "sendemail",
    'action': 'sendemail',
    'title': gettext('Send Email'),
    'url': null,
    'i_class': 'fa fa-envelope-o',
}],  // object_actions
title: gettext('Actions'),
className:  "no-export-col"
}

let objconfig={
    urls: document.object_urls,
    datatable_element:  "#object_table",
    modal_ids: obj_modalids,
    actions: obj_actions,
    datatable_inits: datatable_inits,
    add_filter: true,
    checkable: true,
    relation_render: { },
    delete_display: data => data['subject']
}

let ocrud=ObjectCRUD("emailnotification", objconfig)
ocrud.init();
ocrud.sendemail=function(data){
    send_email_on_server([data.id]);
}
