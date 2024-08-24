// C:\Users\shali\Documents\shalin\test-app\src\components\StepsWorkflow.js

import React, {Component} from "react";
import {Button, Form, Popover, Steps, Tabs} from "antd";
import * as moment from "moment";
import "swfrontend/WORKFLOW/WorkflowSection.css";

const {Step} = Steps;
const {TabPane} = Tabs;

class StepsWorkflow extends Component {
    state = {
        heirarchy: this.props.heirarchy,
        transactions: this.props.transactions,
        moreInfo: false,
        moreInfoIndex: 0,
    };

    toggleMoreInfo = (moreInfoIndex) => {
        this.setState({moreInfoIndex, moreInfo: true});
    };

    getCurrentStep = () => {

        let status = this.props.status;

        //Executes only if workflow is rejected
        if (this.props.status !== null && this.props.status.includes("Rejected")) {
            let current_state = this.props.transactions.filter((t) =>
                t.action.includes("Reject")
            );

            status = current_state[0].current_state;
        }

        let currentStep = 0;
        switch (this.props.status) {
            case "Initiated":
                return currentStep;

            case "Approved":
                return this.props.heirarchy.length;

            case "Final Clearance":
                return this.props.heirarchy.length - 1;

            default:
                this.props.heirarchy.forEach((h, index) => {
                    if (h.current_state.includes(status)) {
                        currentStep = index;
                    }
                });
        }

        return currentStep;
    };

    getApprovalDetailsByGroup = (group, currentState) => {
        let details = [];

        //If group is Initiated
        if (group === "Initiated") {
            details.push(this.props.transactions[0]);
        } else {
            //If group is not Initiated
            details = this.props.transactions.filter(
                (t) =>
                t.approver.substring(2,t.approver.length-2) === group && t.current_state.includes(currentState)
            );
        }

        if (details.length === 0) return [{approver: undefined}];

        return details;
    };

    getGroupDetails = (moreInfoIndex) => {
        if (moreInfoIndex === 0) {
            return ["Initiated"];
        }

        let groupDetail = [];

        if (moreInfoIndex <= this.props.heirarchy.length - 1) {
            return this.props.heirarchy[moreInfoIndex].action_group;
        }

        return groupDetail;
    };

    isRejectedOnCurrentStage = (stage) => {
        let isRejected = this.props.transactions.filter(
            (t) => t.action==="Reject" && t.current_state===stage)

        if (isRejected.length > 0) return true;
    };

