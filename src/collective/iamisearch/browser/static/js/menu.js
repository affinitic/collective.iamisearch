/* The following line defines global variables defined elsewhere. */
/*globals require*/


if(require === undefined){
  require = function(reqs, torun){
    'use strict';
    return torun(window.jQuery);
  };
}

require([
  'jquery',
], function($) {
  'use strict';




function hideAllMenus() {
    jQuery('dl.actionMenu').removeClass('activated').addClass('deactivated');
}

function toggleMenuHandler(event) {
    // swap between activated and deactivated
    jQuery(this).parents('.actionMenu:first')
        .toggleClass('deactivated')
        .toggleClass('activated');
    return false;
}

function actionMenuDocumentMouseDown(event) {
    if (jQuery(event.target).parents('.actionMenu:first').length) {
        // target is part of the menu, so just return and do the default
        return true;
    }

    hideAllMenus();
}

function actionMenuMouseOver(event) {
    var menu_id = jQuery(this).parents('.actionMenu:first').attr('id'),
        switch_menu;
    if (!menu_id) {return true;}

    switch_menu = jQuery('dl.actionMenu.activated').length > 0;
    jQuery('dl.actionMenu').removeClass('activated').addClass('deactivated');
    if (switch_menu) {
        jQuery('#' + menu_id).removeClass('deactivated').addClass('activated');
    }
}

function initializeMenus() {
    jQuery(document).mousedown(actionMenuDocumentMouseDown);

    hideAllMenus();

    // add toggle function to header links
    jQuery('dl.actionMenu dt.actionMenuHeader a')
        .click(toggleMenuHandler)
        .mouseover(actionMenuMouseOver);

    // add hide function to all links in the dropdown, so the dropdown closes
    // when any link is clicked
    jQuery('dl.actionMenu > dd.actionMenuContent').click(hideAllMenus);
}

jQuery(initializeMenus);

});
