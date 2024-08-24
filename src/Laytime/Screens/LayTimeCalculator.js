// C:\Users\shali\Documents\shalin\test-app\src\Laytime\Screens\LayTimeCalculator.js

import React, { Component } from "react";
import { Button, Divider, Form, Table, notification, message } from "antd";
import moment from "moment";
import "jspdf-autotable";
import ShipDetail from "../../components/ShipDetail";
import ShippingStage from "../../components/ShippingStage"
import SplitQuantity from "../../components/SplitQuantity";
import SplitQuantityTable from "../../components/SplitQuantityTable";
import CustomLoader from "../../components/Commons/CustomLoader";
import FormHeader from "../../components/FormHeader";
import WorkflowSection from "../../components/WorkflowSection";
import { downloadPDF } from '../../components/PDFgenerator';
import { METHOD_POST } from '../../components/Constants';
import { fetchShippingDetail, addOrUpdateShippingDetail, initiateWorkflow, navigateToLaytimeCalculator, getCalculateTime, exportToExcel, showApprovalButton } from '../../components/DataProvider';
import { error, success, warning } from "swfrontend/COMS/NotificationMessageMapping.js";
import { patch_workflow_update_call, get_indicate_approval_type } from "swfrontend/COMS/Utils/ApiCommunicaton.js";
import dayjs from 'dayjs';

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

export default class LayTimeCalculator extends Component {
  formRef = React.createRef();
  pdfRef = React.createRef();

