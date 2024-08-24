// C:\Users\shali\Documents\shalin\test-app\src\components\ListViewContent.js
import React, {Component} from "react";
import ListHeader from "./ListHeader";
import ListRenderer from "swfrontend/MDM/MDMScreens/ListView//ListRenderer";
import ListFooter from "swfrontend/MDM/MDMScreens/ListView//ListFooter";

/**
 * List view content
 */

export default class ListViewContent extends Component {
    render() {
        return (
            <div className="col-md-12">
                <ListHeader {...this.props} />
                <ListRenderer {...this.props} />
                <ListFooter {...this.props} />
            </div>
        );
    }
}
