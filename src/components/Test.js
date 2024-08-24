// 8th sem\Laytime\venv\laytime_frontend\src\components\Test.js

import React, { Component } from "react";
import { Button, Divider, Input, Select, Space } from "antd";
import { OPTIONS } from "./Constants";
import { PlusOutlined } from "@ant-design/icons";

const { Option } = Select;
export default class Test extends Component {
  state = {
    customOption: null,
    options: OPTIONS.shippingStages,
  };

//   handleChange = (Value) => {
//     if (
//       !this.state.options.some((item) =>
//         item.label.toLowerCase().includes(Value.toLowerCase())
//       )
//     ) {
//       this.setState({
//         options: [
//           ...this.state.options,
//           {
//             value: Value,
//             label: Value,
//           },
//         ],
//       });
//       // If the selected value is not in the current options, add it.
//       //   this.option = [...options, value];
//     }
//   };
  onSearch=(searchValue)=>{
    this.setState({customOption:searchValue})
  }
  addOptionItem = () => {{
      this.setState({
        options: [
          ...this.state.options,
          {
            value: this.state.customOption,
            label: this.state.customOption,
          },
        ],
      });
      // If the selected value is not in the current options, add it.
      //   this.option = [...options, value];
    }
  };
  render() {
    return (
      <Select
        showSearch
        style={{ width: "100%" }}
        placeholder="Select or enter an option"
        onSearch={this.onSearch}
        dropdownRender={(menu) => (
          <>
            {menu}
            <Divider
              style={{
                margin: "8px 0",
              }}
            />
            <Space
              style={{
                padding: "0 8px 4px",
              }}
            >
              <Input
                placeholder="Please enter item"
                // ref={inputRef}
                // value={name}
                onChange={(e) => this.setState({customOption:e.target.value})}
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
        {this.state.options.sort().map((item) => (
          <Option key={item.value} value={item.value}>
            {item.label}
          </Option>
        ))}
      </Select>
    );
  }
}
