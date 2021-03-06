/* ===================================================
 * bootstrap-overflow-navs.js v0.3
 * ===================================================
 * Copyright 2012-13 Michael Langford, Evan Owens
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * ========================================================== */

+function ($) { "use strict";

	/**
	 * options:
	 *		more - translated "more" text
	 *		offset - width that needs to be subtracted from the parent div width
	 */
	$.fn.overflowNavs = function(options) {
		// Create a handle to our ul menu
		// @todo Implement some kind of check to make sure there is only one?  If we accidentally get more than one
		// then strange things happen
		var ul = $(this);
        
        // This should work with all navs, not just the navbar, so you should be able to pass a parent in
        var parent = options.parent ? options.parent : ul.parents('.navbar');
        
        // Check if it is a nvabar and twitter bootstrap collapse is in use
        var collapse = ul.parents('.navbar-collapse').hasClass('collapse');
		
        // Check if bootstrap navbar is collapsed (mobile)
        if(collapse) {
            var not_collapsed = ul.parents('.collapse').is(":visible");
        }
        else {
            var not_collapsed = true;
        }

		// Get width of the navbar parent so we know how much room we have to work with
		var parent_width = $(parent).width() - (options.offset ? parseInt(options.offset) : 0);

		// Find an already existing .overflow-nav dropdown
		var dropdown = $('li.overflow-nav', ul);
		// Create one if none exists
		if (! dropdown.length) {
			dropdown = $('<li class="overflow-nav dropdown"></li>');
			dropdown.append($('<a class="dropdown-toggle" data-toggle="dropdown" href="#">' + options.more + '<b class="caret"></b></a>'));
			dropdown.append($('<ul class="dropdown-menu"></ul>'));
		}

		// Window is shrinking
		if (ul.outerWidth() >= parent_width) {
        		// Loop through each non-dropdown li in the ul menu from right to left (using .get().reverse())
    			$($('li', ul).not('.dropdown').not('.dropdown li').get().reverse()).each(function() {
	                	if (not_collapsed && ul.outerWidth() >= parent_width) {
		                    // Remember the original width so that we can restore as the window grows
		                    $(this).attr('data-original-width', $(this).outerWidth());
		                    // Move the rightmost item to top of dropdown menu if we are running out of space
		                    dropdown.children('ul.dropdown-menu').prepend(this);
	                	}
	                	// @todo on shrinking resize some menu items are still in drop down when bootstrap mobile navigation is displaying
            		});
		}
		// Window is growing
		else {
			// We used to just look at the first one, but this doesn't work when the window is maximized
			//var dropdownFirstItem = dropdown.children('ul.dropdown-menu').children().first();
			dropdown.children('ul.dropdown-menu').children().each(function() {
				if (not_collapsed && ul.outerWidth()+parseInt($(this).attr('data-original-width')) < parent_width) {
					// Restore the topmost dropdown item to the main menu
					dropdown.before(this);
				}
				else {
					// If the topmost item can't be restored, don't look any further
					return false;
				}
			});
		}

		// Remove or add dropdown depending on whether or not it contains menu items
		if (! dropdown.children('ul.dropdown-menu').children().length) {
			dropdown.remove();
		}
		else {
			// Append new dropdown menu to main menu iff it doesn't already exist
			if (! ul.children('li.overflow-nav').length) {
				ul.append(dropdown);
			}
		}
	};

}(window.jQuery);