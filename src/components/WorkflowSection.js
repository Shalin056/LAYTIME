// C:\Users\shali\Documents\shalin\test-app\src\components\WorkflowSection.js

import React, { Component } from "react";
import "swfrontend/WORKFLOW/WorkflowSection.css";
import { Badge, Button, Descriptions, Divider, Dropdown, Form, Input, Menu, Modal, Select } from "antd";
import Icon from "@ant-design/icons";
import { get_approval_hierarchy, get_approval_transactions, } from "swfrontend/COMS/Utils/ApiCommunicaton";
import { openNotification } from "swfrontend/COMS/NotificationMessageMapping";
import { notificationMessage, notificationTitle, openNotificationType, } from "swfrontend/MDM/MDMUIConfigs/MDMUIMappings";
import moment from "moment";
import StepsWorkflow from "./StepsWorkflow";
import LoadingIndicator from 'swfrontend/COMS/LoadingIndicator/LoadingIndicator';

const { TextArea } = Input;
const { Option } = Select;

class WorkflowSection extends Component {
    form = React.createRef();

    state = {
        steps: [],
        transactions: [],
        current_step: 0,
        apiCalled: false,
        // approval_type:[{'id':1,'name':'IT Asset'},{'id':2,'name':'SAP Login'}],
        selected_approval_type: null,
        modalVisibility: false,
        requestAction: 'Approve',
        isLoading: true
    };

    getTransactions = (appName, modelName, requestNo) => {
        try {
            get_approval_transactions(appName, modelName, requestNo).then((res) => {
                if (res.ok) {
                    res.json().then((response) => {
                     
                        this.setState({ transactions: response }, () => {
                            this.get_approval_hierarchy()
                        });
                    });
                } else {
                    openNotification(
                        openNotificationType.error,
                        notificationTitle.api,
                        notificationMessage.apiConnectionError
                    );
                }
            });
        } catch (error) {
            console.log('Error in getTransactions:', error);
        }
    };

    get_approval_hierarchy = () => {
        try {
            get_approval_hierarchy(
                this.props.app,
                this.props.model,
                this.props.request_no
            ).then((res) => {
                if (res.ok) {
                    res.json().then((response) => {

                        if (this.props.status.includes("Rejected")) {
                            this.setState({ current_step: this.state.transactions.length - 1 });
                        } else if (this.props.approval_status === "Approved") {
                            this.setState({ current_step: response.length });
                        } else {
                            this.setState({ current_step: this.state.transactions.length - 1 });
                        }

                        this.setState({
                            isLoading: false,
                            steps: response,
                            selected_approval_type: [this.props.approval_type[0]]
                        }, () => {
                            this.form.current.setFieldsValue({ 'approval_type': this.props.approval_type[0] });
                        });
                    });
                } else {
                    openNotification(
                        openNotificationType.error,
                        notificationTitle.api,
                        notificationMessage.apiConnectionError
                    );
                }
            });
        } catch (error) {

        }
    };

    getStepsData = () => {
        this.getTransactions(
            this.props.app,
            this.props.model,
            this.props.request_no
        );

    };

    updateWorkflow = () => {

        this.setState({ modalVisibility: false });

        if (this.state.selected_approval_type.length === 0) {
            openNotification(
                openNotificationType.error,
                notificationTitle.form,
                notificationMessage.approval_type
            );
            return
        }

        this.props.updateWorkflow({
            action: this.state.requestAction,
            app_name: this.props.app,
            model_name: this.props.model,
            id: this.props.request_no,
            remarks: this.form.current.getFieldValue("remarks"),
            approval_type: this.state.selected_approval_type
        })
    };

