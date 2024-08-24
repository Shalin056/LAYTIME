// C:\Users\shali\Documents\shalin\test-app\src\Laytime\Screens\ListView.js

import React from "react";
import { Modal, Input, Button, message, Table } from 'antd';
import "jspdf-autotable";
import ListViewContent from "../../components/ListViewContent";
import { DETAIL, SHIP_DETAIL } from "../../components/Constants";
import { fetchShippingDetail, getGridData, deleteShippingDetail, multipleApproval, exportExcelData} from '../../components/DataProvider';
import { downloadPDF } from '../../components/PDFgenerator';
import { APP_NAME, gridViewConfig, settings } from "swfrontend/AppConfigs.js";
import {file_download_api_call} from "swfrontend/COMS/Utils/ApiCommunicaton.js";
import { error, openNotification, success, warning } from "swfrontend/COMS/NotificationMessageMapping.js";
import {notificationMessage,notificationTitle,openNotificationType} from "swfrontend/MDM/MDMUIConfigs/MDMUIMappings.js";
import QuickForm from 'swfrontend/MDM/MDMScreens/QuickFormView/QuickFormView.js'

const APP = APP_NAME.MASTER;

export default class ListView extends React.Component {

    // navbar = new Navbar();
    state = {
        routeName: process.env.REACT_APP_PROJECT_ROUTE === "/null" ? this.props.location.pathname.substr(1).split("/")[0] : this.props.location.pathname.substr(1).split("/")[1],
        routeState: null,
        columnDefs: SHIP_DETAIL,
        columnDefs1: DETAIL,
        defaultColDef: {
            sortable: true,
            filter: true,
            resizable: true,
        },
        rowData: null,
        rowSelection: "multiple",
        selectedRow: null,
        versionList: null,
        permissions: null,
        addButton: false,
        uploadExcelButton: false,
        deleteButton: false,
        editButton: false,
        columnFilterButton: false,
        pageSize: gridViewConfig.paginationPageSize,
        searchQuery: null,
        filterQuery: null,
        total: 0,
        currentPage: 1,
        addFilters: false,
        dashboardFilter: null,
        requester:false,
        modalVisible: false,
        remark: null,
        bulkApprovalData:null
    };

    componentDidMount() {
        if (this.props.location.searchQuery) {
                this.setState({ dashboardFilter: `status=${this.props.location.searchQuery}&`}, () => {
                    this.fetchGridData(this.state.currentPage);
                });
        }
        else {
            this.fetchGridData(this.state.currentPage);
        }
    }

