// C:\Users\shali\Documents\shalin\test-app\src\components\FormHeader.js

import React, { Component } from 'react';
import { Button, Dropdown, Space, Form, Menu, Popconfirm } from 'antd';
import { DownloadOutlined, FileExcelOutlined } from "@ant-design/icons";

class FormHeader extends Component {

    state = {
        status: "",
        hideAction: true,
        isSaveClicked: false,
        isApprovalClicked: false,
    };

    handleSave = () => {
        this.setState({ isSaveClicked: true }, () => {
            this.props.formRef.current.submit();
        });
    };

    render() {
        // const { isSaveClicked } = this.state;
        const { rowData } = this.props;
        // const hideInitiateApprovalButton = rowData.status !== "Draft" && !isSaveClicked;
        const hideInitiateApprovalButton = rowData.status !== "Draft";
        // const menuItems = [
        //     {
        //         key: '1',
        //         label: (
        //             <React.Fragment>
        //             { hideInitiateApprovalButton ? null : (
        //             <Button
        //                 style={{
        //                     float: 'left',
        //                     display: 'block',
        //                     color: 'white',
        //                     backgroundColor: this.state.isApprovalHovered ? '#4CBB17' : 'green',
        //                     borderColor: '#4CBB17',
        //                     borderWidth: '1px',
        //                     borderStyle: 'solid',
        //                     borderRadius: '5px',
        //                     fontWeight: 'bold',
        //                     transition: 'background-color 0.3s, color 0.3s', // Smooth transition
        //                 }}
        //                 onMouseEnter={() => this.setState({ isApprovalHovered: true })}
        //                 onMouseLeave={() => this.setState({ isApprovaltHovered: false })}
        //                 type="primary"
        //                 onClick={() => this.props.initiateApproval()}
        //                 className="login-form-button"
        //             >
        //                 Initiate Approval
        //             </Button>
        //             )}
        //             </React.Fragment>
        //         ),
        //     },
        //     {
        //         key: '2',
        //         label: (
        //             <React.Fragment>
        //             {!this.props.isNewLaytimeCalculator && hideInitiateApprovalButton ? null : (
        //                 <Button
        //                     style={{
        //                         float: 'left',
        //                         display: 'block',
        //                         color: this.state.isSaveHovered ? 'white' : 'red',
        //                         backgroundColor: this.state.isSaveHovered ? 'red' : 'white',
        //                         borderColor: 'red',
        //                         borderWidth: '1px',
        //                         borderStyle: 'solid',
        //                         borderRadius: '5px',
        //                         fontWeight: 'bold',
        //                         transition: 'background-color 0.3s, color 0.3s', // Smooth transition
        //                     }}
        //                     onMouseEnter={() => this.setState({ isSaveHovered: true })}
        //                     onMouseLeave={() => this.setState({ isSaveHovered: false })}
        //                     type="primary"
        //                     // htmlType="submit"
        //                     className="login-form-button"
        //                     onClick={() => this.props.formRef.current.submit()}
        //                 >
        //                     Save
        //                 </Button>
        //             )}
        //             </React.Fragment>
        //         ),
        //     },
        //     {
        //         key: '3',
        //         label: (
        //             <React.Fragment>
        //             {!this.props.isNewLaytimeCalculator && (
        //             <Button
        //                 style={{
        //                     marginRight: '10px',
        //                     color: this.state.isDownloadPDFHovered ? 'white' : 'red',
        //                     backgroundColor: this.state.isDownloadPDFHovered ? 'red' : 'white',
        //                     borderColor: 'red',
        //                     borderWidth: '1px',
        //                     borderStyle: 'solid',
        //                     borderRadius: '5px',
        //                     fontWeight: 'bold',
        //                     transition: 'background-color 0.3s, color 0.3s', // Smooth transition
        //                 }}
        //                 type="primary"
        //                 shape="default"
        //                 onClick={() => this.props.onDownloadPDF()}
        //                 onMouseEnter={() => this.setState({ isDownloadPDFHovered: true })}
        //                 onMouseLeave={() => this.setState({ isDownloadPDFHovered: false })}
        //                 icon={<DownloadOutlined />}
        //             >
        //                 Download PDF
        //             </Button>
        //             )}
        //             </React.Fragment>
        //         ),
        //     },
        //     {
        //         key: '4',
        //         label: (
        //             <React.Fragment>
        //             {!this.props.isNewLaytimeCalculator && (
        //             <Button
        //                 style={{
        //                     marginRight: '10px',
        //                     color: this.state.isDownloadExcelHovered ? 'white' : 'red',
        //                     backgroundColor: this.state.isDownloadExcelHovered ? 'red' : 'white',
        //                     borderColor: 'red',
        //                     borderWidth: '1px',
        //                     borderStyle: 'solid',
        //                     borderRadius: '5px',
        //                     fontWeight: 'bold',
        //                     transition: 'background-color 0.3s, color 0.3s', // Smooth transition
        //                 }}
        //                 type="primary"
        //                 shape="default"
        //                 onClick={() => this.props.onDownloadExcel()}
        //                 onMouseEnter={() => this.setState({ isDownloadExcelHovered: true })}
        //                 onMouseLeave={() => this.setState({ isDownloadExcelHovered: false })}
        //                 icon={<FileExcelOutlined />}
        //             >
        //                 Download Excel
        //             </Button>
        //             )}
        //             </React.Fragment>
        //         ),
        //     },
        // ];

        const menuItems = (
            <Menu>
                <Menu.Item
                    key="1"
                    hidden={hideInitiateApprovalButton}
                >
                    <Popconfirm
                        title="Are you sure want to initiate approval for this request ?"
                        onConfirm={() => this.props.initiateApproval()}
                        okText="Yes"
                        cancelText="No"
                        placement="left"
                    >
                    <Button
                        style={{
                            float: 'left',
                            display: 'block',
                            color: 'white',
                            backgroundColor: this.state.isApprovalHovered ? '#4CBB17' : 'green',
                            borderColor: '#4CBB17',
                            borderWidth: '1px',
                            borderStyle: 'solid',
                            borderRadius: '5px',
                            fontWeight: 'bold',
                            transition: 'background-color 0.3s, color 0.3s', // Smooth transition
                        }}
                        onMouseEnter={() => this.setState({ isApprovalHovered: true })}
                        onMouseLeave={() => this.setState({ isApprovaltHovered: false })}
                        type="primary"
                        // onClick={() => this.props.initiateApproval()}
                        className="login-form-button"
                    >
                        Initiate Approval
                    </Button>
                    </Popconfirm>
                </Menu.Item>
                <Menu.Item
                    key="2"
                    hidden={!this.props.isNewLaytimeCalculator && hideInitiateApprovalButton}
                >
                    <Button
                        style={{
                            float: 'left',
                            display: 'block',
                            color: this.state.isSaveHovered ? 'white' : 'red',
                            backgroundColor: this.state.isSaveHovered ? 'red' : 'white',
                            borderColor: 'red',
                            borderWidth: '1px',
                            borderStyle: 'solid',
                            borderRadius: '5px',
                            fontWeight: 'bold',
                            transition: 'background-color 0.3s, color 0.3s', // Smooth transition
                        }}
                        onMouseEnter={() => this.setState({ isSaveHovered: true })}
                        onMouseLeave={() => this.setState({ isSaveHovered: false })}
                        type="primary"
                        // htmlType="submit"
                        className="login-form-button"
                        onClick={() => this.props.formRef.current.submit()}
                    >
                        Save
                    </Button>
                </Menu.Item>
                <Menu.Item
                    key="3"
                    hidden={this.props.isNewLaytimeCalculator}
                    // onClick={() => this.props.formRef.current.submit()}
                >
                    <Button
                        style={{
                            marginRight: '10px',
                            color: this.state.isDownloadPDFHovered ? 'white' : 'red',
                            backgroundColor: this.state.isDownloadPDFHovered ? 'red' : 'white',
                            borderColor: 'red',
                            borderWidth: '1px',
                            borderStyle: 'solid',
                            borderRadius: '5px',
                            fontWeight: 'bold',
                            transition: 'background-color 0.3s, color 0.3s', // Smooth transition
                        }}
                        type="primary"
                        shape="default"
                        onClick={() => this.props.onDownloadPDF()}
                        onMouseEnter={() => this.setState({ isDownloadPDFHovered: true })}
                        onMouseLeave={() => this.setState({ isDownloadPDFHovered: false })}
                        icon={<DownloadOutlined />}
                    >
                        Download PDF
                    </Button>
                </Menu.Item>
                <Menu.Item
                    key="4"
                    hidden={this.props.isNewLaytimeCalculator}
                >
                    <Button
                        style={{
                            marginRight: '10px',
                            color: this.state.isDownloadExcelHovered ? 'white' : 'red',
                            backgroundColor: this.state.isDownloadExcelHovered ? 'red' : 'white',
                            borderColor: 'red',
                            borderWidth: '1px',
                            borderStyle: 'solid',
                            borderRadius: '5px',
                            fontWeight: 'bold',
                            transition: 'background-color 0.3s, color 0.3s', // Smooth transition
                        }}
                        type="primary"
                        shape="default"
                        onClick={() => this.props.onDownloadExcel()}
                        onMouseEnter={() => this.setState({ isDownloadExcelHovered: true })}
                        onMouseLeave={() => this.setState({ isDownloadExcelHovered: false })}
                        icon={<FileExcelOutlined />}
                    >
                        Download Excel
                    </Button>
                </Menu.Item>

            </Menu>
        )
        
        return (
            <div className="form_header" style={{ position: 'sticky', top: 40, zIndex: 1000, background: 'white' }}>
                <Button
                    hidden={this.props.hasOwnProperty('showBackButton') ? !this.props.showBackButton : true}
                    onClick={() => this.props.onBackPressed()}
                    style={{
                        float: 'left',
                        display: 'block',
                        color: this.state.isBackHovered ? 'white' : 'red',
                        backgroundColor: this.state.isBackHovered ? 'red' : 'white',
                        borderColor: 'red',
                        borderWidth: '1px',
                        borderStyle: 'solid',
                        borderRadius: '20px',
                        fontWeight: 'bold',
                        transition: 'background-color 0.3s, color 0.3s', // Smooth transition
                    }}
                    type="primary"
                    shape="default"
                    onMouseEnter={() => this.setState({ isBackHovered: true })}
                    onMouseLeave={() => this.setState({ isBackHovered: false })}
                    className="login-form-button"
                >
                    Back
                </Button>
                
                <Form.Item style={{ float: 'right' }}>
                {!this.props.isNewLaytimeCalculator && hideInitiateApprovalButton ? null : (
                    <Button
                        type="link"
                        hidden={this.props.editDataAvailable}
                        style={{
                            float: 'left',
                            color: this.state.isClearHovered ? 'blue' : 'red',
                            fontWeight: 'bold',
                            marginRight: '10px',
                            transition: 'background-color 0.3s, color 0.3s', // Smooth transition
                        }}
                        shape="default"
                        onMouseEnter={() => this.setState({ isClearHovered: true })}
                        onMouseLeave={() => this.setState({ isClearHovered: false })}
                        onClick={() => {
                            this.props.onResetFields
                                ? this.props.onResetFields()
                                : this.props.formRef.current.resetFields();
                                
                        }}
                        className="login-form-button"
                    >
                        Clear
                    </Button>
                )}
                </Form.Item>

                <Form.Item style={{ float: 'right' }}>
                <Space direction="vertical">
                    <Space wrap>
                        <Dropdown overlay={menuItems} placement="bottom">
                            <Button
                                style={{
                                marginRight: '10px',
                                color: this.state.isActionsHovered ? 'white' : 'red',
                                backgroundColor: this.state.isActionsHovered ? 'red' : 'white',
                                borderColor: 'red',
                                borderWidth: '1px',
                                borderStyle: 'solid',
                                borderRadius: '20px',
                                fontWeight: 'bold',
                                transition: 'background-color 0.3s, color 0.3s', // Smooth transition
                            }}
                            type="primary"
                            shape="default"
                            onMouseEnter={() => this.setState({ isActionsHovered: true })}
                            onMouseLeave={() => this.setState({ isActionsHovered: false })}
                        >
                            Actions
                        </Button>
                        </Dropdown>
                    </Space>
                </Space>
                </Form.Item>
            </div>
        );
    }
}

export default FormHeader;

