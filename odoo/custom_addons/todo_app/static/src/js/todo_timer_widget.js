/** @odoo-module **/

//
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";
import {useState, onWillStart, onWillDestroy, onMounted, Component} from "@odoo/owl";
import { standardFieldProps } from "@web/views/fields/standard_field_props";


export class TodoTimerWidget extends Component {

    static template = "todo_app.TodoTimerWidget";
    static props = standardFieldProps;


    setup() {
        
        this.notification = useService("notification");
        this.orm = useService("orm");
        this.state = useState({
            start_time: null,
            stop_time: null,
            elapsed: 0,
            running: false
        });

        this.timerId = null;

        onWillStart(this.onWillStart.bind(this));
        onWillDestroy(this.onWillDestroy.bind(this));
        onMounted(this.onMounted.bind(this));

    }

    async onWillStart() {

        /**
         *  @todo REFRESHER there is a freaking mess here, last thing i were doing was pitching from the orm call to fetch data to using 
         * props var to finding that it lazy loads and does not contain all needed data to find out i need some kind field addition
         * to the xml field fo the widget to find the mess of the hierarchy of props accessing
         */
        debugger;

        let timer = null;

        {
            // filter returns an empty array BUT FIND returns undefined
            const timers = this.props.record.data.timer_ids.records.filter(r => r.data.todo_task_id[0] === this.props.record.resId)?.[0]; // the resId is the current todo_task_id ( the model record of the form view we re in)

            if (timers.length === 0) {

                const timerCreation = await this.orm.create('todo.timer', [{

                    todo_task_id: this.props.record.resId, // parent_id
                    elapsed: 0,

                }]);

                this.timerId = timerCreation?.[0];

                if( this.timerId !== 0 && !this.timerId ) {

                    //USER-FRIENDLY error
                    this.notification.add("The timer of this task could not be fetched. Please contact your system's administrator", {
                        title: "Validation Error",
                        type: "danger",
                        sticky: "false"
                    });

                    //developer debug log
                    console.log("timerId is invalid with value:", this.timerId);

                    // halt exec
                    return;

                }

                const timerRecord = await this.orm.read('todo.timer',
                    [this.timerId],
                    ['start_time', 'stop_time', 'elapsed', 'is_running']
                )

                this.state.start_time = timerRecord.start_time;
                this.state.stop_time = timerRecord.stop_time;
                this.state.elapsed = timerRecord.elapsed;
                this.state.running = timerRecord.is_running;

            } else {

                console.log(timers);

                this.timerId = timers.data.id;

                if (!this.timerId) {
            
                    //USER-FRIENDLY error
                    this.notification.add("The timer of this task could not be fetched. Please contact your system's administrator", {
                        title: "Validation Error",
                        type: "danger",
                        sticky: "false"
                    });

                    //developer debug log
                    console.log("timerId is invalid with value:", this.timerId);

                    // halt exec
                    return;
                }
                
                this.state.elapsed = timers.data.elapsed;
                this.state.start_time = timers.data.start_time || "Never";
                this.state.stop_time = timers.data.stop_time || "Never";
                this.state.running = timers.data.is_running;
                

            }
        }


        // if(timers.length === 0) {

        //     console.log("Timers searched for:    ", timers);
        //     const timer = await this.orm.read('todo.timer', timers);

        //     this.state.elapsed = timer.elapsed;
        //     this.state.stop_time = timer.stop_time;
        //     this.state.start_time = timer.start_time;
        //     this.state.running = timer.is_running;
        //     console.log("\n\n\n\n\n\n\n\n\n\n");

        //     console.log(timer);

        // }

            
        // this.state.running = timer[0]?.is_running;
        // this.state.elapsed = timer[0]?.elapsed;

    }

    onMounted() {

        this.pollingInterval = setInterval(async () => {
            if (this.state.running) {
                
                try {
                    const res = await this.orm.call(
                        "todo.timer", 
                        "update_live_elapsed", 
                        [[this.timerId]]
                    );
                    this.state.elapsed = res[0]?.elapsed;

                }

                catch (e) {
                    console.error("Polling failed:", e);
                }
            }
        }, 950);  // ~1 second

    }

    onWillDestroy() {
debugger;
        if(this.pollingInterval){

            clearInterval(this.pollingInterval);
        }

    }

    async startTimer() {

        try {

            const res = await this.orm.call(
                "todo.timer", 
                "action_start_timer", 
                [],
                {
                    record_ids: [this.timerId]
                }
            );


            this.state.running = res[0].is_running;
            this.state.start_time = res[0].start_time;

        }

        catch (error){

            console.error("Timer failed: ", error.message);
            // no need to display a pop-up as Odoo validation exception already displays it 
        }
        
    }

    async stopTimer() {

        try {

            const res = await this.orm.call(
                "todo.timer", 
                "action_stop_timer", 
                [],
                {
                    record_ids: [this.timerId]
                }
            );
            this.state.running = res[0].is_running;
            this.state.stop_time = res[0].stop_time;

        }

        catch (error){

            console.error("Timer failed: ", error.message);
            // no need to display a pop-up as Odoo validation exception already displays it 

        }

    }
}


//register the widget so it can be used in the field tag to fill the *widget* att
registry.category("fields").add("todo_timer_widget", {
    component: TodoTimerWidget,
    
    /**
     * odoo needs the field type when it relational to be able to run the this js class with
     * the associated field
     */
    supportedTypes: ["one2many"],
});