    handleMenuItemClick = (searchQuery) => {
        this.gridApi.showLoadingOverlay();
        if (searchQuery === null) {
            this.setState({ dashboardFilter: null }, () => {
                this.fetchGridData(this.state.currentPage);
            });
        } else {
            this.setState({ dashboardFilter: `status=${searchQuery}&` }, () => {
                this.fetchGridData(this.state.currentPage);
            });
        }
    };

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    onPaginationChange = (page, pageSize) => {
        if (page === 0 || page === null) {
            page = 1
        }
        this.gridApi.showLoadingOverlay();
        this.setState({ pageSize: pageSize, currentPage: page }, () => {
            this.fetchGridData(page);
        });
    };

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    fileDownload = (file) => {
        file_download_api_call(file.uid).then((res) => {
            if (res.ok) {
                res.blob().then((blob) => {
                    if (navigator.appVersion.toString().indexOf(".NET") > 0) {
                        window.navigator.msSaveBlob(blob, file.name);
                    } else {
                        let url = window.URL.createObjectURL(blob);
                        let a = document.createElement("a");
                        a.href = url;
                        a.download = file.name;
                        a.click();
                    }
                });
            } else {
                openNotification(
                    openNotificationType.error,
                    notificationTitle.api,
                    notificationMessage.apiConnectionError
                );
            }
        });
    };

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    fetchGridData(pageNo) {
        let values = "";
        if (pageNo !== null) {
            values = "?page=" + pageNo;
        }
        
        if (this.state.pageSize !== null) {
            values += "&pageSize=" + this.state.pageSize;
        }
        
        if (this.state.searchQuery !== null) {
            values += "&" + this.state.searchQuery;
        }

        if (this.state.filterQuery !== null) {
            if (this.state.dashboardFilter !== null) {
                values += "&" + this.state.filterQuery.slice(0, -1);
            } else {
                values += "&" + this.state.filterQuery + "filter=1";
            }
        }
        
        if(this.state.dashboardFilter !== null) {
            values += "&" + this.state.dashboardFilter + "filter=1";
        }

        getGridData(values)
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Network response was not ok.');
                }
            })
            .then(responseData => {
                if (responseData.results) {
                    try {
                        this.gridApi.hideOverlay();
                    } catch (e) {
                    }
                    this.setState({ total: responseData.total, rowData: responseData.results, requester: responseData.is_requester});
                    this.gridApi.current.autoSizeColumns();
                } else {
                    openNotification(
                        openNotificationType.error,
                        notificationTitle.api,
                        notificationMessage.apiConnectionError
                    );
                }
            })
            .catch(error => {
                console.error('Error fetching data:', error);
            });
    };

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    onGridReady = (params) => {
        this.gridApi = params.api;
    };

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    onSelectionChanged = () => {
        let selectedRows = this.gridApi.getSelectedRows();
        this.setState(() => ({
            selectedRow: selectedRows,
        }));
    };

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    deleteField = () => {
    if (this.state.selectedRow != null && this.state.selectedRow.length > 0) {
        const temp = this.state.columnDefs[0].primarykeyfield;
        const model_name = 'shipping_detail';
        let listItems = this.state.selectedRow.map(row => row[temp]);

        deleteShippingDetail(model_name, listItems)
            .then(response => {
                if (response.ok) {
                    return response;
                } else {
                    throw new Error('Network response was not ok.');
                }
            })
            .then(data => {
                const updatedRowData = this.state.rowData.filter(row => !listItems.includes(row[temp]));
                this.setState({ rowData: updatedRowData, currentPage: 1 });
                success(this.state.selectedRow.length === 1 ? 'Item deleted successfully' : 'Items deleted successfully');
            })
            .catch(error => {
                console.error('Error deleting item(s):', error);
                // error('Failed to delete item(s)');
            })
            .finally(() => {
                this.setState({ selectedRow: null });
            });
    } else {
        openNotification(
            openNotificationType.warning,
            notificationTitle.delete,
            notificationMessage.listDeleteDataNotSelected
        );
    }
};

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    addField = () => {
        this.props.history.push({
            pathname: `${process.env.REACT_APP_PROJECT_ROUTE}/LaytimeCalculator/new`
        });
    };

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

// excelExport1 = () => {
//     if (this.state.selectedRow == null || this.state.selectedRow.length === 0) {
//         // If no rows are selected, fetch all data
//         this.fetchGridDataForExport(true);
//     } else {
//         // If rows are selected, export selected data
//         this.fetchGridDataForExport(false);
//     }
// };

// fetchGridDataForExport = (allExport) => {
//     let values = "?page=1";
//     if (this.state.pageSize !== null) {
//         values += "&pageSize=" + this.state.pageSize;
//     }
//     if (this.state.searchQuery !== null) {
//         values += "&" + this.state.searchQuery;
//     }
//     if (this.state.filterQuery !== null) {
//         values += "&" + this.state.filterQuery + "filter=1";
//     }
    
//     getGridData(values)
//         .then(response => {
//             if (response.ok) {
//                 return response.json();
//             } else {
//                 throw new Error('Network response was not ok.');
//             }
//         })
//         .then(responseData => {
//             if (responseData.results) {
//                 let data = {
//                     results: responseData.results,
//                     columns: this.state.columnDefs1.map(column => column.field),
//                     search: this.state.searchQuery,
//                     filter: this.state.filterQuery ? this.state.filterQuery.slice(0, -1) : null,
//                     primary_key: this.state.columnDefs1.filter(item => item.hasOwnProperty('primarykeyfield'))[0]['primarykeyfield']
//                 };

