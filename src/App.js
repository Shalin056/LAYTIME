// C:\Users\shali\Documents\shalin\test-app\src\App.js

import React from "react";
import { BrowserRouter, Switch, Route } from "react-router-dom";
import MDMApp from "swfrontend/MDMApp";
import { localStorageVariableName } from "swfrontend/AppConfigs";
import LoginPage from "swfrontend/LOGIN/LoginPage";
import getRoutes from "./ScreenRouters";
import "./App.css";
import NoFormApproval from "./components/ApprovalForm";


const App = () => {

  return window.location.pathname.includes("ApprovalForm") ?
    <BrowserRouter>
      <Switch>
        <Route exact path={`${process.env.REACT_APP_PROJECT_ROUTE}/ApprovalForm/:hash`} component={NoFormApproval}/>
      </Switch>
    </BrowserRouter> :
      localStorage.getItem(localStorageVariableName.authToken) == null ? (
        <LoginPage />
      ) : (
        <BrowserRouter>
          <MDMApp routes={getRoutes} />
        </BrowserRouter>
      )
};

export default App;
