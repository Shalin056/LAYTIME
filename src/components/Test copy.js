// 8th sem\Laytime\venv\laytime_frontend\src\components\Test copy.js

import React, { Component } from "react";
import ShippingStage from "./ShippingStage";
import ShipDetail from "./ShipDetail";
import { Button, Divider, Form,Table, notification } from "antd";
import SplitQuantity from "./SplitQuantity";
import { DownloadOutlined, SaveOutlined } from "@ant-design/icons";
import ReactToPrint from "react-to-print";
import dayjs from "dayjs";
import moment from "moment/moment";
import { apiHelper } from "./Constants";

export default class LayTimeCalculator extends Component {
  formRef = React.createRef();

  state = {
    modelVisibility: false,
    calculatedData: {},
  };

  openNotification = (type, message, description) => {
    notification[type]({
      message,
      description,
      duration: 1,
    });
  };

  componentDidMount() {
      apiHelper("https://accounts.accesscontrol.windows.net/37cd273a-1cec-4aae-a297-41480ea54f8d/tokens/OAuth/2",'POST','grant_type=%20client_credentials&resource=%2000000003-0000-0ff1-ce00-000000000000%2Farcelormittal.sharepoint.com%4037cd273a-1cec-4aae-a297-41480ea54f8d&client_id=%20f4d5ab10-a673-435c-a893-1331b5c8046a%4037cd273a-1cec-4aae-a297-41480ea54f8d&client_secret=%20WKLRPwejD78%2FMzKWCO8sHcEzBMU4x2rp9DiqTQloFHU%3D')
        .then((response) => response.text())
        .then((result) => console.log(result))
        .catch((error) => console.log("error", error));
    }

  onFinish = (values) => {
    const formData = new FormData();
    values.calculatedValue = this.state.calculatedData;
    formData.append("data", JSON.stringify(values));
    console.log(formData);
    console.log(values);

    apiHelper("http://localhost:8001", "POST", formData)
      .then((res) => {
        console.log(res.status);
        if (res.ok) {
          console.log(res);
          res.json().then((res) => {
            this.openNotification(
              "success",
              "data saved successfully",
              res.message
            );
          });
        } else {
          console.log(res);
          res.json().then((res) => {
            this.openNotification(
              "error",
              "error while save data",
              res.message
            );
          });
        }
      })
      .catch((error) => {
        console.error(error);
      });
  };

  resetCalculation = () => {
    this.setState({ calculatedData: [], modelVisibility: false });
  };

  onFinishFailed = (values) => {
    //SHOW ERROR NOTIFICATION
    try {
      if (values.errorFields.length > 0) {
        this.formRef.current.scrollToField(values.errorFields[0].name);
        this.openNotification("error", "Error", "Please fill mendetory field");
      } else {
        return true;
      }
    } catch (error) {
      console.log(error);
    }
  };

  handleCancel = () => {
    this.setState({ modelVisibility: false });
  };

