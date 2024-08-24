// C:\Users\shali\Documents\shalin\test-app\src\ScreenRouters.js

import React from "react";
import {Route, Switch} from "react-router-dom";
import LayTimeCalculator from "../src/Laytime/Screens/LayTimeCalculator";
import ListView from "../src/Laytime/Screens/ListView";
import MyResponsivePie from "../src/Laytime/Screens/DashBoard";

/**
 * Custom component mapping
 * @param {component} : Component being mapped
 * @param {routers} : Creating route for a component specified with route link
 */
function getRoutes() {
    return ({
        "Dashboard": {
            component: MyResponsivePie,
            routers: [
                <Switch>
                    <Route exact path={process.env.REACT_APP_PROJECT_ROUTE} component={MyResponsivePie}/>
                </Switch>
            ]
        },
        "LaytimeCalculator": {
            component: LayTimeCalculator, 
            routers: [<Switch>
                        <Route exact path={`${process.env.REACT_APP_PROJECT_ROUTE}/LaytimeCalculator`} component={ListView}/>
                        <Route exact path={`${process.env.REACT_APP_PROJECT_ROUTE}/LaytimeCalculator/new`} component={LayTimeCalculator}/>
                        <Route exact path={`${process.env.REACT_APP_PROJECT_ROUTE}/LaytimeCalculator/:id`} component={LayTimeCalculator}/>
            </Switch>],
            
        },
        "LaytimeApprovals": {
            component: LayTimeCalculator, 
            routers: [<Switch>
                        <Route exact path={`${process.env.REACT_APP_PROJECT_ROUTE}/LaytimeApprovals`} component={ListView}/>
                        {/* <Route exact path={`${process.env.REACT_APP_PROJECT_ROUTE}/LaytimeApprovals/new`} component={LayTimeCalculator}/> */}
                        <Route exact path={`${process.env.REACT_APP_PROJECT_ROUTE}/LaytimeApprovals/:id`} component={LayTimeCalculator}/>
            </Switch>],}
    })
}

export default getRoutes;