    render() {
        const { transactions } = this.state;
        let isRejected = false;

        if (transactions.length > 0 && transactions[transactions.length - 1].action.includes('Reject')) {
            isRejected = true;
        }

        if (this.props.request_no && !this.state.apiCalled) {
            this.getStepsData();
            this.setState({ apiCalled: true });
        }

        const workflow = (
            <Menu>
                <Menu.Item
                    className="Approve"
                    key="1"
                    hidden={this.props.hasOwnProperty("hideApproveOption") ? this.props.hideApproveOption : false}
                    onClick={() => {
                        if (
                            this.props.isRemarksRequired &&
                            (this.form.current.getFieldValue("remarks") === "" ||
                                this.form.current.getFieldValue("remarks") === undefined)
                        ) {
                            openNotification(
                                openNotificationType.error,
                                notificationTitle.form,
                                notificationMessage.remarks
                            );
                            return;
                        }
                        this.setState({ modalVisibility: true, requestAction: 'Approve' })
                    }}
                >
                    Approve
                </Menu.Item>
                <Menu.Item
                    className="Reject"
                    key="2"
                    hidden={this.props.hasOwnProperty("hideRejectOption") ? this.props.hideRejectOption : false}
                    onClick={() => {
                        if (
                            this.props.isRemarksRequired &&
                            (this.form.current.getFieldValue("remarks") === "" ||
                                this.form.current.getFieldValue("remarks") === undefined)
                        ) {
                            openNotification(
                                openNotificationType.error,
                                notificationTitle.form,
                                notificationMessage.remarks
                            );
                            return;
                        }
                        this.setState({ modalVisibility: true, requestAction: 'Reject' })
                    }}
                >
                    Reject
                </Menu.Item>
            </Menu>
        );

        return (
            this.state.steps.length > 0 ?
                <div className="workflow_section">
                    <legend className="form-legend">{this.props.isChangeRequest && "Change Request "}Approval Workflow</legend>
                    <div className="workflow_section_inside">
                        {this.state.isLoading && <LoadingIndicator />}
                        <div className="workflow_menu">

                            <Descriptions.Item
                                label="Status"
                                span={3}
                                className="workflow_menu_status"
                            >
                                <Badge
                                    color={isRejected ? 'red' : 'green'}
                                    status={
                                        this.props.approval_status === "Approved"
                                            ? "success"
                                            : isRejected
                                                ? "error"
                                                : "processing"
                                    }
                                    text={
                                        isRejected
                                            ? "Rejected"
                                            : this.props.approval_status
                                    }
                                    className="workflow_menu_status"
                                />
                            </Descriptions.Item>

                            &nbsp;&nbsp;
                            <div
                                style={{ display: "inline-block" }}
                                hidden={
                                    this.props.hideApprovalAction ||
                                    this.props.approval_status === "Approved"
                                }
                            >
                                <Dropdown
                                    trigger={["click"]}
                                    className="workflow_menu_button"
                                    overlay={workflow}
                                >
                                    <Button className="workflow_menu_button">
                                        Approve / Reject
                                        <Icon
                                            type="down"
                                            style={{ fontSize: "10px", color: "#000" }}
                                        />
                                    </Button>
                                </Dropdown>
                            </div>
                        </div>

                        <Divider style={{borderTop: "2px solid #DF9C07"}}/>
                        <Form ref={this.form} layout={"vertical"}>
                            <div className="row">
                                <div className="col-md-6">
                                    <Form.Item label={"Request no"}>
                                        <Input
                                            placeholder="Request No."
                                            value={this.props.request_no}
                                            disabled
                                        />
                                    </Form.Item>
                                </div>
                                <div className="col-md-6">
                                    <Form.Item label={"Request category"}>
                                        <Input
                                            placeholder="Request category"
                                            value={this.props.request_category}
                                            disabled
                                        />
                                    </Form.Item>
                                </div>
                            </div>
                            <div className="row">
                                <div className="col-md-6">
                                    <Form.Item label={"Request date"}>
                                        <Input
                                            placeholder="Request date"
                                            value={moment(
                                                this.props.request_date,
                                                "YYYY-MM-DD HH:mm:ss"
                                            ).format("YYYY-MM-DD HH:mm:ss")}
                                            disabled
                                        />
                                    </Form.Item>
                                </div>

                                {this.props.approval_type !== undefined && (
                                    <div className="col-md-6">
                                        <Form.Item
                                            name={"approval_type"}
                                            rules={[
                                                {
                                                    required: true,
                                                    message: "Please select approval",
                                                },
                                            ]}
                                            validateTrigger="onBlur"
                                            label={"Approval Group"}
                                        >
                                            <Select
                                                disabled={
                                                    isRejected ? true :
                                                        this.props.approval_type.length === 0 ? true :
                                                            this.props.approval_type.length === 1 && true
                                                }

                                                mode={this.props.approval_type.length > 1 && 'multiple'}

                                                onChange={(e) => this.setState({ selected_approval_type: e })}>
                                                {this.props.approval_type.map((each_type) => (
                                                    <Option value={each_type}>{each_type}</Option>
                                                ))}
                                            </Select>
                                        </Form.Item>
                                    </div>
                                )}

                                <div className="col-md-6">
                                    <Form.Item
                                        name={"remarks"}
                                        rules={[
                                            {
                                                required: this.props.isRemarksRequired,
                                                message: "Please enter remarks",
                                            },
                                        ]}
                                        validateTrigger="onBlur"
                                        label={"Approver's Remarks"}
                                    >
                                        <TextArea
                                            placeholder="Enter remarks"
                                            disabled={
                                                this.props.hideApprovalAction ||
                                                this.props.approval_status === "Approved"
                                            }
                                        />
                                    </Form.Item>
                                </div>
                            </div>
                        </Form>
                        {this.props.children}
                        <Divider style={{borderTop: "2px solid #DF9C07"}}/>
                        <strong className={"ApprovalText"}> Approval Hierarchy</strong>

                        {/* Confirmatiion model */}
                        <Modal
                            title="Confirm"
                            visible={this.state.modalVisibility}
                            onCancel={() => this.setState({ modalVisibility: false })}
                            footer={[
                                <Button
                                    key="submit"
                                    type="primary"
                                    onClick={this.updateWorkflow}>
                                    OK
                                </Button>,
                            ]}
                        >
                            Are you sure you want to <b>{this.state.requestAction}</b> this request ?
                        </Modal>

                        <StepsWorkflow
                            status={this.props.status}
                            heirarchy={this.state.steps}
                            transactions={this.state.transactions} />
                    </div>

                </div>
                :
                <LoadingIndicator />
        );
    }
}

export default WorkflowSection;
