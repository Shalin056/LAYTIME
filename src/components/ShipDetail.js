// C:\Users\shali\Documents\shalin\test-app\src\components\ShipDetail.js

import React, { useRef, Component } from "react";
import { Form, Input, DatePicker, Row, Col, notification, Radio, Button, InputNumber} from "antd";
import { getAllowedTime } from './DataProvider';
import TextArea from "antd/lib/input/TextArea";

export default class ShipDetail extends Component {
  
  openNotification = (type) => {
    notification[type]({
      message: "Error",
      description: "Time allowed can not be negative",
      duration: 1,
    });
    this.props.formRef.current.resetFields(["allowed_time"]);
    // this.formRef = this.props.formRef || useRef(null);
  };

  getAllowedTime = () => {
    const cargoQty = this.props.formRef.current.getFieldValue("cargo_qty");
    const dischRate = this.props.formRef.current.getFieldValue("discharge_rate");

    if (cargoQty && dischRate) {
      const data = { cargoQty, dischRate };

      getAllowedTime(data)
        .then(response => {
          if (response.ok) {
            return response.json();
          } else {
            throw new Error('Network response was not ok.');
          }
        })
        .then(responseData => {

          if (responseData.success) {
            const allowedTime = responseData.data.allowed_time.toFixed(5);
            this.props.formRef.current.setFieldsValue({
              ["allowed_time"]: allowedTime,
            });
            this.props.calculateTime()
          } else {
            this.openNotification("error", "Error", responseData.message);
          }
        })
        .catch(error => {
          console.error('Fetch error:', error);
          this.openNotification("error", "Error", "An error occurred.");
        });
    } else {
      this.props.formRef.current.resetFields(["allowed_time"]);
    }
  };
  
