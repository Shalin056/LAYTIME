// C:\Users\shali\Documents\shalin\test-app\src\components\Constants.js

import {notification } from "antd";

export const OPTIONS = {
  shippingStages: [
    {
      value: "NOR Tendered / 12 HRS TT / Shifting time NTC",
      label: "NOR Tendered / 12 HRS TT / Shifting time NTC",
    },
    {
      value: "VSL Berthed at Berth NO. 1 TNTC",
      label: "VSL Berthed at Berth NO. 1 TNTC",
    },
    {
      value: "Initial draft survey completed TNTC",
      label: "Initial draft survey completed TNTC",
    },
    {
      value: "Discharging commenced",
      label: "Discharging commenced",
    },
    {
      value: "Discharging",
      label: "Discharging",
    },
    {
      value: "Discharging completed / Laytime to cease",
      label: "Discharging completed / Laytime to cease",
    },
    {
      value: "Final draft survey completed TNTC",
      label: "Final draft survey completed TNTC",
    },
    {
      value: "VSL Sailed",
      label: "VSL Sailed",
    },
    {
      value: "Waiting for loading",
      label: "Waiting for loading",
    },
    {
      value: "Waiting for discharging",
      label: "Waiting for discharging",
    },
    {
      value: "Waiting for berth",
      label: "Waiting for berth",
    },
    {
      value: "VSL waited at anchorage due to berth congestion",
      label: "VSL waited at anchorage due to berth congestion",
    },

    {
      value: "Gangway lowered",
      label: "Gangway lowered",
    },
    {
      value: "Customs cleared",
      label: "Customs cleared",
    },

    {
      value: "Waiting for tide",
      label: "Waiting for tide",
    },
    {
      value: "No work due to heavy fog/poor visibility",
      label: "No work due to heavy fog/poor visibility",
    },
    {
      value: "Rain delay",
      label: "Rain delay",
    },
    {
      value: "No work due to strong wind and rain",
      label: "No work due to strong wind and rain",
    },
    {
      value: "Tea break/FHEX",
      label: "Tea break/FHEX",
    },
    {
      value: "Prayer break/FHEX",
      label: "Prayer break/FHEX",
    },
    {
      value: "Dinner break/FHEX",
      label: "Dinner break/FHEX",
    },
    {
      value: "Initial draft survey NTC",
      label: "Initial draft survey NTC",
    },
    {
      value: "Intermediate draft survey NTC",
      label: "Intermediate draft survey NTC",
    },
    {
      value: "Final draft survey NTC",
      label: "Final draft survey NTC",
    },
  ],

  ports: [
    {
      value: "Hazira",
      label: "Hazira",
    },
    {
      value: "Vizag",
      label: "Vizag",
    },
    {
      value: "Paradip",
      label: "Paradip",
    },
  ],
};   

export const DETAIL = [
  //shipping detail columns
  {headerName: "id", field: "id", type: "text", headerCheckboxSelection: true, checkboxSelection: true, primarykeyfield: "id"},
  {headerName: "Vessel", field: "vessel", type: "text",},
  {headerName: "Created_by", field: "created_by", type: "text",},
  {headerName: "last_updated_by", field: "last_updated_by", type: "text",},
  {headerName: "Bl Date", field: "bl_date", type: "text"},
  {headerName: "commenced_loading_time", field: "commenced_loading_time", type: "text"},
  {headerName: "completed_loading_time", field: "completed_loading_time", type: "text"},
  {headerName: "Created Date", field: "created_date", type: "text"},
  {headerName: "Updated Date", field: "last_updated_date", type: "text"},
  {headerName: "Amount", field: 'laytime_calculator.amount', type: 'text'},
  {headerName: "Actual Time", field: 'laytime_calculator.actual_time', type: 'text'}, 
  {headerName: "Allowed Time", field: 'laytime_calculator.allowed_time', type: 'text'},
  {headerName: "Total Time Difference", field: 'laytime_calculator.total_time_difference', type: 'text'}, 
  {headerName: "Is Time Saved", field: 'laytime_calculator.is_time_saved', type: 'text'}, 
  // {field: "last_updated_date", type: "text"},
  // {field: "is_deleted", type: "text"},

  //shipping stage detail columns
  {field: 'shipping_detail', type: 'text'},
  {field: 'count', type: 'text'}, 
  {field: 'stage_name', type: 'text'}, 
  {field: 'start_date_time', type: 'text'}, 
  {field: 'end_date_time', type: 'text'},
  {field: 'is_deleted', type: 'text'}, 

  //split quantity columns
  {field: 'shipping_detail', type: 'text'},
  {field: 'port_name', type: 'text'}, 
  {field: 'cargo_quantity', type: 'text'},
  {field: 'amount', type: 'text'}, 
  {field: 'remaining_cargo_qty', type: 'text'}, 
  {field: 'is_deleted', type: 'text'}, 

  //laytime calculator columns
  {field: 'shipping_detail', type: 'text'},
  {field: 'amount', type: 'text'},
  {field: 'actual_time', type: 'text'},
  {field: 'allowed_time', type: 'text'}, 
  {field: 'total_time_difference', type: 'text'},
  {field: 'is_time_saved', type: 'text'}, 
  {field: 'is_deleted', type: 'text'}, 
]