//                 allExport ? warning("Please wait! Exporting all data") : warning("Please wait! Exporting selected data");

//                 exportExcelData(data)
//                 .then(response => {
//                     if (response.ok) {
//                         return response.blob();
//                     } else {
//                         throw new Error('Network response was not ok.');
//                     }
//                 })
//                 .then(blob => {
//                     if (navigator.msSaveBlob) {
//                         window.navigator.msSaveBlob(blob, 'Cal.xlsx');
//                     } else {
//                         let url = window.URL.createObjectURL(blob);
//                         let a = document.createElement("a");
//                         a.href = url;
//                         a.download = 'Cal.xlsx';
//                         a.click();
//                     }
//                     success("Successfully Exported to Excel");
//                 })
//                 .catch(error => {
//                     console.error('Error exporting data:', error);
//                 });
//             } else {
//                 openNotification(
//                     openNotificationType.error,
//                     notificationTitle.api,
//                     notificationMessage.apiConnectionError
//                 );
//             }
//         })
//         .catch(error => {
//             console.error('Error fetching data:', error);
//         });
// };


    excelExport1 = () => {
        if (this.state.selectedRow == null || this.state.selectedRow.length === 0) {
            this.excelDownload1("all");
        } else {
            this.excelDownload1(null);
        }
    };

    excelDownload1 = (allExport) => {
        let listItems = [];
        let columns = [];

        for (let i = 0; i < this.state.columnDefs1.length; i++) {
            let value = this.state.columnDefs1[i].field;
            if (value.includes(".")) {
                columns.push(value.split(".")[0]);
            } else {
                if (value.toLowerCase() === 'files') {
                    continue;
                }
                columns.push(value);
            }
        }

        if (allExport) {
            listItems = "all";
        } else {
            for (let i = 0; i < this.state.selectedRow.length; i++) {
                listItems.push(this.state.selectedRow[i]);
            }
            listItems = listItems.map(item => {
                let newItem = { ...item };
                columns.forEach(column => {
                    if (typeof newItem[column] === 'boolean') {
                        newItem[column] = newItem[column] ? 'Yes' : 'No';
                    }
                });
                return newItem;
            });
        }

        let data = {
            results: listItems,
            columns: columns,
            search: this.state.searchQuery,
            filter: this.state.filterQuery ? this.state.filterQuery.slice(0, -1) : null,
            primary_key: this.state.columnDefs.filter(item => item.hasOwnProperty('primarykeyfield'))[0]['primarykeyfield']
        };

        allExport ? warning("Please wait! Exporting all data") : warning("Please wait! Exporting selected data");

        exportExcelData(data)
        .then(response => {
            if (response.ok) {
                return response.blob();
            } else {
                throw new Error('Network response was not ok.');
            }
        })
        .then(blob => {
            if (navigator.msSaveBlob) {
                window.navigator.msSaveBlob(blob, 'Cal.xlsx');
            } else {
                let url = window.URL.createObjectURL(blob);
                let a = document.createElement("a");
                a.href = url;
                a.download = 'Cal.xlsx';
                a.click();
            }
            this.setState({ selectedRow: null });
            success("Successfully Exported to Excel");
        })
        .catch(error => {
            console.error('Error exporting data:', error);
        });
    };

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////


    handleColumnFilter = (columnList) => {
        this.fetchColumnsData(columnList);
    };

    handleFilterApply = (querystring) => {
        try {
            this.gridApi.showLoadingOverlay();    
        } catch (e) {}
        this.setState({ filterQuery: querystring, currentPage: 1 }, () => this.fetchGridData(1));
    };

    handleResetFilter = () => {
        this.gridApi.showLoadingOverlay();
        this.setState({ selectedRow: null, filterQuery: null, currentPage: 1 }, () => this.fetchGridData(1));
    };

    handleResetSearch = () => {
        this.gridApi.showLoadingOverlay();
        this.setState({ selectedRow: null });
    };

    handleColumnResetFilter = () => {
        this.fetchColumnsData(null);
    };

    handleSearchApply = (value) => {
        try {
            this.gridApi.showLoadingOverlay();    
        } catch (e) {}
        
        let quer_param = "search=" + value;
        if (value === "") {
            quer_param = null;
        }
        this.setState({ searchQuery: quer_param, currentPage: 1 }, () => this.fetchGridData(1));
    };

    removeRouteState = () => this.setState({ routeState: null }, () => this.fetchGridData(this.state.currentPage));

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    editField1 = (event) => {
        if (this.state.selectedRow == null || (this.state.selectedRow == null && this.state.searchQuery!=null)){
            const requester = localStorage.getItem('is_requester')
            if (requester){
                this.props.history.push({pathname: `${process.env.REACT_APP_PROJECT_ROUTE}/${window.location.pathname.split("/").pop()}/${event.data.id}`})
            }
            else
            {
                this.props.history.push({pathname: `${process.env.REACT_APP_PROJECT_ROUTE}/${window.location.pathname.split("/").pop()}/${event.data.id}`})
            }
        }

    };

    editField = () => {
        if (this.state.selectedRow != null && this.state.selectedRow.length === 1) {
            const selectedRowData = this.state.selectedRow[0];
            const id = selectedRowData.id;
    
            fetchShippingDetail(id)
                .then(response => {
                    if (response.ok) {
                        return response.json();
                    } else {
                        throw new Error('Network response was not ok.');
                    }
                })
                .then(rowData => {
    
                    // Navigate to the new route with the selected row data
                    
                    this.props.history.push({
                        pathname: `${process.env.REACT_APP_PROJECT_ROUTE}/${window.location.pathname.split("/").pop()}/${id}`,
                        state: { rowData },
                    });
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                    openNotification(
                        openNotificationType.error,
                        notificationTitle.edit,
                        `Error fetching data for id ${id}`
                    );
                });
        } else {
            openNotification(
                openNotificationType.warning,
                notificationTitle.edit,
                notificationMessage.listEditDataNotSelected
            );
        }
    };

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

