/** @odoo-module **/

import { SearchPanel } from "@web/search/search_panel/search_panel";
import {patch} from "web.utils";


patch(SearchPanel.prototype, "runex_search_panel.RunexSearchPanel", {

 setup() {
   this._super.apply(this, arguments);
 },

 getValueName(value) {
        console.log(value.display_name);
        return value.display_name;
    },
});