export const SHIP_DETAIL = [
  {headerName: "Id", field: "id", type: "text", headerCheckboxSelection: true, checkboxSelection: true, primarykeyfield: "id", cellStyle: function (params) {
    return {
      color: "blue",
      "text-decoration": "underline",
    };
  },
  cellRendererFramework: (params) => {
    return (
      <a
        onClick={() =>
          params.context.editField1(params)
        }
      >
        {params.value}
      </a>
    );
  },},
  // {headerName: "Status", field: "status", type: "text", headerAlign: "center"},
  {headerName: "Status",
  field: "status",
  type: "text",
  headerAlign: "center",
  valueFormatter: params => {
    const status = params.value;
    return (status !== 'Draft' && status !== 'Approved' && status !== 'Rejected') ? `Pending from ${status}` : status;
  }},
  {headerName: "Vessel", field: "vessel", type: "text"},
  {headerName: "Created Date", field: "created_date", type: "text"},
  {headerName: "Created by", field: "created_by", type: "text", },
  {headerName: "Bl Date", field: "bl_date", type: "text"},
  {headerName: "Rate Type", field: "rate_type", type: "text"},
  {headerName: "Commenced Time", field: "commenced_loading_time", type: "text"},
  {headerName: "Completed Time", field: "completed_loading_time", type: "text"},
  {headerName: "Amount (USD $)", field: 'laytime_calculator.amount', type: 'text'}, 
  {headerName: "Actual Time (days)", field: 'laytime_calculator.actual_time', type: 'text'}, 
  {headerName: "Allowed Time (days)", field: 'laytime_calculator.allowed_time', type: 'text'},
  {headerName: "Total Time Difference (days)", field: 'laytime_calculator.total_time_difference', type: 'text'}, 
  {headerName: "Is Time Saved", field: 'laytime_calculator.is_time_saved', type: 'text', valueFormatter: (params) => params.value ? 'Yes' : 'No',}, 
  {
    headerName: 'Stage Name',
    field: 'stages',
    type: 'text',
    cellRenderer: function (params) {
        return params.data.stages.map(stage => `${stage.stage_name}`).join(', ');
    }
  },
  {
    headerName: 'Stages: start_date_time and end_date_time',
    field: 'stages',
    type: 'text',
    cellRenderer: function (params) {
        return params.data.stages.map(stage => `(${stage.start_date_time} to ${stage.end_date_time})`).join(', ');
    }
  },
  {
    headerName: 'Stages: percentage',
    field: 'stages',
    type: 'text',
    cellRenderer: function (params) {
        return params.data.stages.map(stage => `(${stage.percentage})`).join(', ');
    }
  },
  {
    headerName: 'Split Quantities: Port name',
    field: 'split_quantities',
    type: 'text',
    cellRenderer: function (params) {
        return params.data.split_quantities.map(split => `${split.port_name}`).join(', ');
    }
  },
  {
    headerName: 'Split Quantities: Cargo Quantity',
    field: 'split_quantities',
    type: 'text',
    cellRenderer: function (params) {
        return params.data.split_quantities.map(split => `Cargo Quantity: ${split.cargo_quantity}`).join(', ');
    }
  },
  {
    headerName: 'Download PDF',
    field: '',
    type: 'text',
    pinned: 'right',
    cellRendererFramework: function (params) {
      return <p onClick={() => {
        params.context.handleDownloadPDF(params.data.id);
      }} style={{color: '#1890ff', cursor: 'pointer', textAlign:'center'}}>
        Download PDF
      </p>
    },
  },
]

export const PORTS = {
  "Hazira" : "Hazira",
  "Vizag" : "Vizag",
  "Paradip" : "Paradip",
}

export const openNotification = (type, message, description) => {
  notification[type]({
    message,
    description,
    duration: 2,
  });
};

export const BASE_URL = `${process.env.REACT_APP_SERVER_PROTOCOL}://${process.env.REACT_APP_SERVER_URL}:${process.env.REACT_APP_SERVER_PORT}`;

export const API_URLS = {
  SHIPPING_DETAIL: (model_name, id) => `${BASE_URL}/LAYTIME_UAT_API/laytime/detail/${model_name}/${id}/`,
  DETAILS: (model_name) => `${BASE_URL}/LAYTIME_UAT_API/laytime/detail/${model_name}/`,
  LIST: (values) => `${BASE_URL}/LAYTIME_UAT_API/laytime/list/${values}`,
  SHOW_APPROVAL_BUTTON: (app, model, id) => `${BASE_URL}/LAYTIME_UAT_API/workflow/to-show-approval-button/${app}.${model}?id=${id}`,
  INITIATE_APPROVAL: (id) => `${BASE_URL}/LAYTIME_UAT_API/laytime/initiate-approval/${id}/`,
  PDF: (model_name, id) => `${BASE_URL}/LAYTIME_UAT_API/laytime/pdf/${model_name}/${id}/`,

  CREATE: `${BASE_URL}/LAYTIME_UAT_API/laytime/create/`,
  CALCULATE_TIME: `${BASE_URL}/LAYTIME_UAT_API/laytime/calculate-time/`,
  FORM_EXCEL_EXPORT: `${BASE_URL}/LAYTIME_UAT_API/laytime/form-excel-export/`,
  EXCEL_EXPORT: `${BASE_URL}/LAYTIME_UAT_API/master/laytime_details.ShippingDetail/export`,
  CALCULATE_ALLOWED_TIME: `${BASE_URL}/LAYTIME_UAT_API/laytime/calculate-allowed-time/`,
  DASHBOARD:`${BASE_URL}/LAYTIME_UAT_API/laytime/dashboard/`,
  BULK_APPROVAL: `${BASE_URL}/LAYTIME_UAT_API/laytime/bulkApproval/`,
  
  // EXCEL_EXPORT: `${BASE_URL}/laytime/api/excel-export/`,
};

export const METHOD_PUT = "PUT";
export const METHOD_POST = "POST";
export const METHOD_GET = "GET";
export const METHOD_PATCH = "PATCH";
export const METHOD_DELETE = "DELETE";
export const METHOD_OPTIONS = "OPTIONS";
