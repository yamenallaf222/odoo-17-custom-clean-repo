/* @odoo-module */


import { Component, useState, onWillUnmount } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class FormView extends Component {
    static template = "app_one.FormView";

    setup() {
        this.state = useState({
            name: "",
            postcode: "",
            date_availability: ""
        });

        this.rpc = useService("rpc");
    };

    async createRecord() {
        await this.rpc("/web/dataset/call_kw", {
            model: "property",
            method: "create",
            args: [{
                name: this.state.name,
                postcode: this.state.postcode,
                date_availability: this.state.date_availability,
            }],
            kwargs: {}
        });
        this.props.onRecordCreated();
    };

    cancel() {
        this.state.name = "";
        this.state.postcode = "";
        this.state.date_availability = "";
        this.props.onCancel();
    }
};