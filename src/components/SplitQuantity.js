// C:\Users\shali\Documents\shalin\test-app\src\components\SplitQuantity.js

import React, { Component } from "react";
import { openNotification, OPTIONS, API_URLS, METHOD_POST } from "./Constants";
import { Form, Select, Button, Row, Col, Input, Divider, InputNumber } from "antd";
import { DeleteOutlined, PlusOutlined } from "@ant-design/icons";
import apiHelper from '../Utils/ApiHelper'

const { Option } = Select;

export default class SplitQuantity extends Component {
  state = {
    remainingQuantity: 0,
    selectedPorts: [],
  };

  componentDidMount() {
    setTimeout(() => {
      this.cargoQuantityChange();
      const split_quantities = this.props.formRef.current.getFieldValue("split_quantities") || [];
      const selectedPorts = split_quantities.map(quantity => quantity.port_name);
      this.setState({ selectedPorts })
    }, 100);
  }

  componentDidUpdate(prevProps) {
    setTimeout(() => {
      this.cargoQuantityChange();
    }, 100);
  }

  cargoQuantityChange = () => {
    var totalAmount = this.props.calculatedData.amount;

    var split_quantities = this.props.formRef.current.getFieldValue("split_quantities");

    var total_quantity = parseFloat(
      this.props.formRef.current.getFieldValue("cargo_qty")
    );

    var used_quantity = 0;

    if (split_quantities !== undefined) {
      split_quantities.forEach((eachQuantity, index) => {
        if (
          eachQuantity &&
          eachQuantity.port_name &&
          eachQuantity.cargo_quantity
        ) {
          used_quantity += parseFloat(eachQuantity.cargo_quantity);
          if (used_quantity > total_quantity) {
            openNotification(
              "warning",
              "Split quantity exceed total quantity"
            );
            used_quantity -= parseFloat(eachQuantity.cargo_quantity);
            eachQuantity.cargo_quantity = eachQuantity.amount = 0;
            return;
          } else {
            eachQuantity.amount = parseFloat((
              (eachQuantity.cargo_quantity / total_quantity) * totalAmount
            ).toFixed(5));
          }
        }
      });
    }
    this.props.formRef.current.setFieldsValue({
      ["remaining_cargo_qty"]: total_quantity - used_quantity,
    });
  };

  // Function to handle API call to save split quantity
  saveSplitQuantity = (data) => {
    apiHelper(API_URLS.CREATE, METHOD_POST, data)
      .then((response) => {
        if (response.ok) {
          response.json().then((responseData) => {
          });
        } else {
          response.json().then((errorData) => {
            console.error("Error saving split quantity", errorData);
          });
        }
      })
      .catch((error) => {
        console.error("Error saving split quantity", error);
      });
  };

  handlePortNameChange = (value, name) => {
    const selectedPorts = [...this.state.selectedPorts];

    if (value) {
      selectedPorts[name] = value;
    } else {
      delete selectedPorts[name];
    }

    this.setState({ selectedPorts });
  };


  removeSplitQuantity = (index) => {
    const split_quantities = [...this.props.formRef.current.getFieldValue("split_quantities")];

    if (split_quantities[index]) {
      const removedPortName = split_quantities[index].port_name;

      if (removedPortName) {
        const selectedPorts = this.state.selectedPorts.filter(port => port !== removedPortName);
        this.setState({ selectedPorts });
      }

      split_quantities.splice(index, 1);
      this.props.formRef.current.setFieldsValue({ split_quantities });
    }
  };

