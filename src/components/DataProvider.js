// C:\Users\shali\Documents\shalin\test-app\src\components\DataProvider.js

import apiHelper from '../Utils/ApiHelper.js'
import { API_URLS, METHOD_GET, METHOD_PATCH, METHOD_POST, METHOD_DELETE } from './Constants';

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

export const fetchShippingDetail = async (id) => {
  const model_name = 'shipping_detail';
  try {
    return await apiHelper(API_URLS.SHIPPING_DETAIL(model_name, id), METHOD_GET, {});
  } catch (error) {
    console.error("Failed to fetch shipping detail:", error);
    throw error;
  }
};

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

export const addOrUpdateShippingDetail = async (shippingDetail, id) => {
    try {
        const apiUrl = id ? API_URLS.SHIPPING_DETAIL('shipping_detail', id) : API_URLS.CREATE;
        const method = id ? METHOD_PATCH : METHOD_POST;

        return await apiHelper(apiUrl, method, { shipping_detail: shippingDetail });
    } catch (error) {
        console.error("Failed to add/update shipping detail:", error);
        throw error;
    }
};

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

export const navigateToLaytimeCalculator = (history, method) => {
    try {
        if (method === METHOD_POST) {
            history.push(process.env.REACT_APP_PROJECT_ROUTE + "/LaytimeCalculator");
        }
    } catch (error) {
        console.error("Failed to navigate to Laytime Calculator:", error);
        throw error;
    }
};

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

export const exportToExcel = async (rowData) => {
  try {
    return apiHelper(API_URLS.FORM_EXCEL_EXPORT, METHOD_POST, rowData);
  } catch (error) {
    console.error('Error exporting data:', error);
    throw error;
  }
};
  
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

export const getCalculateTime = async (shipping_detail, stages, otherData) => {
  try {
    return await apiHelper(API_URLS.CALCULATE_TIME, METHOD_POST, { shipping_detail, stages, otherData });
  } catch (error) {
    console.error("Failed to calculate time:", error);
    throw error;
  }
};

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

export const showApprovalButton = async (app, model, id) => {
    try {
      const response = await apiHelper(API_URLS.SHOW_APPROVAL_BUTTON(app, model, id), METHOD_GET);
      return response;
    } catch (error) {
      console.error('Error fetching data:', error);
      throw error;
    }
  };

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

export const getIndicateApprovalType = async (app, model, id) => {
  try {
    return await apiHelper(API_URLS.GET_INDICATE_APPROVAL_TYPE(app, model, id), METHOD_GET);
  } catch (error) {
    console.error("Failed to get indicate approval type:", error);
    throw error;
  }
};

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

export const getGridData = async (values) => {

    try {
        return await apiHelper(API_URLS.LIST(values).replace('${values}', values), METHOD_GET);
    } catch (error) {
        console.error('Error fetching grid data:', error);
        throw error;
    }
};

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

export const deleteShippingDetail = async (model_name, listItems) => {
    try {
        return await apiHelper(API_URLS.DETAILS(model_name), METHOD_DELETE, { items: listItems });
    } catch (error) {
        console.error('Error deleting item(s):', error);
    }
};

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

export const exportExcelData = async (data) => {
    try {
      return apiHelper (API_URLS.EXCEL_EXPORT, METHOD_POST, data);
    } catch (error) {
      console.error('Error exporting data:', error);
      throw error;
    }
  };

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

export const getAllowedTime = async (data) => {
    try {
      return await apiHelper(API_URLS.CALCULATE_ALLOWED_TIME, METHOD_POST, data);
    } catch (error) {
      console.error('Error exporting data:', error);
      throw error;
    }
  };

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

export const initiateWorkflow = async (id) => {
  try {
      const url = API_URLS.INITIATE_APPROVAL(id);
      const method = METHOD_POST;
      return await apiHelper(url, method, {});
  } catch (error) {
      console.error('Error initiating workflow:', error);
      throw error;
  }
};

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

export const getDashData = async () => {
  try {
    return await apiHelper(API_URLS.DASHBOARD, METHOD_GET, null);
  } catch (error) {
    console.error('Error exporting data:', error);
    throw error;
  }
};

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

export const getPdfData = async (id) => {
  const model_name = 'shipping_detail';
  try {
    return await apiHelper(API_URLS.PDF(model_name, id), METHOD_GET, {});
  } catch (error) {
    console.error("Failed to fetch shipping detail:", error);
    throw error;
  }
};

////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

export const multipleApproval = async (bulkData) => {
  try {
      return await apiHelper(API_URLS.BULK_APPROVAL, METHOD_POST, bulkData);
  } catch (error) {
      console.error('Error deleting item(s):', error);
  }
};