  state = {
    modelVisibility: false,
    calculatedData: {},
    isLoading: false,
    rowData: {},
    approver: [],
    approval: { show_section: false },
    isSaveClicked: false,
    id: '',
    rateType: 'discharging'
  };

  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  openNotification = (type, message, description) => {
    notification[type]({
      message,
      description,
      duration: 2,
    });
  };

  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  componentDidMount() {
    let id = this.props.requestID;
    if (!id) {
      const { id: idFromParams } = this.props.match.params;
      id = idFromParams;
    }

    if (!id) {
      this.props.history.push(`${process.env.REACT_APP_PROJECT_ROUTE}/LaytimeCalculator/new`);
    } else {
      this.setState({ id })
      fetchShippingDetail(id)
        .then(response => {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error('Network response was not ok.');
          }
        })
        .then(rowData => {
          this.setState({ rowData });

          this.approvalType();
          this.showApprovalButton();

          if (rowData) {
            console.log('rowData: ', rowData)

            if (this.formRef.current) {
              // Keys to exclude
              const keysToExclude = ["laytime_calculator", "created_date", "updated_date", "is_deleted", "is_active"];

              // Filter keys to include only those not in keysToExclude
              const keysToInclude = Object.keys(rowData).filter(key => !keysToExclude.includes(key));

              // Iterate over the keys to include
              keysToInclude.forEach((key) => {
                // Ignore specific keys
                if (["stages", "split_quantities", "laytime_calculator"].includes(key)) {
                  return; // Skip this key
                }

                // Handle specific date fields
                if (key === "bl_date" || key === "nor_tendered" || key === "commenced_loading_time" || key === "completed_loading_time") {
                  const dateValue = moment(rowData[key], "DD-MM-YYYY HH:mm:ss");
                  if (dateValue.isValid()) {
                      this.formRef.current.setFieldsValue({ [key]: dateValue });
                  } else {
                      console.error('Invalid date format for key:', key, 'value:', rowData[key]);
                  }
                } else {
                    this.formRef.current.setFieldsValue({ [key]: rowData[key] });
                }
              });

              // Set values for the nested arrays
              Object.keys(rowData).forEach((key) => {
                if (Array.isArray(rowData[key])) {
                  const arrayValues = rowData[key].map((item, index) => {
                    const itemValues = {};
                    Object.keys(item).forEach((nestedKey) => {
                      // Exclude specific keys from the nested array
                      if (!["shipping_detail",
                        "is_approved",
                        "is_deleted",
                        "created_date",
                        "last_updated_date",
                        "created_by",
                        "last_updated_by",
                        "remaining_cargo_qty",
                        "is_active"].includes(nestedKey)) {
                        // Handle specific date fields in the nested array
                        if (nestedKey === "start_date_time" || nestedKey === "end_date_time") {
                          const dateValue = moment(item[nestedKey], "DD-MM-YYYY HH:mm:ss");
                          if (dateValue.isValid()) {
                            itemValues[`${nestedKey}`] = dateValue;
                          } else {
                            console.error("Invalid date format for nested key:", nestedKey, "value:", item[nestedKey]);
                          }
                        } else {
                          itemValues[`${nestedKey}`] = item[nestedKey];
                        }
                      }
                    });
                    return itemValues;
                  });
                  this.formRef.current.setFieldsValue({ [key]: arrayValues });
                }
              });

              this.calculateTime();
              this.handleRateTypeChange(rowData['rate_type']);
            } else {
              console.error("Form reference not available");
            }
          }
        })
        .catch(error => {
          console.error("Failed to fetch data:", error);
        });
    }
  }

  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  // validateDate() {
  //   const stages = this.formRef.current.getFieldValue("stages");
  //   console.log('-----stagevalidateDate--------',stages)
    
    
  //   if (!stages) {
  //     this.openNotification("warning", "Warning", "Please add Shipping stages.");
  //     return false;
  //   }
  
  //   console.log(stages);
  
  //   let errorOccurred = false;
  
  //   stages.forEach((each, index) => {
  //     if (!(each['start_date_time'] < each['end_date_time'])) {
  //       this.openNotification("error", "Error", "Start date time must be less than end date time for stage " + index);
  //       errorOccurred = true;
  //     }
  //   });
  
  //   return !errorOccurred;
  // }

  validateDate() {
    const shipping_detail = this.formRef.current.getFieldsValue("shipping_detail");
    const commenced_loading_time = shipping_detail['commenced_loading_time'];
    const completed_loading_time = shipping_detail['completed_loading_time'];
    
    if (shipping_detail.completed_loading_time < shipping_detail.commenced_loading_time) {
      this.openNotification("error", "Error", "Completed time cannot be older than commenced time.");
      return false;
    }
    const stages = this.formRef.current.getFieldValue("stages");
        
    if (!stages) {
      this.openNotification("warning", "Warning", "Please add Shipping stages.");
      return false;
    }

    let errorOccurred = false;
    
    stages.forEach((each, index) => {
      if (!(each['start_date_time'] < each['end_date_time'])) {
        this.openNotification("error", "Error", "Start date time must be less than end date time for stage " + index);
        errorOccurred = true;
      }
      if (each['start_date_time'] < commenced_loading_time || each['start_date_time'] > completed_loading_time) {
        this.openNotification("error", "Error", "Start date time for stage " + index + " must be within the range of commenced and completed loading time.");
        errorOccurred = true;
      }
      if (each['end_date_time'] < commenced_loading_time || each['end_date_time'] > completed_loading_time) {
        this.openNotification("error", "Error", "End date time for stage " + index + " must be within the range of commenced and completed loading time.");
        errorOccurred = true;
      }
    });
    
    return !errorOccurred;
  }

  onFinish = () => {
    try {
      
      const shipping_detail = this.formRef.current.getFieldsValue("shipping_detail");
      if (!this.validateDate()) {
        return;
      }
      shipping_detail['bl_date'] = moment(shipping_detail['bl_date']).format('YYYY-MM-DD');
      shipping_detail['nor_tendered'] = moment(shipping_detail['nor_tendered']).format('YYYY-MM-DD HH:mm:ss');
      shipping_detail['completed_loading_time'] = moment(shipping_detail['completed_loading_time']).format('YYYY-MM-DD HH:mm:ss');
      shipping_detail['commenced_loading_time'] = moment(shipping_detail['commenced_loading_time']).format('YYYY-MM-DD HH:mm:ss');
      
      console.log("shipping_detail.completed_loading_time: ",shipping_detail)
      if (shipping_detail.completed_loading_time < shipping_detail.commenced_loading_time) {
        this.openNotification("error", "Error", "Completed time cannot be older than commenced time.");
        return false;
      }

      if (Array.isArray(shipping_detail.stages) && shipping_detail.stages.length > 0) {

        const id = this.state.id
        if (!this.state.calculatedData.is_time_saved) {
          const remark = this.formRef.current.getFieldValue('remarks');
          if (!remark) {
            this.openNotification("warning", "Warning", "Please enter reason for demurrage.");
            return;
          }
        }
        addOrUpdateShippingDetail(shipping_detail, id)
          .then(response => {
            if (response.ok) {
              return response.json();
            } else {
              throw new Error('Network response was not ok.');
            }
          })
          .then(responseData => {
            if (responseData) {
              message.success(id ? "Data updated successfully!" : "Data added successfully!");
              this.resetCalculation();

              navigateToLaytimeCalculator(this.props.history, METHOD_POST);
            } else {
              console.error(id ? "Error updating Data:" : "Error adding Data:", responseData);
              message.error(id ? "Failed to update Data" : "Failed to add Data");
            }
          })
          .catch(error => {
            console.error("Error adding shipping stage:", error);
            message.error("Failed to add/update shipping stage");
          });
      } else {
        console.error("Form values for data are empty.");
        message.error("Please add Shipping details and Shipping stage details.");
      }
    } catch (error) {
      console.error("Error adding shipping stage:", error);
      message.error("Failed to add/update shipping stage");
    }
  };

  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  calculateTime = async (demurrageCheck=false) => {
    let isValid = await this.formRef.current.validateFields().catch(this.onFinishFailed);
    // if (!isValid) {
    //   return
    // }
    console.log(demurrageCheck)
    const shipping_detail = this.formRef.current.getFieldsValue("shipping_detail");
    console.log(moment(shipping_detail['commenced_loading_time']).format('YYYY-MM-DD HH:mm:ss'))
    console.log(moment(shipping_detail['completed_loading_time']).format('YYYY-MM-DD HH:mm:ss'))

    const stages = this.formRef.current.getFieldValue("stages");
    if (!this.validateDate()) {
      return;
    }

    delete shipping_detail.stages;
    delete shipping_detail.split_quantities;
    delete shipping_detail.remaining_cargo_qty;

    const otherData = {
      allowed_time: parseFloat(this.formRef.current.getFieldValue("allowed_time")),
      demurrage_rate_per_day: parseFloat(this.formRef.current.getFieldValue("demurrage_rate_per_day")),
      despatch_rate_per_day: parseFloat(this.formRef.current.getFieldValue("despatch_rate_per_day")),
    };
    this.setState({ isLoading: true }, () => {
    getCalculateTime(shipping_detail, stages, otherData)
      .then(response => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error('Network response was not ok.');
        }
      })
      .then(responseData => {
        
        let res = responseData.calculatedData
        if(demurrageCheck && !res['is_time_saved']) {
          message.info("Vessel on Demurrage");
        }

        if (responseData.calculatedData) {
          this.setState({
            modelVisibility: demurrageCheck ? false : true,
            calculatedData: responseData.calculatedData,
          });
        } else {
          this.openNotification("error", "Error", responseData.message);
        }
      })
      .catch(error => {
        console.error("API request error:", error);
        this.openNotification("error", "Error", error.message);
      }).finally(() => this.setState({ isLoading: false }));
    })
  };

  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  resetCalculation = () => {
    if (this.state.modelVisibility) {
      this.setState({ calculatedData: [], modelVisibility: false });
    }
  };

  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  onFinishFailed = (values) => {
    try {
      if (values.errorFields.length > 0) {
        this.formRef.current.scrollToField(values.errorFields[0].name);
        this.openNotification("error", "Error", "Please check the form");
      } else {
        return true;
      }
    } catch (error) {
      console.log(error);
    }
  };

  ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  getColumns = () => {
    const isDemurrage = !this.state.calculatedData.is_time_saved;
    const cellStyle = {
      backgroundColor: isDemurrage ? '#FF2400' : 'rgb(0, 180, 0)',
      color: 'white',
      padding: '10px 0px',
      margin: '0px 0px',
      borderRadius: '5px',
      display: 'inline-block',
      width: '100%',
      textAlign: 'center',
      fontSize: '15px'
    };

    const valueStyle = {
      fontWeight: 'bold'
    };

    const columns = [
      {
        title: (
          <span style={cellStyle}>
            Total Allowed time (in days)
          </span>
        ),
        dataIndex: "allowed_time",
        key: "allowed_time",
        align: 'center',
        render: (text) => <span style={{ ...valueStyle }}>{text}</span>
      },
      {
        title: (
          <span style={cellStyle}>
            Total Actual time (in days)
          </span>
        ),
        dataIndex: "actual_time",
        key: "actual_time",
        align: 'center',
        render: (text) => <span style={{ ...valueStyle }}>{text}</span>
      },
      {
        title: this.state.calculatedData.is_time_saved
          ? (
            <span style={cellStyle}>
              Time Saved (in days)
            </span>
          )
          : (
            <span style={cellStyle}>
              Time Exceed (in days)
            </span>
          ),
        dataIndex: "total_time_difference",
        key: "total_time_difference",
        align: 'center',
        render: (text) => <span style={{ ...valueStyle }}>{text}</span>
      },
      {
        title: (
          <span style={cellStyle}>
            {isDemurrage ? 'Total Demurrage Amount (USD $)' : 'Total Despatch Amount (USD $)'}
          </span>
        ),
        dataIndex: "amount",
        key: "amount",
        align: 'center',
        render: (text) => <span style={{ ...valueStyle }}>{text}</span>
      },
    ];

    return columns;
  };

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  calculateAndSetTimeSaved = () => {
    this.calculateTime(true);  
  };