  render() {
    // const {formRef} = this.props
    const splitQuantities = this.props.formRef.current.getFieldValue("split_quantities") || [];
    return (

      <div className="page" style={{ background: 'white', width: "98.5%", margin: "20px 0px 0px 10px", borderRadius: "10px", boxShadow: "0px 2px 4px rgba(0, 0, 0, 0.1)" }}>
        <Divider />
        <legend style={{
          borderBottom: '2px solid red',
          fontSize: "x-large",
          textAlign: "left",
          fontWeight: "200",
          color: "red",
          margin: "0px 0px 20px 20px",
          padding: "0px 0px 10px 0px",
          width: "96.5%",
        }}>
          Split Cargo Quantity
        </legend>
        {/* <Form form={formRef}> */}
        <div style={{ background: "white", width: "100%", margin: '0px 0px 10px 0px', padding: '20px 0px 10px 50px', borderRadius: "10px" }}>
          <Form.Item>
            <Form.List name="split_quantities">
              {(fields, { add, remove }) => (
                <div>
                  {fields.map((key, name, ...restField) => (
                    <div key={key}>
                      <Row gutter={16}>

                        <Col span={10}>
                          <Form.Item
                            {...restField}
                            style={{ textAlign: "left" }}
                            name={[name, "port_name"]}
                            label="Port"
                            rules={[
                              {
                                required: true,
                                message: "Please select port",
                              },
                            ]}
                          >
                            <Select
                              showSearch
                              style={{ width: "100%" }}
                              placeholder="Select or enter an option"
                              allowClear={true}
                              onChange={(value) => this.handlePortNameChange(value, name)}
                              disabled={this.props.disabled}
                            >
                              {OPTIONS.ports.map((item) => (
                                <Option
                                  key={item.value}
                                  value={item.value}
                                  disabled={this.state.selectedPorts.includes(item.value)}
                                >
                                  {item.label}
                                </Option>
                              ))}
                            </Select>
                            {/* <Select
                            showSearch
                            style={{ width: "100%" }}
                            placeholder="Select or enter an option"
                            allowClear={true}
                          >
                            {OPTIONS.ports.map((item) => (
                              <Option key={item.value} value={item.value}>
                                {item.label}
                              </Option>
                            ))}
                          </Select> */}
                          </Form.Item>
                        </Col>

                        <Col span={6}>
                          <Form.Item
                            {...restField}
                            name={[name, "cargo_quantity"]}
                            label="Cargo Quantity"
                            rules={[
                              {
                                required: true,
                                message: "Please enter quantity",
                              },
                            ]}

                          >
                            <InputNumber
                              style={{ width: "100%" }}
                              min={0}
                              type="number"
                              placeholder="enter quantity"
                              onChange={(e) => this.cargoQuantityChange(e)}
                              disabled={this.props.disabled}
                            // onChange={(e) => this.props.formRef.current.setFieldsValue({
                            //   ["amount"]: (e.target.value)})}
                            />
                          </Form.Item>
                        </Col>

                        <Col span={6}>
                          <Form.Item
                            {...restField}
                            name={[name, "amount"]}
                            label="Amount"
                            rules={[
                              {
                                required: true,
                                message: "Please enter amount",
                              },
                            ]}
                          >
                            <Input
                              style={{ width: "100%" }}
                              placeholder="enter amount"
                              disabled={true}
                            />
                          </Form.Item>
                        </Col>

                        {
                          !this.props.disabled && 
                          <Col span={1}>
                          <Form.Item label="">
                            <DeleteOutlined
                              style={{
                                fontSize: "18px",
                                marginTop: "35px",
                                marginBottom: "0px",
                                color: "red",
                              }}
                              onClick={() => {
                                
                                this.removeSplitQuantity(key.name);
                                remove(key.name);
                              }}
                            ></DeleteOutlined>
                          </Form.Item>
                        </Col>

                        }

                      </Row>
                      <br />
                    </div>
                  ))}
                  
                  {/* {splitQuantities.length < OPTIONS.ports.length && */}
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
                  onClick={() => add()}
                  onMouseEnter={() => this.setState({ isHovered: true })}
                  onMouseLeave={() => this.setState({ isHovered: false })}
                >
                  Add Quantity Split
                </Button>
                {/* } */}
                </div>
              )}
            </Form.List>

            <Form.Item
              style={{ float: "right", paddingRight: "50px" }}
              name="remaining_cargo_qty"
              label="Remaining Cargo Quantity"
              rules={[
                {
                  required: false,
                  message: "Please enter remaining cargo quantity",
                },
              ]}
            >
              <Input
                style={{ width: "100%" }}
                placeholder="remaining quantity"
                disabled={true}
              />
            </Form.Item>

          </Form.Item>
          {/* </Form> */}

        </div>
      </div>
    );
  }
}