  calculateTime = () => {
    var shipping_stage_details = this.formRef.current.getFieldValue(
      "shipping_stage_details"
    );
    var total_minute = 0;
    var amount = 0;
    var allowed_time = parseFloat(
      this.formRef.current.getFieldValue("allowed_time")
    );
    var demurrage_rate = this.formRef.current.getFieldValue("demurrage_rate");
    var despatch_rate = this.formRef.current.getFieldValue("despatch_rate");
    var actual_time = 0;
    var difference_in_dayjs = 0;
    var total_time_diffrence = 0;
    var difference_in_minutes = 0;
    var isTimeSaved;

    if (shipping_stage_details !== undefined) {
      console.log(shipping_stage_details);
      shipping_stage_details.map((eachStage) => {
        if (
          eachStage &&
          eachStage.is_included &&
          eachStage.end_date_time &&
          eachStage.start_date_time
        ) {
          difference_in_minutes = moment
            .duration(eachStage.end_date_time.diff(eachStage.start_date_time))
            .asMinutes();
          difference_in_dayjs = dayjs(eachStage.end_date_time).diff(
            dayjs(eachStage.start_date_time),
            "minute"
          );
          console.log(difference_in_minutes);
          console.log(difference_in_dayjs);

          difference_in_minutes = Math.round(difference_in_minutes);
          console.log(difference_in_minutes);
          total_minute += difference_in_minutes;
          console.log("day:", (difference_in_minutes / (24 * 60)).toFixed(5));
        }
      });
    }

    if (total_minute && allowed_time && demurrage_rate && despatch_rate) {
      actual_time = (total_minute / (24 * 60)).toFixed(5);
      total_time_diffrence = Math.abs(allowed_time - actual_time).toFixed(5);
      console.log(`total time difference ${total_time_diffrence}`);
      if (allowed_time < actual_time) {
        isTimeSaved = false;
        amount = (total_time_diffrence * demurrage_rate).toFixed(5);
      } else {
        isTimeSaved = true;
        amount = (total_time_diffrence * despatch_rate).toFixed(5);
      }
      this.setState({
        modelVisibility: true,
        calculatedData: {
          amount: amount,
          actual_time: actual_time,
          allowed_time: allowed_time,
          total_time_difference: total_time_diffrence,
          is_time_saved: isTimeSaved,
        },
      });
    } else {
      this.openNotification("error", "Error", "Calculation data is missing");
    }
  };

  getColumns = () => {
    return [
      {
        title: "Total Allowed time",
        dataIndex: "allowed_time",
        key: "allowed_time",
      },
      {
        title: "Total Actual time",
        dataIndex: "actual_time",
        key: "actual_time",
      },
      {
        title: this.state.calculatedData.is_time_saved
          ? "Time Saved"
          : "Time Exceed",
        dataIndex: "total_time_difference",
        key: "total_time_difference",
      },
      {
        title: this.state.calculatedData.is_time_saved
          ? "Total Despatch Amount"
          : "Total Demurrage Amount",
        dataIndex: "amount",
        key: "amount",
      },
    ];
  };

  data = [
    {
      key: "1",
      name: "John Brown",
      borrow: 10,
      repayment: 33,
    },
    {
      key: "2",
      name: "Jim Green",
      borrow: 100,
      repayment: 0,
    },
    {
      key: "3",
      name: "Joe Black",
      borrow: 10,
      repayment: 10,
    },
    {
      key: "4",
      name: "Jim Red",
      borrow: 75,
      repayment: 45,
    },
  ];

  render() {
   
    return (
      <>
      <div style={{ margin: "auto" }}>
        <Form
          layout="vertical"
          className="form"
          ref={this.formRef}
          onFinish={this.onFinish}
          onFinishFailed={this.onFinishFailed}
        >
          <h2>Laytime calculation</h2>
          <Divider />
          <ShipDetail formRef={this.formRef} />
          <Button
            style={{ width: "100px" }}
            type="primary"
            shape="default"
            onClick={() => this.calculateTime()}
          >
            Calculate
          </Button>
          <br />
          <br />
          {this.state.modelVisibility && (
            <Form.Item label="" name="table_value">
              <Table
                dataSource={[this.state.calculatedData]}
                columns={this.getColumns()}
                pagination={false}
                bordered={true}
              />
            </Form.Item>
          )}

          <ShippingStage
            formRef={this.formRef}
            calculateTime={this.calculateTime}
            resetCalculation={this.resetCalculation}
          />
          {this.state.modelVisibility && (
            <SplitQuantity
              calculatedData={this.state.calculatedData}
              formRef={this.formRef}
            />
          )}
          {/* <SplitQuantityTable isDisabled={false} formRef={this.formRef} /> */}

          <Divider />
          <Button
            style={{ width: "100px", float: "left" }}
            type="primary"
            htmlType="submit"
            icon={<SaveOutlined />}
          >
            Save
          </Button>

          <ReactToPrint
            trigger={() => (
              <Button style={{ float: "right" }} icon={<DownloadOutlined />}>
                Download Pdf
              </Button>
            )}
            content={() => this.props.pdfRef.current}
            documentTitle="Laytime-calculation.pdf"
          />
          <br />
          <Divider />
        </Form>
      </div>
      </>
    );
  }
}