    render() {
        const {moreInfo, moreInfoIndex} = this.state;
        const {heirarchy, transactions} = this.props;
        const currentStep = this.getCurrentStep();
        console.log(this.props.status, this.props.heirarchy, this.props.transactions);
        return (
            <>
                <br/>
                <br/>

                {/* PARENT STEPS */}
                <div>
                    <Steps progressDot size="small" current={currentStep}>
                        {/* TO GENERATE DYNAMIC STEPS FROM HEIRARCHY */}
                        {heirarchy.map((each_heirarchy, index) => (
                            <Step
                                status={
                                    this.isRejectedOnCurrentStage(each_heirarchy.current_state) &&
                                    "error"
                                }
                                title={
                                    <Popover
                                        placement="top"
                                        content={<p>Click to see more info</p>}
                                        trigger="hover"
                                    >
                                        <p>{each_heirarchy.current_state}</p>
                                        <p style={{fontSize: 10}}>Click for more info</p>
                                    </Popover>
                                }
                                onClick={(i) => this.toggleMoreInfo(index)}
                            />
                        ))}

                        {/* TO GENERATE APPROVED STEP */}
                        {[heirarchy[heirarchy.length - 1]].map((each_heirarchy) => (
                            <Step title={each_heirarchy.next_state}/>
                        ))}
                    </Steps>

                    {/* TOGGLE MORE INFO SECTION */}
                    {moreInfo && (
                        <>
                            {/* CURRENTLY ACTIVE TOGGLED STEP TITLE */}
                            <p className="heirarchy-title">
                                {heirarchy[moreInfoIndex].current_state}
                            </p>
                            <hr/>

                            {/* PARENT TABS */}
                            <Tabs tabPosition="left">
                                {/* EACH GROUP TRANSACTION DETAIL */}
                                {this.getGroupDetails(moreInfoIndex).map(
                                    (each_group, index) => (
                                        // CHILD TABS
                                        <TabPane
                                            tab={moreInfoIndex === 0 ? "Initiated" : each_group}
                                            key={index}
                                        >
                                            {/* APPROVAL DETAILS BASED ON GROUP NAME */}
                                            {this.getApprovalDetailsByGroup(
                                                moreInfoIndex === 0 ? "Initiated" : each_group,
                                                heirarchy[moreInfoIndex].current_state
                                            ).map((each_transaction) =>
                                                // IF UNDEFINED THEN CONSIDER NO TRANSACTION INFO AVAILABLE
                                                each_transaction.approver === undefined ? (
                                                    <div> Pending for approval. </div>
                                                ) : (
                                                    <Form className="row" layout="vertical">
                                                        <div className="col-md-3">
                                                            <Form.Item label="Action">
                                                                <p
                                                                    className={
                                                                        each_transaction.action.includes(
                                                                            "Reject"
                                                                        ) && "text-danger"
                                                                    }
                                                                >
                                                                    {moreInfoIndex === 0
                                                                        ? transactions[0].action
                                                                        : each_transaction.action}
                                                                </p>
                                                            </Form.Item>

                                                            <Form.Item label="Approver">
                                                                <p
                                                                    className={
                                                                        each_transaction.action.includes(
                                                                            "Reject"
                                                                        ) && "text-danger"
                                                                    }
                                                                >
                                                                    {moreInfoIndex === 0
                                                                        ? transactions[0].approver
                                                                            .substring(
                                                                                transactions[0].approver.indexOf("'"),
                                                                                transactions[0].approver.indexOf("]")
                                                                            )
                                                                            .replace(/'/g, "")
                                                                        : each_transaction.approver
                                                                            .substring(
                                                                                each_transaction.approver.indexOf(
                                                                                    "'"
                                                                                ),
                                                                                each_transaction.approver.indexOf("]")
                                                                            )
                                                                            .replace(/'/g, "")}
                                                                </p>
                                                            </Form.Item>
                                                        </div>

                                                        <div className="col-md-3">
                                                            <Form.Item label="User">
                                                                <p
                                                                    className={
                                                                        each_transaction.action.includes(
                                                                            "Reject"
                                                                        ) && "text-danger"
                                                                    }
                                                                >
                                                                    {moreInfoIndex === 0
                                                                        ? transactions[0].approver_user_if_group
                                                                        : each_transaction.approver_user_if_group}
                                                                </p>
                                                            </Form.Item>

                                                            <Form.Item label="Created Date">
                                                                <p
                                                                    className={
                                                                        each_transaction.action.includes(
                                                                            "Reject"
                                                                        ) && "text-danger"
                                                                    }
                                                                >
                                                                    {moment(
                                                                        moreInfoIndex === 0
                                                                            ? transactions[0].created_date
                                                                            : each_transaction.created_date
                                                                    ).format("YYYY-MM-DD THH:mm")}
                                                                </p>
                                                            </Form.Item>
                                                        </div>

                                                        <div className="col-md-3">
                                                            <Form.Item label="Remarks">
                                                                <p
                                                                    className={
                                                                        each_transaction.action.includes(
                                                                            "Reject"
                                                                        ) && "text-danger"
                                                                    }
                                                                >
                                                                    {moreInfoIndex === 0
                                                                        ? transactions[0].remarks
                                                                        : each_transaction.remarks}
                                                                </p>
                                                            </Form.Item>
                                                        </div>

                                                        <div className="col-md-12">
                                                            <hr/>
                                                        </div>
                                                    </Form>
                                                )
                                            )}
                                        </TabPane>
                                    )
                                )}
                            </Tabs>

                            <hr/>
                            <div class="text-center">
                                <Button
                                    className="workflow_menu_button"
                                    type="ghost"
                                    onClick={() => this.setState({moreInfo: false})}
                                >
                                    Close
                                </Button>
                            </div>
                        </>
                    )}
                </div>
            </>
        );
    }
}

export default StepsWorkflow;
