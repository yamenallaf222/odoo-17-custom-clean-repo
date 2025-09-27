/* @odoo-module */


import { Component, useState, onWillUnmount } from "@odoo/owl";
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
        this.rpc = useService("rpc");
        this.loadRecords();

        this.loadRecordsIntervalId = setInterval(() => {this.loadRecords()}, 3000);
        
        onWillUnmount(() => {clearInterval(this.loadRecordsIntervalId)});
    };

    // async loadRecords() {
    //     const result = await this.orm.searchRead("property", [], []);
    //     console.log(result);
    //     this.state.records = result;
    // };

    async loadRecords() {
        const result = await this.rpc("/web/dataset/call_kw", {
            model: "property",
            method: "search_read",
            args: [[]],
            kwargs: {fields: ['id', 'name', 'postcode', 'date_availability']}
        });
        console.log(result);
        this.state.records = result;
    }

    async createRecord() {
        await this.rpc("/web/dataset/call_kw/", {
            model: "property",
            method: "create",
            args:[{
                name: "new property",
                postcode: "1423232",
                date_availability: "2024-04-24"
            }],
            kwargs: {}
        });
        this.loadRecords();
    }

    async deleteRecord(recordId) {
        await this.rpc("/web/dataset/call_kw/", {
            model: "property",
            method: "unlink",
            args:[recordId],
            kwargs: {}
        });
        this.loadRecords();
    }
}

registry.category("actions").add("app_one.action_list_view", ListViewAction);