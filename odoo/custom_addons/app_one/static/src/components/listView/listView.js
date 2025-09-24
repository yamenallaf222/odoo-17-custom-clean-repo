/* @odoo-module */


import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class ListViewAction extends Component {
    static template = "app_one.ListView";
}

registry.category("actions").add("app_one.action_list_view", ListViewAction);