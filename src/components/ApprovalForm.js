// // C:\Users\shali\Documents\shalin\8th sem\test-app\src\components\ApprovalForm.js

import React from "react";
import { Result, Form, Button } from "antd";
import Modal from "react-bootstrap/Modal";
import amns from "swfrontend/assets/images/amns_transparent.png"
import { localStorageVariableName } from "swfrontend/AppConfigs";
import FormLoader from "swfrontend/MDM/MDMScreens/FormView/FormLoader";
import { openNotification } from "swfrontend/COMS/NotificationMessageMapping";
import {openNotificationType, notificationTitle} from "swfrontend/MDM/MDMUIConfigs/MDMUIMappings";
import LayTimeCalculator from "../Laytime/Screens/LayTimeCalculator";
import { get_approval_model,get_indicate_approval_type, patch_workflow_update_call } from "swfrontend/COMS/Utils/ApiCommunicaton.js";

class NoFormApproval extends React.Component {
  // DataProvider = new fetchShippingDetail();
  formRef = React.createRef();
  approvalString = window.location.pathname.split("/").pop();
  authString = null;
  request_id = null;
  app = null;
  model = null;

  state = {
    is_approved: false,
    is_token_expired: false,
    isLoading: false,
    showRemark: false,
    error: false,
    error_msg: "",
    success_msg:"",
    approver: [],
    workflow_completed: false,
    requestID: null,
    authorization: null
  };

  componentDidMount() {
    this.getHashStringData();
  }

  getHashStringData = () => {
    this.setState({ isLoading: true });
    try {
      localStorage.setItem("approval-authorization", this.approvalString);

      get_approval_model()
        .then((res) => {
          if (res.ok) {
            res.json().then((response) => {
              this.setState({requestID: response.request_id, authString: response.auth_token}, ()=> {
                localStorage.setItem(localStorageVariableName.authToken, response.auth_token);
              })

              // UPDATE VALUES FOR FINAL APPROVAL
              this.request_id = response.request_id;
              this.app = 'laytime_detail';
              this.model = 'shipping_detail';
         
              this.setState({ isLoading: false,success_msg:"Request processed Successfully" }, () => {
                this.getNextApprover();
              });
            });
          } else {
            this.setState({ 
              isLoading: false,
              error: true,
              error_msg: "Invalid Approval Token."
            });
  
            return res.json().then((res) => {
              Object.keys(res).forEach((k) => {
                openNotification(
                  openNotificationType.error,
                  k,
                  res[k]
                );    
              });
            });
          }
        }).finally(() => this.setState({ isLoading: false }));
    } catch (error) {
      // ErrorLogger(error.toString())
      // InternalServerError()
    }
  };

  getNextApprover = () => {
    try {
      this.setState({ isLoading: true })
      get_indicate_approval_type('laytime_details', 'shippingdetail', this.request_id).then((res) => {
        if (res.ok) {
          return res.json().then((response) => {
            this.setState({ approver: response.approval_type, isLoading: false });
          });
        } else {
          this.setState({
            isLoading: false,
            error: true,
            // error_msg: NOTIFICATIONS.GET_APPROVAL_GROUP_ERROR,
          });

          openNotification(
            openNotificationType.error,
            notificationTitle.api,
            "error"
          );
        }
      });
    } catch (error) {
      console.error(`Error While Fetching Next Approver${error}`);
    }
  };

  updateWorkflow = async (params) => {
    try {

      this.setState({ isLoading: true });

      patch_workflow_update_call(params)
        .then((res) => {
          if (res.ok) {
            return res.json().then((res) =>
              this.setState({
                is_approved: true,
                isLoading: false,
                showRemark: false,
                success_msg:"Request processed Successfully"
              })
            );
          } else {
            this.setState({
              error: this.state.showRemark === false ? true : false,
              // error_msg: NOTIFICATIONS.WORKFLOW_APPROVE_ERROR,
            });

            openNotification(
              openNotificationType.error,
              notificationTitle.api,
              "error"
              // NOTIFICATIONS.WORKFLOW_APPROVE_ERROR
            );
          }
        })
        .finally(() => this.setState({ isLoading: false }));
    } catch (error) {
      console.error(`Error While Updating Workflow ${error}`);
    }
  };

  render() {
    const {
      is_token_expired,
      is_approved,
      isLoading,
      showRemark,
      error,
      error_msg,
      success_msg,
      workflow_completed,
      requestID
    } = this.state;

    if(this.state.is_approved){
      return(
        <>
        <div style={{ backgroundColor: "white", textAlign: "center" }}>
              <img src={amns} alt="" style={{ width: "150px" }} />
            </div>

            <div className="p-4">
            <Result title={success_msg} status="success" />
          </div>
        </>
        
      )
    }

    return (
      
        <>
        {/* AMNS Logo, For mail approval */}
        
        {
          window.location.pathname.includes("ApprovalForm") && (
            <div style={{ backgroundColor: "white", textAlign: "center" }}>
              <img src={amns} alt="" style={{ width: "150px" }} />
            </div>
          )
        }
                <div style={{margin:'0px 10%'}}>
          {this.state.requestID &&
            <LayTimeCalculator
              requestID={this.state.requestID}
              updateWorkflow={this.updateWorkflow}
            />
          }
        </div>
        {isLoading && (
          <Modal show centered>
            <Modal.Body>
              <FormLoader source="Modal" loading="true" />
              <p className="text-center">loading</p>
            </Modal.Body>
          </Modal>
        )}

        {is_token_expired && (
          <div className="p-4">
            <Result status="error" />
          </div>
        )}

        {workflow_completed && (
          <div className="p-4">
            <Result title={success_msg} status="success" />
          </div>
        )}

        {is_approved && (
          <div className="p-4">
            <Result title={success_msg} status="success" />
          </div>
        )}

        {error && (
          <div className="p-4">
            <Result title={error_msg} status="error" />
          </div>
        )}      
        
      </>
    );
  }
}

export default NoFormApproval;




