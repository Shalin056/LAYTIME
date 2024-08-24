// C:\Users\shali\Documents\shalin\test-app\src\components\ShippingStage.js

import React, { Component } from "react";
import { openNotification, OPTIONS, API_URLS, METHOD_PUT, METHOD_POST, METHOD_GET, METHOD_PATCH, METHOD_DELETE, METHOD_OPTIONS } from "./Constants";
import {Form, DatePicker, Select, Checkbox, Button, Row, Col, Divider, Space, Input, InputNumber, message,} from "antd";
import { DeleteOutlined, PlusOutlined } from "@ant-design/icons";
import dayjs from "dayjs";

const { Option } = Select;

export default class ShippingStage extends Component {
  state = {
    customOption: null,
    options: OPTIONS.shippingStages,
    defaultPercentage: 100,
  };

  addOptionItem = () => {
    const { options, customOption } = this.state;
    const exists = options.some((option) => option.value === customOption);
  
    if (!exists && customOption) {
      this.setState({
        options: [
          ...options,
          {
            value: customOption,
            label: customOption,
          },
        ],
        customOption: null, 
      });
    }else {
      openNotification("error", "Error", "Stage already exists!");
    }
  };

  handleCountCheckbox = (name) => {
    const { form } = this.props;
    const values = form.getFieldValue("stages");
  
    const currentStage = values.find((stage) => stage.key === name);
  
    if (
      currentStage.stage_name &&
      currentStage.start_date_time &&
      currentStage.end_date_time &&
      currentStage.percentage
    ) {
      this.props.calculateAndSetTimeSaved();
    } else {
      form.setFieldsValue({
        [`stages[${name}].count`]: false,
      });
      message.error("Please fill all required fields before enabling Count.");
    }
  };
  render() {
    const sortedOptions = this.state.options.sort((a, b) =>
      a.label.localeCompare(b.label)
    );
    // const {formRef} = this.props
    return (

      <div className="page" style={{ background: 'white', width: "98.3%", margin: "20px 0px 0px 10px", borderRadius: "10px", boxShadow: "0px 2px 4px rgba(0, 0, 0, 0.1)" }}>
        <legend
          style={{
            borderBottom: '2px solid red',
            fontSize: "x-large",
            textAlign: "left",
            fontWeight: "200",
            color: "red",
            margin: "0px 0px 20px 20px",
            padding: "20px 0px 10px 0px",
            width: "96.5%",
          }}
        >
          Shipping Stage details
        </legend>
        <div style={{ background: "white", width: "100%", margin: '0px 0px 10px 0px', padding: '20px 0px 10px 65px', borderRadius: "10px" }}>
          {/* <Form form = {formRef}> */}
          <Form.List name="stages">
            {(fields, { add, remove }) => (
              <div>
                {fields.map((key, name, ...restField) => (

                  <div key={key}>
                    <Row gutter={16} >
                      <Col span={2}>
                        <Form.Item
                          name={[name, "count"]}
                          label="Count"
                          valuePropName="checked"
                        >
                          <Checkbox defaultChecked={false}
                          //  onChange={() => this.props.resetCalculation()} disabled={this.props.disabled}
                          onChange={() => {
                            const { getFieldValue, setFieldsValue } = this.props.formRef.current;
                            const stageName = getFieldValue(['stages', name, 'stage_name']);
                            const startDate = getFieldValue(['stages', name, 'start_date_time']);
                            const endDate = getFieldValue(['stages', name, 'end_date_time']);
                            const percentage = getFieldValue(['stages', name, 'percentage']);
                        
                            if (stageName && startDate && endDate && percentage) {
                              this.props.calculateAndSetTimeSaved();
                            } else {
                              message.error('Please fill in (Stage Name, Start Date Time, End Date Time, Percentage) before checking the count checkbox.');
                              setFieldsValue({ ['stages']: { [name]: { ['count']: false } } }); 
                            }
                            this.props.resetCalculation();
                          }}
                          disabled={this.props.disabled} 
                          />
                        </Form.Item>
                      </Col>
                      {/* style={{ margin: '0px 100px 0px 0px' }} */}
                      <Col span={8}>
                        <Form.Item
                          {...restField}
                          style={{ textAlign: "left" }}
                          name={[name, "stage_name"]}
                          label="Stage Name"
                          rules={[
                            {
                              required: true,
                              message: "Please select shipping stage",
                            },
                          ]}
                        >
                          <Select
                            showSearch
                            style={{ width: "100%" }}
                            placeholder="Select or enter an option"
                            disabled={this.props.disabled}
                            onSearch={(searchValue) => this.setState({ customOption: searchValue })}
                            dropdownRender={(menu) => (
                              <>
                                {menu}
                                <Divider
                                  style={{
                                    margin: "8px 0",
                                    borderTop: "1px solid black"
                                  }}
                                />
                                <Space
                                  style={{ padding: "0 8px 4px", }}
                                >
                                  <Input
                                    placeholder="Please enter item"

                                    onChange={(e) =>
                                      this.setState({
                                        customOption: e.target.value,
                                      })
                                    }
                                  />
                                  <Button
                                    type="text"
                                    icon={<PlusOutlined />}
                                    onClick={this.addOptionItem}
                                  >
                                    Add Option
                                  </Button>
                                </Space>
                              </>
                            )}
                          >
                            {sortedOptions.map((item) => (
                              <Option key={item.value} value={item.value}>
                                {item.label}
                              </Option>
                            ))}
                          </Select>
                        </Form.Item>
                      </Col>

                      <Col span={4} >
                        <Form.Item
                          {...restField}
                          name={[name, "start_date_time"]}
                          label="Start Date Time"
                          rules={[
                            {
                              required: true,
                              message: "Please select start date time",
                            },
                          ]}
                        >
                          <DatePicker
                            style={{ width: "100%" }}
                            format="YYYY-MM-DD HH:mm"
                            showTime
                            placeholder="select date and time"
                            disabled={this.props.disabled}
                            onChange={() => {this.props.resetCalculation(); this.props.calculateTime();}}
                          />
                        </Form.Item>
                      </Col>

                      <Col span={4}>
                        <Form.Item
                          {...restField}
                          name={[name, "end_date_time"]}
                          label="End Date Time"
                          rules={[
                            {
                              required: true,
                              message: "Please select end date time",
                            },
                          ]}
                        >
                          <DatePicker
                            style={{ width: "100%"}}
                            showTime
                            format="YYYY-MM-DD HH:mm"
                            placeholder="select date and time"
                            disabled={this.props.disabled}
                            onChange={() => {this.props.resetCalculation();this.props.calculateTime();}}
                          />
                        </Form.Item>
                      </Col>

                      <Col span={3}>
                        <Form.Item
                          {...restField}
                          name={[name, "percentage"]}
                          label="Percentage"
                          rules={[
                            {
                              required: true,
                              message: "Please enter a percentage",
                            },
                            {
                              type: "number",
                              min: 0,
                              max: 100,
                              message: "Percentage must be between 0 and 100",
                            },
                          ]}
                          initialValue={this.state.defaultPercentage}
                        >
                          <InputNumber style={{ width: "100%" }} placeholder="Please enter a percentage" disabled={this.props.disabled}
                            min={0}
                            max={100}
                            formatter={(value) => `${value}%`}
                            parser={(value) => value.replace("%", "")} 
                            onChange={() => {
                              this.props.calculateTime();
                            }}
                            />
                        </Form.Item>
                      </Col>


                      {
                        !this.props.disabled &&
                        <Col span={1} style={{ margin: '0px 0px 0px 50px'}}>
                        <Form.Item label="">
                          <DeleteOutlined
                            style={{
                              fontSize: "18px",
                              marginTop: "35px",
                              marginBottom: "0px",
                              color: "red",
                            }}
                            onClick={() => {
                            
                              remove(key.name);
                              this.props.resetCalculation();
                            }}

                          ></DeleteOutlined>
                        </Form.Item>
                      </Col>

                      }

                    </Row>
                    <br />
                  </div>
                ))}

                <Button
                  style={{
                    float: "left",
                    width: "200px",
                    margin: "0 auto",
                    display: "flex",
                    color: this.state.isHovered ? "white" : "red",
                    backgroundColor: this.state.isHovered ? "red" : "white",
                    borderColor: this.state.isHovered ? "black" : "red",
                    borderWidth: "1px",
                    borderStyle: "solid",
                    borderRadius: "20px",
                    fontWeight: "bold",
                    justifyContent: "center",
                    alignItems: "center",
                  }}
                  icon={<PlusOutlined style={{ color: this.state.isHovered ? "white" : "red", fontSize: '16px', }} />}
                  disabled={this.props.disabled}
                  onClick={() => {

                    // this.addShippingStage({ count: true, stage_name: "", start_date_time: null, end_date_time: null });
                    add();
                    this.props.resetCalculation();
                  }}
                  onMouseEnter={() => this.setState({ isHovered: true })}
                  onMouseLeave={() => this.setState({ isHovered: false })}
                >
                  Add Shipping stage
                </Button>
                <br />
                <br />
              </div>
            )}
          </Form.List>
          {/* </Form> */}
        </div>
      </div>
    );
  }
}

