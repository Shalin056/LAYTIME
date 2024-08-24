// 8th sem\Laytime\venv\laytime_frontend\src\components\Commons\CustomLoader.js

import React from "react";
import "./CustomLoader.css";
import { Modal } from "antd";

export default function LoadingSpinner() {
  return (
    <div className="spinner-container">
      <div className="loading-box">
        <div className="loading-spinner"></div>
        <div className="loading-text">Please Wait</div>
      </div>
    </div>
    
  );
}