handleDownloadPDF = (id) => {
    
    if (id) {
        downloadPDF(id)
            .then(response => {
                if (response.ok) {
                    return response.json();
                } else {
                    throw new Error('Network response was not ok.');
                }
            })
            .then(rowData => {
                console.log(rowData);
            })
            .catch(error => {
                console.error('Error fetching rowData:', error);
            });
    } else {
        console.error('No row selected or more than one row selected.');
    }
  };
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    
handleModalVisible = visible => {
    this.setState({ modalVisible: visible });
  };
  
  bulkApproval = () => {
    if (this.state.selectedRow != null && this.state.selectedRow.length > 0) {
    //   if (!this.state.modalVisible) {
    //     const temp = this.state.columnDefs[0]?.primarykeyfield;
    //     const ids = this.state.selectedRow.map(row => row[temp]);
  
    //     const bulkData = {
    //       request_id: ids,
    //       remark: null,
    //       action: null,
    //     };
  
        this.handleModalVisible(true);
        // this.setState({ bulkData });
    //   }
    } else {
      openNotification('error', 'Error', 'Please select rows to perform bulk approval.');
    }
  };
  
  handleAction = (action) => {
    // bulkData.action = action;
    // bulkData.remark = remark;
    
    // multipleApproval(bulkData)
    //   .then(response => {
    //     this.handleModalVisible(false);
    //     this.setState({ remark: null })
    //     window.location.reload();
    //     message.success('Request processed successfully!');
    //   })
    //   .catch(error => {
    //     console.error('Error performing bulk approval:', error);
    //     message.error('Error performing bulk approval. Please try again.');
    //   });
    const ids = this.state.selectedRow.map(row => row['id']);
    const bulkData = {
        remark: this.state.remark,
        action: action,
        request_id: ids
    };
    
    this.setState({ isLoading: true }, () => {
        multipleApproval(bulkData)
        .then(response => {
          if (response.ok) {
              return response.json();
          } else {
              throw new Error('Network response was not ok.');
          }
        })
        .then(rowData => {
          console.log(rowData);
          this.handleModalVisible(false);
          message.success('Request processed successfully!');
          this.setState({ remark: null, bulkApprovalResults: rowData, showResult: true }, () => this.fetchGridData(1));
          })
          .catch(error => {
              console.error('Error performing bulk approval:', error);
              message.error('Error performing bulk approval. Please try again.');
          }).finally(() => this.setState({ isLoading: false }))  
    })
  };
  
