
datatable_inits = {
    columns: [
        {data: "id", name: "id", title: gettext("Id"), type: "string", visible: false},
        {data: "code", name: "code", title: gettext("Code"), type: "string", visible: true},
        {data: "subject", name: "subject", title: gettext("Subject"), type: "string", visible: true},
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
table_actions: [],  //table_actions
object_actions: [  {
    'name': "preview",
    'action': 'preview',
    'title': gettext('Preview'),
    'url': null,
    'i_class': 'fa fa-eye',
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

let ocrud=ObjectCRUD("emailtemplate", objconfig)
ocrud.init();
ocrud.preview=function(data){

}
