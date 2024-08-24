// C:\Users\shali\Documents\shalin\test-app\src\Utils\ApiHelper.js

import getCookie from "swfrontend/COMS/Utils/cookies.js";

const apiHelper = async (url, method, body) => {

    const csrf_token = getCookie(`${process.env.REACT_APP_TOKEN_PREFIX}-csrftoken`);
    const authToken = JSON.parse(localStorage.getItem(`${process.env.REACT_APP_TOKEN_PREFIX}-auth-token`));
    const approvalAuthorization = localStorage.getItem("approval-authorization");

    let fetchOptions = {
        method: method,
        headers: {
            "Content-Type": "application/json",
            'X-CSRFToken': csrf_token,
            "Authorization": authToken,
            "Approval-Authorization": approvalAuthorization,
        }
    };

    if (method !== 'GET' && body) {
        fetchOptions.body = JSON.stringify(body);
    }

    try {
        const response = await fetch(url, fetchOptions);

        if (response.ok) {
            return response
        } else {
            throw new Error("API request failed");
        }
    } catch (error) {
        console.error("API request error:", error);
        throw error;
    }
};

export default apiHelper;
