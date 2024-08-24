// C:\Users\shali\Documents\shalin\test-app\src\components\ListHeader.js

import React, { Component } from "react";
import { Button, Dropdown, Input, Menu, Upload } from "antd";
import ListViewFilters from "swfrontend/MDM/MDMScreens/ListView/ListViewFilters";
import ColumnListViewFilters from "swfrontend/MDM/MDMScreens/ListView/ColumnListViewFilters";
import { SearchOutlined } from "@ant-design/icons";
import { getDashData } from '../components/DataProvider';

const { Search } = Input;

export default class ListHeader extends Component {

    state = {
        addButton: true,
        deleteButton: true,
        editButton: true,
        filterClicked: false,
        columnfilterClicked: false,
        searchValue: "",
        searchClicked: false,
        dropdownData: [],
    };

    componentDidMount() {
        this.fetchDashData();
    }

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    fetchDashData = () => {
        getDashData()
            .then(response => response.json())
            .then(data => {
                this.setState({ dropdownData: data, isLoading: false });
            })
            .catch(error => {
                console.error("Error fetching data:", error);
                this.setState({ isLoading: false });
            });
    };

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    handleSearch = (value) => {
        this.setState({ searchClicked: true, searchValue: value });
        this.props.onSearch(value);
    };

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    handleFilterClick = () => {
        this.setState({ filterClicked: true }, () => {
            this.setState({ filterClicked: false });
        });
    };

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    handleColumnFilterClick = () => {
        this.setState({ columnfilterClicked: true }, () => {
            this.setState({ columnfilterClicked: false });
        });
    };

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    handleBeforeUpload = (file) => {
        this.props.excelImport(file);
        return false;
    };

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    render() {
        const menu = (
            <Menu style={{
                    backgroundColor: "white",
                    borderColor: "red",
                    borderWidth: "1px",
                    borderStyle: "solid",
                    borderRadius: "5px",
                    margin:'10px 0px 0px 0px',
                }}>
                <Menu.Item
                    key="1"
                    style={{
                        display: "block",
                        color: this.state.isDeleteHovered ? "white" : "red",
                        backgroundColor: this.state.isDeleteHovered ? "red" : "white",
                        fontWeight: 'bold',
                        transition: 'background-color 0.3s, color 0.3s',
                    }}
                    onMouseEnter={() => this.setState({ isDeleteHovered: true })}
                    onMouseLeave={() => this.setState({ isDeleteHovered: false })}
                    hidden={!this.props.deleteButton}
                    onClick={this.props.deleteField}
                >
                    Delete data
                </Menu.Item>
                
                <Menu.Item
                    key="2"
                    style={{
                        display: "block",
                        color: this.state.isExcelHovered ? "white" : "red",
                        backgroundColor: this.state.isExcelHovered ? "red" : "white",
                        fontWeight: 'bold',
                        transition: 'background-color 0.3s, color 0.3s',
                    }}
                    onMouseEnter={() => this.setState({ isExcelHovered: true })}
                    onMouseLeave={() => this.setState({ isExcelHovered: false })}
                    onClick={this.props.excelExport}>
                    Export to excel
                </Menu.Item>

                <Menu.Item
                    key="3"
                    style={{
                        display: "block",
                        color: this.state.isWorkflowHovered ? "white" : "red",
                        backgroundColor: this.state.isWorkflowHovered ? "red" : "white",
                        fontWeight: 'bold',
                        transition: 'background-color 0.3s, color 0.3s',
                    }}
                    onMouseEnter={() => this.setState({ isWorkflowHovered: true })}
                    onMouseLeave={() => this.setState({ isWorkflowHovered: false })}
                    onClick={this.props.bulkApproval}
                    hidden={this.props.requester}>
                    Approve/Reject
                </Menu.Item>
                
                <Menu.Item
                    hidden={this.props.uploadExcelButton}>
                    <Upload
                        beforeUpload={this.handleBeforeUpload}
                        accept={".csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, application/vnd.ms-excel"}
                        fileList={[]}
                        multiple="false">
                        Import from excel
                    </Upload>
                </Menu.Item>
            </Menu>
        );
        
        // const { dropdownData, selectedStatus } = this.state;
        
        // let buttonWidth = 100; 

        // if (selectedStatus) {
        //     buttonWidth = selectedStatus.length * 10; 
        // }
        // const menu2 = (
        //     <Menu 
        //         style={{
        //             backgroundColor: "white",
        //             borderColor: "red",
        //             borderWidth: "1px",
        //             borderStyle: "solid",
        //             borderRadius: "5px",
        //             margin: '10px 0px 0px 0px'
        //         }}>
                    
        //             <Menu.Item
        //                 key="All"
        //                 style={{
        //                     color: this.state.isStatusHovered ? "white" : "green",
        //                     fontWeight: 'bold', 
        //                 }}
        //                 hidden={this.props.addStatusButton}
        //                 onClick={() => {this.props.onFilterStatus(null);
        //                                 this.setState({ selectedStatus: null });}
        //                         }
        //             >
        //                 All status
        //             </Menu.Item>

        //             {dropdownData.map((item, index) => (
        //                 <Menu.Item
        //                     key={index.toString()}
        //                     style={{
        //                         color: this.state.isStatusHovered ? "white" : "red",
        //                         fontWeight: 'bold', 
        //                     }}
        //                     hidden={this.props.addStatusButton}
        //                     onClick={() => {
        //                         this.props.onFilterStatus(item.name);
        //                         this.setState({selectedStatus: item.name});
        //                  }}
        //                 >
        //                     {item.name}
        //                 </Menu.Item>
        //             ))}
        //     </Menu>
        // );

        if (this.props.showListHeader === false) {
            return null;
        } else {
            return (
                <div>
                    <div className="header_buttons">
                        <div
                            className="search_header"
                            hidden={this.props.hide_search ? this.props.hide_search : false}>
                            <Search
                                placeholder="Search in table"
                                onSearch={this.handleSearch}
                                value={this.state.searchValue}
                                onChange={(e) => {
                                    this.setState({ searchValue: e.target.value });
                                }}
                                style={{ float: "left", width: "65%" }}
                                hidden={this.props.hide_search ? this.props.hide_search : false}
                                enterButton={<Button style={{
                                    fontSize: '16px',
                                    display: "block",
                                    borderRadius: "3px",
                                    backgroundColor: 'red',
                                    color: 'white',
                                }}>
                                    {<SearchOutlined />}
                                </Button>} />

                            <div style={{ display: "inline-block" }}>
                                <Button
                                    type="link"
                                    hidden={!this.state.searchClicked}
                                    onClick={() => {
                                        this.handleSearch("");
                                        this.setState({ searchClicked: false });
                                        this.props.onResetSearch();
                                    }}>
                                    Reset
                                </Button>
                            </div>

                        </div>
                        
                        <Button
                            style={{
                                width: "60px",
                                display: "block",
                                color: "white",
                                backgroundColor: "red",
                                borderColor: "red",
                                borderRadius: "20px",
                                fontWeight: 'bold',
                            }}
                            className={"add_header"}
                            type="primary"
                            onClick={this.props.addField}
                            hidden={!this.props.requester}>
                            New
                        </Button>  

                        <Dropdown className={"drop_down_header"} overlay={menu}>
                            <Button
                                style={{
                                    width: "80px",
                                    display: "block",
                                    color: this.state.isActionHovered ? "white" : "red",
                                    backgroundColor: this.state.isActionHovered ? "red" : "white",
                                    borderColor: "red",
                                    borderWidth: "1px",
                                    borderStyle: "solid",
                                    borderRadius: "20px",
                                    fontWeight: 'bold',
                                    transition: 'background-color 0.3s, color 0.3s'
                                }}
                                onMouseEnter={() => this.setState({ isActionHovered: true })}
                                onMouseLeave={() => this.setState({ isActionHovered: false })}
                                hidden={this.props.addAction}
                                className={"drop_down_header"}
                            >Action</Button>
                        </Dropdown>

                        <Button
                            style={{
                                width: "100px",
                                display: "block",
                                color: this.state.isAddFilterHovered ? "white" : "red",
                                backgroundColor: this.state.isAddFilterHovered ? "red" : "white",
                                borderColor: "red",
                                borderWidth: "1px",
                                borderStyle: "solid",
                                borderRadius: "20px",
                                fontWeight: 'bold',
                                transition: 'background-color 0.3s, color 0.3s' 
                            }}
                            onMouseEnter={() => this.setState({ isAddFilterHovered: true })}
                            onMouseLeave={() => this.setState({ isAddFilterHovered: false })}
                            className={"drop_down_header"}
                            onClick={this.handleFilterClick}
                            hidden={this.props.addFilters}
                        >
                            Add Filters
                        </Button>

                        {/* <Dropdown className={"status"} overlay={menu2}>
                            <Button style={{
                                    // width: `${buttonWidth}px`,
                                    width:'100px',
                                    textAlign: 'center', 
                                    display: 'flex',
                                    justifyContent: 'center',
                                    alignItems: 'center',
                                    color: this.state.isStatusFilterHovered ? "white" : "red",
                                    backgroundColor: this.state.isStatusFilterHovered ? "red" : "white",
                                    borderColor: "red",
                                    borderWidth: "1px",
                                    borderStyle: "solid",
                                    borderRadius: "20px",
                                    fontWeight: 'bold',
                                    transition: 'background-color 0.3s, color 0.3s' 
                                }}
                                onMouseEnter={() => this.setState({ isStatusFilterHovered: true })}
                                onMouseLeave={() => this.setState({ isStatusFilterHovered: false })}
                                hidden={this.props.addStatus}
                                className={"drop_down_header"}
                                >
                                    Get Status
                                
                            </Button>
                        </Dropdown> */}
                        
                        {this.props.columnFilterButton ? (
                            <Button
                                style={{
                                    width: "100px",
                                    display: "block",
                                    color: this.state.isColumnFilterHovered ? "white" : "red",
                                    backgroundColor: this.state.isColumnFilterHovered ? "red" : "white",
                                    borderColor: this.state.isColumnFilterHovered ? "black" : "red",
                                    borderWidth: "1px",
                                    borderStyle: "solid",
                                    borderRadius: "20px",
                                    fontWeight: 'bold',
                                    transition: 'background-color 0.3s, color 0.3s'
                                }}
                                onMouseEnter={() => this.setState({ isColumnFilterHovered: true })}
                                onMouseLeave={() => this.setState({ isColumnFilterHovered: false })}
                                className={"drop_down_header"}
                                onClick={this.handleColumnFilterClick}>
                                Column Filter
                            </Button>) : null}

                        <ColumnListViewFilters
                            {...this.props}
                            handleColumnFilterClick={this.state.columnfilterClicked} />
                        <ListViewFilters
                            {...this.props}
                            handleFilterClick={this.state.filterClicked} />
                    </div>
                </div>
            );
        }
    }
}
