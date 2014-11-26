/*
 * Ebtest
 * 
 *
 * Copyright (c) 2014 Trapeze
  */

(function () {
    var global = this;


    // Initial setup
    // =============

    // Map dependancies to local variables
    var _       = global._;
    var $       = global.jQuery;


    // Constructor
    // ===========

    var Trapeze = (global.Trapeze || (global.Trapeze = { }));

    var Core = Trapeze.Core = function (options) {
        var defaults = { };

        this.config         = $.extend(true, defaults, options || { });

        this._initialize();
    };


    // Initialization
    // ==============

    Core.prototype._initialize = function () {
        this._registerInstanceVars();
        this._initializePage();
    };

    Core.prototype._registerInstanceVars = function () {
    };

    Core.prototype._initializePage = function () {
        var classnames  = $('body').prop('class').split(' ');
        var index       = classnames.length;

        if (index > 1) {
            while(index--) {
                switch (classnames[index]) {
                    case 'home-page':
                    case 'detail-page':
                        // Execute page specific javascript
                        break;

                    case 'contact-page':
                        break;
                }
            }
        }
    };


}).call(this);