  render() {
    // const {formRef} = this.props
    const { rateType } = this.props;
    const label1 = rateType === 'discharge' ? 'Discharge rate' : 'Loading rate';
    const label2 = rateType === 'discharge'? 'Commenced Discharging Time' : 'Commenced Loading Time'
    const label3 = rateType === 'discharge'? 'Completed Discharging Time' : 'Completed Loading Time'

    return (
      // <Form form = {formRef}>
      <div style={{ background: "white", width: "98.3%", margin: '20px 0px 10px 10px', padding: '10px 20px 10px 20px', borderRadius: "5px", boxShadow: "0px 2px 4px rgba(0, 0, 0, 0.1)" }}>
        <legend
          style={{
            fontSize: "x-large",
            borderBottom: '2px solid red',
            textAlign: "left",
            fontWeight: "200",
            color: "red",
            margin: "0px 0px 20px 0px",
            padding: "10px 0px",
            width: "100%",
          }}
          className="font-large"
        >
          Ship Detail
        </legend>
        <Row gutter={16}>
          <Col xs={24} sm={12}>
            <Form.Item
              name="vessel"
              label="Vessel"
              rules={[
                { required: true, message: "Please enter vessel name" },
              ]}

            >
              <Input 
              placeholder="Enter vessel name" 
              maxLength={100} 
              disabled={this.props.disabled} />
            </Form.Item>

            <Form.Item
              name="bl_date"
              label="B/L Date"
              rules={[{ required: true, message: "Please enter B/L Date" }]}
            >
              <DatePicker
                disabled={this.props.disabled}
                format="YYYY-MM-DD"
                style={{ width: "100%" }}
                placeholder="Select date"
              />
            </Form.Item>

            <Form.Item
              name="load_port"
              label="Load Port"
              rules={[
                {
                  required: true,
                  message: "Please enter load port name",
                },
                {
                  pattern: /^[A-Za-z\s!"#$%&'()*+,\-./:;<=>?@[\\\]^_`{|}~]+$/,
                  message: "Only letters are allowed in the load port name"
                },
              ]}
            >
              <Input 
              placeholder="Enter load port name" 
              maxLength={40} 
              disabled={this.props.disabled} />
            </Form.Item>

            <Form.Item
              name="discharge_port"
              label="Discharge Port"
              rules={[
                {
                  required: true,
                  message: "Please enter discharge port name",
                },
                {
                  pattern: /^[A-Za-z\s!"#$%&'()*+,\-./:;<=>?@[\\\]^_`{|}~]+$/,
                  message: "Only letters are allowed in the discharge port name"
                },
                ({ getFieldValue }) => ({
                  validator(_, value) {
                    if (value && value === getFieldValue('load_port')) {
                      return Promise.reject(new Error('Load Port and Discharge Port must not be the same'));
                    }
                    return Promise.resolve();
                  },
                }),
              ]}
            >
              <Input
                placeholder="Enter discharge port name"
                maxLength={40}
                disabled={this.props.disabled}
              />
            </Form.Item>

            <Form.Item
              name="receiver_buyer"
              label="Receiver / Buyer"
              rules={[
                { required: true, message: "Please enter receiver/buyer" },
                {
                  pattern: /^[A-Za-z\s!"#$%&'()*+,\-./:;<=>?@[\\\]^_`{|}~]+$/,
                  message: "Only letters are allowed in the receiver/buyer name"
                },
              ]}
            >
              <Input 
              placeholder="Enter receiver/buyer" 
              maxLength={100} 
              disabled={this.props.disabled} />
            </Form.Item>

            <Form.Item
              name="turn_time_hours"
              label="Turn Time (hrs)"
              rules={[{ required: true, message: "Please enter turn time" },
              ]}
            >
              <InputNumber
                style={{ width:"100%" }}
                min={0}
                placeholder="Enter turn time"
                disabled={this.props.disabled}
              />
            </Form.Item>

            <Form.Item
              name="cargo"
              label="Cargo"
              rules={[
                { required: true, message: "Please enter cargo name" },
                {
                  pattern: /^[A-Za-z\s!"#$%&'()*+,\-./:;<=>?@[\\\]^_`{|}~]+$/,
                  message: "Only letters are allowed in the Cargo name"
                },
              ]}
            >
              <Input placeholder="Enter cargo name" 
              maxLength={100} 
              disabled={this.props.disabled} />
            </Form.Item>

            <Form.Item
              name="shipper_supplier"
              label="Shipper/Supplier"
              rules={[
                {
                  required: true,
                  message: "Please enter shipper/supplier name",
                },
                {
                  pattern: /^[A-Za-z\s!"#$%&'()*+,\-./:;<=>?@[\\\]^_`{|}~]+$/,
                  message: "Only letters are allowed in the shipper/supplier name"
                },
              ]}
            >
              <Input placeholder="Enter shipper/supplier name" 
              maxLength={100} 
              disabled={this.props.disabled} />
            </Form.Item>
          </Col>
          <Col xs={24} sm={12}>
            <Form.Item
              name="demurrage_rate_per_day"
              label="Demurrage rate/day (USD $)"
              rules={[
                { required: true, message: "Please enter demurrage rate" },
              ]}
            >
              <InputNumber
                style={{ width:"100%" }}
                min={0}
                step={0.01}
                max={99999999.99}
                placeholder="Enter demurrage rate"
                onChange={(e) => {this.props.formRef.current.setFieldsValue({
                  ["despatch_rate_per_day"]: (e / 2)
                }); this.props.calculateTime();}}
                disabled={this.props.disabled}
              />
            </Form.Item>

            <Form.Item
              name="despatch_rate_per_day"
              label="Despatch rate/day (USD $)"
              rules={[
                { required: true, message: "Please enter despatch rate" },
              ]}
            >
              <InputNumber
                style={{ width:"100%" }}
                min={0}
                step={0.01}
                max={99999999.99}
                disabled={true}
                placeholder="Enter despatch rate"
                onChange={() => {
                  this.props.calculateTime();
                }}
              />
            </Form.Item>

            <Form.Item
              name="cargo_qty"
              label="Cargo Qty (M/T)"
              rules={[{ required: true, message: "Please enter cargo qty" },
              ]}
            >
              <InputNumber
                style={{ width:"100%" }}
                min={0}
                placeholder="Enter cargo qty"
                onChange={(e) => {
                  this.getAllowedTime(e);
                }}
                disabled={this.props.disabled}
              />
            </Form.Item>
            
            <Form.Item
              name="rate_type"
              label="Rate Type"
              rules={[{ required: true, message: "Please select a rate type" }]}
              // initialValue="discharge"
            >
              <Radio.Group >
                <Radio value="loading" onChange={(e) => this.props.handleRateTypeChange(e.target.value)} disabled={this.props.disabled}>Loading rate</Radio>
                <Radio value="discharge" onChange={(e) => this.props.handleRateTypeChange(e.target.value)} disabled={this.props.disabled}>Discharge rate</Radio>
              </Radio.Group>
            </Form.Item>

            <Form.Item
              name="discharge_rate"
              label={label1}
              rules={[{ required: true, message: `Please enter ${rateType} rate` },
              ]}
            >
              <InputNumber
                style={{ width:"100%" }}
                min={0}
                placeholder={`Enter ${rateType === 'discharge' ? 'Discharge' : 'Loading'} rate`}
                onChange={() => {
                  this.getAllowedTime();
                  // this.props.calculateTime();
                }}
                disabled={this.props.disabled}
              />
            </Form.Item>

            <Form.Item
              style={{ color: "black", opacity: "1" }}
              name="allowed_time"
              label="Time allowed"
              rules={[
                { required: true, message: "Please enter time allowed" },
              ]}
            >
              <InputNumber
                style={{ width:"100%" }}
                placeholder="Enter allowed time"
                disabled={true}
                // onChange={() => 
                //   this.props.calculateTime()
                // }
              />
            </Form.Item>

            <Form.Item
              name="charter_type"
              label="Charter Type"
              rules={[
                { required: true, message: "Please enter charter type" },
                {
                  pattern: /^[A-Za-z\s!"#$%&'()*+,\-./:;<=>?@[\\\]^_`{|}~]+$/,
                  message: "Only letters are allowed in the Charter Type"
                },
              ]}
            >
              <Input placeholder="Enter charter type" 
              maxLength={100} 
              disabled={this.props.disabled} />
            </Form.Item>
            <Form.Item
              name="nor_tendered"
              label="NOR Tendered"
              rules={[
                { required: true, message: "Please enter NOR tendered" },
              ]}
            >
              <DatePicker
                style={{ width: "100%" }}
                format="YYYY-MM-DD HH:mm"
                showTime={true}
                placeholder="Select date and time"
                disabled={this.props.disabled}
              />
            </Form.Item>
            
          </Col>
        </Row>
        <Row gutter={16}>
          <Col xs={24} sm={12}>
          <Form.Item
              name="commenced_loading_time"
              // label="Commenced Loading Time"
              label={label2}
              rules={[
                {
                  required: true,
                  message: `Please enter commenced ${rateType} time`,
                },
              ]}
            >
              <DatePicker
                style={{ width: "100%" }}
                format="YYYY-MM-DD HH:mm"
                showTime={true}
                placeholder="Select date and time"
                disabled={this.props.disabled}
              />
            </Form.Item>
          </Col>
          <Col xs={24} sm={12}>
          <Form.Item
              name="completed_loading_time"
              // label="Completed Loading Time"
              label={label3}
              rules={[
                {
                  required: true,
                  message: `Please enter completed ${rateType} time`,
                },
              ]}
            >
              <DatePicker
                style={{ width: "100%" }}
                format="YYYY-MM-DD HH:mm"
                showTime={true}
                placeholder="Select date and time"
                disabled={this.props.disabled}
              />
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col xs={24} sm={12}>
          <Form.Item
              name="remarks"
              label="Remarks"
              rules={[
                {
                  required: false,
                  message: "Please enter Remark",
                },
              ]}
            >
              <TextArea
                style={{ width: "100%" }}
                placeholder="Enter Remark"
                maxLength={200}
                disabled={this.props.disabled}
                
              />
            </Form.Item>
          </Col>
        </Row>

      </div>
      // </Form>
    );
  }
}