/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  onBackPressed = () => {
    // this.props.history.goBack();
    const isRequester = localStorage.getItem('is_requester') === 'true';
    const route = isRequester ? `${process.env.REACT_APP_PROJECT_ROUTE}/LaytimeCalculator` : `${process.env.REACT_APP_PROJECT_ROUTE}/LaytimeApprovals`;
    this.props.history.push(route);
  };

  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  handleDownloadPDF = () => {
    const id = this.state.id;
    console.log(id)
    if (id) {
      this.setState({ isLoading: true }, () => {
        downloadPDF(id)
        .then(response => {
          if (response.ok) {
            console.log(response)
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
        })
        .finally(() => this.setState({ isLoading: false }));
      });
    } else {
      console.error('No row selected or more than one row selected.');
    }
  };
  // handleDownloadPDF = async () => {
  //   const id = this.state.id;
  //   console.log(id);
  //   const shipping_detail = this.formRef.current.getFieldsValue("shipping_detail");
  
  //   if (!this.validateDate()) {
  //     return;
  //   }
  
  //   // Format dates
  //   shipping_detail['bl_date'] = moment(shipping_detail['bl_date']).format('YYYY-MM-DD');
  //   shipping_detail['nor_tendered'] = moment(shipping_detail['nor_tendered']).format('YYYY-MM-DD HH:mm:ss');
  //   shipping_detail['completed_loading_time'] = moment(shipping_detail['completed_loading_time']).format('YYYY-MM-DD HH:mm:ss');
  //   shipping_detail['commenced_loading_time'] = moment(shipping_detail['commenced_loading_time']).format('YYYY-MM-DD HH:mm:ss');
    
  //   console.log("shipping_detail.completed_loading_time: ", shipping_detail);
  
  //   // Check if completed time is before commenced time
  //   if (shipping_detail.completed_loading_time < shipping_detail.commenced_loading_time) {
  //     this.openNotification("error", "Error", "Completed time cannot be older than commenced time.");
  //     return false;
  //   }
  
  //   if (Array.isArray(shipping_detail.stages) && shipping_detail.stages.length > 0) {

  //     if (id) {
  //       try {
  //         this.setState({ isLoading: true });
  
  //         const response = await addOrUpdateShippingDetail(shipping_detail, id);
  //         if (!response.ok) {
  //           throw new Error('Network response was not ok.');
  //         }
  
  //         const responseData = await response.json();
  //         console.log('))))))', responseData)
  //         if (responseData) {
  //           message.success(id ? "Data updated successfully!" : "Data added successfully!");
  //           this.resetCalculation();
  //         } else {
  //           console.error(id ? "Error updating Data:" : "Error adding Data:", responseData);
  //           message.error(id ? "Failed to update Data" : "Failed to add Data");
  //         }
  
  //         const pdfResponse = await downloadPDF(id);
  //         console.log('((((((((', pdfResponse)
  //         if (!pdfResponse.ok) {
  //           throw new Error('Network response was not ok.');
  //         }
  
  //         const rowData = await pdfResponse.json();
  //         console.log(rowData);
          
  //       } catch (error) {
  //         console.error('Error:', error);
  //       } finally {
  //         this.setState({ isLoading: false });
  //         // this.calculateTime();
  //       }
  //     } else {
  //       console.error('No row selected or more than one row selected.');
  //     }
  //   }
  // };
  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  handleDownloadExcel = () => {
    warning("Please wait, While we are downloading the excel");
    exportToExcel(this.state.rowData)
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
      .catch(e => {
        console.error('Error exporting data:', e);
        error("Error downloading excel file");
      });
  };

  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  updateWorkflow = (params) => {
    this.setState({ isLoading: true })
    try {
      patch_workflow_update_call(params)
        .then((res) => {
          if (res.ok) {
            window.onbeforeunload = null;
            window.location.reload();
          } else {
            return res.json()
          }
        }).finally(() => { this.setState({ isLoading: false }) });
    } catch (error) {
      console.log(error);

    }
  };

  showApprovalButton = () => {
    try {
      const id = this.state.id
      showApprovalButton('laytime_details', 'shippingdetail', id)
        .then(response => {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error('Network response was not ok.');
          }
        })
        .then(responseData => {
          this.setState({
            approval: responseData
          });
        })
        .catch(error => {
          console.error('Error fetching data:', error);
        });
    } catch (error) {
      console.log(error);
    }
  };

  approvalType = () => {
    const id = this.state.id
    try {
      if (this.props.approval_status !== "Draft") {
        get_indicate_approval_type('laytime_details', 'shippingdetail', id)
          .then((res) => {
            if (res.ok) {
              return res.json().then((response) => {
                this.setState({
                  approver: response.approval_type
                });
              });
            } else if (res.status === 401) {
              window.onbeforeunload = null;
              window.location.reload();
            } else {
              return res.json().then((res) => {
                Object.keys(res).forEach((k) => { });
              });
            }
          })
          .catch((error) => {
            console.error("Error in API call:", error);
          });
      }
    } catch (error) {
      console.error("Error in try block:", error);
    }
  };

  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  initiateApproval = async() => {
    let isValid = await this.formRef.current.validateFields().catch(this.onFinishFailed);
    if (isValid) {
      let values = this.formRef.current.getFieldsValue();
      this.setState({ isLoading: true }, () => {
        const id = this.state.id
  
        initiateWorkflow(id, values)
          .then(response => {
            if (response.ok) {
              return response;
            } else {
              throw new Error('Network response was not ok.');
            }
          })
          .then(responseData => {
            message.success('Approval initiated successfully!');
            window.location.reload();
          })
          .catch(error => {
            console.error('Error initiating approval:', error);
            message.error('Failed to initiate approval.');
          })
          .finally(() => this.setState({ isLoading: false }));
      })
    }
  };

  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  onResetFields = () => {
    this.setState({
      modelVisibility: false
    }, () => this.formRef.current.resetFields())
  }

  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  handleRateTypeChange = (value) => {
    this.setState({ rateType: value });
  };

  /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  render() {
    const { isLoading, rowData, isSaveClicked } = this.state;
    const id = this.state.id
    const isNewLaytimeCalculator = !id;
    const hideInitiateApprovalButton = rowData && rowData.status !== "Draft" && !isSaveClicked;

    return (
      <>
        {isLoading && <CustomLoader message={"Please Wait"} />}
        <div style={{ margin: "auto", flexDirection: 'column', alignItems: 'center', justifyContent: 'center', fontSize: '25px' }}>
          <Form
            layout="vertical"
            className="ant-form ant-form-vertical"
            ref={this.formRef}
            onFinish={this.onFinish}
            onFinishFailed={this.onFinishFailed}
          >
            <FormHeader
              {...this.props}
              formRef={this.formRef}
              showBackButton={!this.props.requestID}
              onBackPressed={this.onBackPressed}
              // onCalculate={this.calculateTime}
              onDownloadPDF={this.handleDownloadPDF}
              onDownloadExcel={this.handleDownloadExcel}
              showSaveButton={true}
              initiateApproval={this.initiateApproval}
              isNewLaytimeCalculator={isNewLaytimeCalculator}
              rowData={this.state.rowData}
              onResetFields={this.onResetFields}
            />

            {this.state.rowData.hasOwnProperty("status") && this.state.rowData.status !== "Draft" &&
              <WorkflowSection
                formRef={this.props.formRef}
                hideApprovalAction={!this.state.approval.show_section}
                app="laytime_details"
                model="shippingdetail"
                isRemarksRequired={true}
                request_no={id}
                approval_status={this.state.rowData.status}
                approval_type={this.state.approver}
                status={this.state.rowData.status}
                updateWorkflow={this.props.requestID ? this.props.updateWorkflow : this.updateWorkflow}
                request_category="shippingdetail"
                request_date={this.state.rowData.created_date}
              />
            }

            <ShipDetail
              formRef={this.formRef}
              rateType={this.state.rateType}
              disabled={!isNewLaytimeCalculator && (rowData.status !== "Draft" && !isSaveClicked)}
              handleRateTypeChange={this.handleRateTypeChange}
              calculateTime={this.calculateTime}
            />

            {!isNewLaytimeCalculator && hideInitiateApprovalButton ? null : (
              <Button
                style={{
                  width: "100px",
                  margin: "20px auto",
                  display: "block",
                  color: this.state.isCalculateHovered ? "white" : "red",
                  backgroundColor: this.state.isCalculateHovered ? "red" : "white",
                  borderColor: this.state.isCalculateHovered ? "black" : "red",
                  borderWidth: "1px",
                  borderStyle: "solid",
                  borderRadius: "20px",
                  fontWeight: 'bold',
                  transition: 'background-color 0.3s, color 0.3s'
                }}
                type="primary"
                shape="default"
                onClick={() => this.calculateTime()}
                onMouseEnter={() => this.setState({ isCalculateHovered: true })}
                onMouseLeave={() => this.setState({ isCalculateHovered: false })}
              >
                Calculate
              </Button>
            )}
            <br />

            {this.state.modelVisibility && (
              <React.Fragment>

                <div style={{ background: 'white', margin: '0px 10px 0px 10px', padding: '10px 10px 10px 10px', borderRadius: '10px', boxShadow: "0 2px 4px rgba(0, 0, 0, 0.1)" }}>
                  <legend
                    style={{
                      borderBottom: `2px solid ${this.state.calculatedData.is_time_saved ? 'rgba(0, 100, 0)' : 'red'}`,
                      fontSize: "x-large",
                      textAlign: "left",
                      fontWeight: "200",
                      color: `${this.state.calculatedData.is_time_saved ? 'rgba(0, 100, 0)' : 'red'}`,
                      padding: "10px 0px",
                      width: "98%",
                      margin: '0px 0px 20px 10px'
                    }}
                  >
                    Laytime Calculation
                  </legend>

                  <Table
                    dataSource={[this.state.calculatedData]}
                    columns={this.getColumns()}
                    pagination={false}
                    bordered={true}
                    style={{
                      margin: '0px 10px 50px 10px',
                      background: 'white',
                      borderRadius: '10px',
                    }}
                  />

                </div>
              </React.Fragment>
            )}

            <ShippingStage
              formRef={this.formRef}
              calculateTime={this.calculateTime}
              resetCalculation={this.resetCalculation}
              calculateAndSetTimeSaved={this.calculateAndSetTimeSaved}
              disabled={!isNewLaytimeCalculator && (rowData.status !== "Draft" && !isSaveClicked)}
            />
            {this.state.modelVisibility && (
              <SplitQuantity
                calculatedData={this.state.calculatedData}
                formRef={this.formRef}
                disabled={!isNewLaytimeCalculator && (rowData.status !== "Draft" && !isSaveClicked)}
              />
            )}

            <br />
            <Divider />

          </Form>
        </div>
      </>
    );
  }
}


