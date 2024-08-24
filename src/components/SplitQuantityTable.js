// 8th sem\Laytime\venv\laytime_frontend\src\components\SplitQuantityTable.js

import React from "react";
import { Table, Form, Input, DatePicker, notification } from "antd";

export default class SplitQuantityTable extends React.Component {
  openNotification = (type, message, description) => {
    notification[type]({
      message,
      description,
      duration: 1,
    });
  };

  onDateChange = (decorator, date) => {
    if (
      decorator == "clarification_of_legal_obligation_from_date" ||
      decorator == "commercial_operation_to_date"
    ) {
      var start_date_field = "clarification_of_legal_obligation_from_date";
      var end_date_field = "commercial_operation_to_date";
      var desired_approval_date = "desired_approval_date";
      var expected_completion_date = "expected_completion_date";
      var start_date =
        this.props.formRef.current.getFieldValue(start_date_field);
      var end_date = this.props.formRef.current.getFieldValue(end_date_field);
      if (
        start_date != undefined &&
        start_date != null &&
        end_date != undefined &&
        end_date != null
      ) {
        const project_duration = end_date.diff(start_date, "days");
        if (project_duration <= 0) {
          this.openNotification(
            "error",
            "Error",
            "Please fill mendetory field"
          );
          this.props.formRef.current.resetFields([decorator]);
        }
      }
      this.props.formRef.current.setFieldsValue({
        [desired_approval_date]:
          this.props.formRef.current.getFieldValue(start_date_field),
      });
      this.props.formRef.current.setFieldsValue({
        [expected_completion_date]:
          this.props.formRef.current.getFieldValue(end_date_field),
      });
    }
    if (decorator.includes("from")) {
      var from_field = decorator;
      var to_field = decorator.replace("from", "to");
      var duration_field = decorator.replace("from_date", "duration");
    } else {
      var to_field = decorator;
      var from_field = decorator.replace("to", "from");
      var duration_field = decorator.replace("to_date", "duration");
    }
    var from_date = this.props.formRef.current.getFieldValue(from_field);
    var to_date = this.props.formRef.current.getFieldValue(to_field);

    if (
      to_date != undefined &&
      to_date != null &&
      from_date != undefined &&
      from_date != null
    ) {
      const duration_days = to_date.diff(from_date, "days");
      if (duration_days < 0) {
        this.openNotification("error", "Error", "Please fill mendetory field");
        this.props.formRef.current.resetFields([duration_field, decorator]);
        return;
      }
      this.props.formRef.current.setFieldsValue({
        [duration_field]: duration_days,
      });
    }
  };

  projectSchedulecolumns = [
    {
      title: <strong>Port Name</strong>,
      dataIndex: "port_name",
      key: "port_name",
      width: "23%",
    },
    {
      title: "Quantity",
      dataIndex: "quantity",
      key: "quantity",
      width: "18%",
      align: "center",
    },
    {
      title: "Amount",
      dataIndex: "amount",
      key: "amount",
      width: "18%",
      align: "center",
    },
  ];

  getProjectScheduleData = (isDisabled) => {
    return [
      {
        port_name: <strong>{"Paradip"}</strong>,
        quantity: (
          <Form.Item
            style={{ margin: "0px" }}
            name="paradip_quantity"
            rules={[{ required: true, message: "Please enter quantity" }]}
          >
            <Input
              style={{ width: "100%" }}
              onChange={(date) => this.onDateChange("paradip_quantity", date)}
              disabled={false}
            />
          </Form.Item>
        ),
        amount: (
          <Form.Item
            style={{ margin: "0px" }}
            name="paradip_amount"
            rules={[{ required: false }]}
          >
            <Input placeholder="Auto calculated" disabled={false} />
          </Form.Item>
        ),
      },
      {
        port_name: <strong>{"Vizag"}</strong>,
        quantity: (
          <Form.Item
            style={{ margin: "0px" }}
            name="viazag_quantity"
            rules={[{ required: true, message: "Please enter quantity" }]}
          >
            <Input
            defaultValue={"0"}
              style={{ width: "100%" }}
              onChange={(date) => this.onDateChange("vizag_quantity", date)}
              disabled={false}
            />
          </Form.Item>
        ),
        amount: (
          <Form.Item
            style={{ margin: "0px" }}
            name="vizag_amount"
            rules={[{ required: false }]}
          >
            <Input placeholder="Auto calculated" disabled={false} />
          </Form.Item>
        ),
      },
      {
        port_name: <strong>{"Total"}</strong>,
        quantity: <Form.Item
        style={{ margin: "0px" }}
        name="total_amount"
        rules={[{ required: true, message: "Please enter quantity" }]}
      >
        <Input
        defaultValue={0}
          style={{ width: "100%" }}
          onChange={(date) => this.onDateChange("total_item", date)}
          disabled={false}
        />
      </Form.Item>,
        amount: (
          <Form.Item
            style={{ margin: "0px" }}
            name="total_amount"
            rules={[{ required: true, message: "Please enter quantity" }]}
          >
            <Input
            defaultValue={"0"}
              style={{ width: "100%" }}
              onChange={(date) => this.onDateChange("total_item", date)}
              disabled={false}
            />
          </Form.Item>
        ),
      },
    ];
  };

  render() {
    const { isDisabled } = this.props;

    return (
        <div>
          <Form.Item
            name=""
            rules={[{ required: false, message: "Please complete the table" }]}
          >
            <div style={{ padding: "20px" }}>
              <Table
                dataSource={this.getProjectScheduleData(isDisabled)}
                pagination={false}
                bordered={true}
                // loading={this.state.showProgress}
                columns={this.projectSchedulecolumns}
              />
            </div>
          </Form.Item>
        </div>
    );
  }
}