/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

    render() {
        const { bulkData, isLoading } = this.state;
        return (
            
            <div>
                <Modal
                    title="Approver Remark"
                    visible={this.state.modalVisible}
                    onCancel={() => this.handleModalVisible(false)}
                    footer={[
                    <Button key="approve" type="primary" style={{ borderRadius: '5px' }} onClick={() => this.handleAction('Approve', bulkData, this.state.remark)}>
                        Approve
                    </Button>,
                    <Button key="reject" type="danger" style={{ borderRadius: '5px' }} onClick={() => this.handleAction('Reject', bulkData, this.state.remark)}>
                        Reject
                    </Button>,
                    ]}
                >
                    <div style={{ textAlign: 'center' }}>
                    <Input.TextArea
                        placeholder="Type your remark here..."
                        onChange={e => this.setState({ remark: e.target.value })}
                        value={this.state.remark}
                    />
                    </div>
                </Modal>

                <Modal
                    style={{ marginTop: "60px", marginBottom: "70px" }}
                    title="Approval Details"
                    centered
                    open={this.state.showResult}
                    onCancel={() => this.setState({ showResult: !this.state.showResult })}
                    width={700}
                    footer={[]}
                >
                    <Table
                        columns={[
                            {
                                title: 'Request ID',
                                dataIndex: 'request_id',
                                key: 'request_id',
                            },
                            {
                                title: 'Status',
                                dataIndex: 'message',
                                key: 'message',
                            }
                        ]}
                        dataSource={this.state.bulkApprovalResults}
                        pagination={false}
                        bordered={true}
                        size="middle"
                    />
                </Modal>

                <ListViewContent
                    {...this.state}
                    context={this}

                    showListHeader={true}
                    addButton={true}
                    uploadExcelButton={true}
                    addFilters={false}
                    filterClicked={true}
                    columnfilterClicked={true}
                    searchClicked={true}

                    addField={this.addField}
                    deleteField={this.deleteField}
                    excelExport={this.excelExport1}
                    onGridReady={this.onGridReady}
                    onSelectionChanged={this.onSelectionChanged}
                    onRowDoubleClicked={this.editField}
                    onFilter={this.handleFilterApply}
                    onResetFilter={this.handleResetFilter}
                    onResetSearch={this.handleResetSearch}
                    onColumnFilter={this.handleColumnFilter}
                    onColumnReset={this.handleColumnResetFilter}
                    onSearch={this.handleSearchApply}
                    onPaginationChange={this.onPaginationChange}
                    onDownloadPDF={this.handleDownloadPDF}
                    onFilterStatus = {this.handleMenuItemClick}
                    requester={this.state.requester}
                    bulkApproval={this.bulkApproval}
                />
                {this.state.routeState ?
                    <QuickForm
                        routeState={this.state.routeState}
                        removeRouteState={this.removeRouteState}
                        routeName={this.state.routeName}
                    /> : null
                }
            </div>

        );
    }
}

