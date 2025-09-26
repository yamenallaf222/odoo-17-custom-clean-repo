/* @odoo-module */


import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class ListViewAction extends Component {
    static template = "app_one.ListView";

    // this is more of a constructor with no args
    setup() {
        this.state = useState({
            'records': []
        });
        this.orm = useService("orm");
        this.loadRecords();
    };

    async loadRecords() {
        const result = await this.orm.searchRead("property", [], []);
        console.log(result);
        this.state.records = result;
    };
}

registry.category("actions").add("app_one.action_list_view", ListViewAction);