/**
 * @desc jQuery plugin to sort html list also the tree structures
 * @author Vladimír Čamaj
 * @license MIT
 */

( function( $ )
{

    /**
     * @desc jQuery plugin
     * @param options
     * @returns this to unsure chaining
     */
    $.fn.sortableLists = function( options )
    {
        // Local variables. This scope is available for all the functions in this closure.
        var jQBody = $( 'body' ).css( 'position', 'relative' ),

            defaults = {
                currElClass: '',
                placeholderClass: '',
                placeholderCss: {
                    'position': 'relative',
                    'padding': 0
                },
                hintClass: '',
                hintCss: {
                    'display': 'none',
                    'position': 'relative',
                    'padding': 0
                },
                hintWrapperClass: '',
                hintWrapperCss: { /* Description is below the defaults in this var section */ },
                baseClass: '',
                baseCss: {
                    'position': 'absolute',
                    'top': 0 - parseInt( jQBody.css( 'margin-top' ) ),
                    'left': 0 - parseInt( jQBody.css( 'margin-left' ) ),
                    'margin': 0,
                    'padding': 0,
                    'z-index': 2500
                },
                opener: {
                    active: false,
                    open: '',
                    close: '',
                    openerCss: {
                        'float': 'left',
                        'display': 'inline-block',
                        'background-position': 'center center',
                        'background-repeat': 'no-repeat'
                    },
                    openerClass: ''
                },
                maxLevels: false,
                listSelector: 'ul',
                listsClass: '', // Used for hintWrapper and baseElement
                listsCss: {},
                insertZone: 50,
                insertZonePlus: false,
                scroll: 20,
                ignoreClass: '',
                isAllowed: function( cEl, hint, target ) { return true; },  // Params: current el., hint el.
                onDragStart: function( e, cEl ) { return true; },  // Params: e jQ. event obj., current el.
                onChange: function( cEl ) { return true; },  // Params: current el.
                complete: function( cEl ) { return true; }  // Params: current el.
            },

            setting = $.extend( true, {}, defaults, options ),

            // base element from which is counted position of draged element
            base = $( '<' + setting.listSelector + ' />' )
                .prependTo( jQBody )
                .attr( 'id', 's-l-base' )
                .css( setting.baseCss )
                .addClass( setting.listsClass + ' ' + setting.baseClass ),

            // placeholder != state.placeholderNode
            // placeholder is document fragment and state.placeholderNode is document node
            placeholder = $( '<li />' )
                .attr( 'id', 's-l-placeholder' )
                .css( setting.placeholderCss )
                .addClass( setting.placeholderClass ),

            // hint is document fragment
            hint = $( '<li />' )
                .attr( 'id', 's-l-hint' )
                .css( setting.hintCss )
                .addClass( setting.hintClass ),

            // Is document fragment used as wrapper if hint is inserted to the empty li
            hintWrapper = $( '<' + setting.listSelector + ' />' )
                .attr( 'id', 's-l-hint-wrapper' )
                .addClass( setting.listsClass + ' ' + setting.hintWrapperClass )
                .css( setting.listsCss )
                .css( setting.hintWrapperCss ),

            // Is +/- ikon to open/close nested lists
            opener = $( '<span />' )
                .addClass( 's-l-opener ' + setting.opener.openerClass )
                .css( setting.opener.openerCss )
                .on( 'mousedown', function( e )
                {
                    var li = $( this ).closest( 'li' );

                    if ( li.hasClass( 's-l-closed' ) )
                    {
                        open( li );
                    }
                    else
                    {
                        close( li );
                    }

                    return false; // Prevent default
                } );

        if ( setting.opener.as == 'class' )
        {
            opener.addClass( setting.opener.close );
        }
        else if ( setting.opener.as == 'html' )
        {
            opener.html( setting.opener.close );
        }
        else
        {
            console.error( 'jQuerySortableLists opener as background image has been removed with release 2.0.0. Use html instead please.' );
        }

        // Container with all actual elements and parameters
        var state = {
            isDragged: false,
            isRelEFP: null,  // How browser counts elementFromPoint() position (relative to window/document)
            oEl: null, // overElement is element which returns elementFromPoint() method
            rootEl: {
                el: $( this ),
                offset: null,
                rootElClass: $( this ).attr( 'class' )
            },
            cEl: null, // currentElement is currently dragged element
            placeholderParentLi: null,
            upScroll: false,
            downScroll: false,
            pX: 0,
            pY: 0,
            cX: 0,
            cY: 0,
            isAllowed: true, // The function is defined in setting
            e: { pageX: 0, pageY: 0, clientX: 0, clientY: 0 }, // TODO: unused??
            doc: $( document ),
            win: $( window )
        };

        if ( setting.opener.active )
        {
            if ( ! setting.opener.open ) throw 'Opener.open value is not defined. It should be valid url, html or css class.';
            if ( ! setting.opener.close ) throw 'Opener.close value is not defined. It should be valid url, html or css class.';

            $( this ).find( 'li' ).each( function()
            {
                var li = $( this );

                if ( li.children( setting.listSelector ).length )
                {
                    opener.clone( true ).prependTo( li.children( 'div' ).first() );

                    if ( ! li.hasClass( 's-l-open' ) )
                    {
                        close( li );
                    }
                    else
                    {
                        open( li );
                    }
                }
            } );
        }

        if( setting.maxLevels !== false )
        {
            if( isNaN( setting.maxLevels ) ) throw 'JQuery-sortable-lists maxLevels values is not a number';

            $( this ).find( 'li' ).each( function()
            {
                var insideLevs = getInsideLevels( $(this) );
                var upperLevs = getUpperLevels( $(this) );
                setInsideLevels( $(this), insideLevs );
                setUpperLevels( $(this), upperLevs );
            });
        }

        // Return this ensures chaining
        return this.on( 'mousedown', function( e )
            {
                var target = $( e.target );

                if ( state.isDragged !== false || ( setting.ignoreClass && target.closest( '.' + setting.ignoreClass ).length ) ) return; // setting.ignoreClass is checked cause hasClass('') returns true

                // Solves selection/range highlighting
                e.preventDefault();

                // El must be li in jQuery object
                var el = target.closest( 'li' ),
                    rEl = $( this );

                // Check if el is not empty
                if ( el[0] )
                {
                    setting.onDragStart( e, el );
                    startDrag( e, el, rEl );
                }
            }
        );

        /**
         * @desc Binds events dragging and endDrag, sets some init. values
         * @param e event obj.
         * @param el curr. dragged element
         * @param rEl root element
         */
        function startDrag( e, el, rEl )
        {
            state.isDragged = true;

            var elMT = parseInt( el.css( 'margin-top' ) ), // parseInt is necesary cause value has px at the end
                elMB = parseInt( el.css( 'margin-bottom' ) ),
                elML = parseInt( el.css( 'margin-left' ) ),
                elMR = parseInt( el.css( 'margin-right' ) ),
                elXY = el.offset(),
                elIH = el.innerHeight();

            state.rootEl = {
                el: rEl,
                offset: rEl.offset(),
                rootElClass: rEl.attr( 'class' )
            };

            state.cEl = {
                el: el,
                mT: elMT, mL: elML, mB: elMB, mR: elMR,
                offset: elXY
            };

            state.cEl.xyOffsetDiff = { X: e.pageX - state.cEl.offset.left, Y: e.pageY - state.cEl.offset.top };
            state.cEl.el.addClass( 's-l-current ' + setting.currElClass );

            el.before( placeholder );  // Now document has node placeholder

            var placeholderNode = state.placeholderNode = $( '#s-l-placeholder' );  // jQuery object && document node

            el.css( {
                'width': el.width(),
                'position': 'absolute',
                'top': elXY.top - elMT,
                'left': elXY.left - elML
            } ).prependTo( base );

            placeholderNode.css( {
                'display': 'block',
                'height': elIH
            } );

            hint.css( 'height', elIH );

            state.doc
                .on( 'mousemove', dragging )
                .on( 'mouseup', endDrag );
        }

        /**
         * @desc Start dragging
         * @param e event obj.
         */
        function dragging( e )
        {
            if ( state.isDragged )
            {
                var cEl = state.cEl,
                    doc = state.doc,
                    win = state.win;

                // event triggered by trigger() from setInterval does not have XY properties
                if ( ! e.pageX )
                {
                    setEventPos( e );
                }

                // Scrolling up
                if ( doc.scrollTop() > state.rootEl.offset.top - 10 && e.clientY < 50 )
                {
                    if ( ! state.upScroll ) // Has to be here after cond. e.clientY < 50 cause else unsets the interval
                    {
                        setScrollUp( e );
                    }
                    else
                    {
                        e.pageY = e.pageY - setting.scroll;
                        $( 'html, body' ).each( function( i )
                        {
                            $( this ).scrollTop( $( this ).scrollTop() - setting.scroll );
                        } );
                        setCursorPos( e );
                    }
                }
                // Scrolling down
                else if ( doc.scrollTop() + win.height() < state.rootEl.offset.top + state.rootEl.el.outerHeight( false ) + 10 && win.height() - e.clientY < 50 )
                {
                    if ( ! state.downScroll )
                    {
                        setScrollDown( e );
                    }
                    else
                    {
                        e.pageY = e.pageY + setting.scroll;
                        $( 'html, body' ).each( function( i )
                        {
                            $( this ).scrollTop( $( this ).scrollTop() + setting.scroll );
                        } );
                        setCursorPos( e );
                    }
                }
                else
                {
                    scrollStop( state );
                }

                // Script needs to know old oEl
                state.oElOld = state.oEl;

                cEl.el[0].style.visibility = 'hidden';  // This is important for the next row
                state.oEl = oEl = elFromPoint( e.pageX, e.pageY );
                cEl.el[0].style.visibility = 'visible';

                showHint( e, state );

                setCElPos( e, state );
            }
        }

        /**
         * @desc endDrag unbinds events mousemove/mouseup and removes redundant elements
         * @param e
         */
        function endDrag( e )
        {
            var cEl = state.cEl,
                hintNode = $( '#s-l-hint', state.rootEl.el ),
                hintStyle = hint[0].style,
                targetEl = null, // hintNode/placeholderNode
                isHintTarget = false, // if cEl will be placed to the hintNode
                hintWrapperNode = $( '#s-l-hint-wrapper' );

            if ( hintStyle.display == 'block' && hintNode.length && state.isAllowed )
            {
                targetEl = hintNode;
                isHintTarget = true;
            }
            else
            {
                targetEl = state.placeholderNode;
                isHintTarget = false;
            }

            offset = targetEl.offset();

            cEl.el.animate( { left: offset.left - state.cEl.mL, top: offset.top - state.cEl.mT }, 250,
                function()  // complete callback
                {
                    tidyCurrEl( cEl );

                    targetEl.after( cEl.el[0] );
                    targetEl[0].style.display = 'none';
                    hintStyle.display = 'none';
                    // This has to be document node, not hint as a part of documentFragment.
                    hintNode.remove();

                    hintWrapperNode
                        .removeAttr( 'id' )
                        .removeClass( setting.hintWrapperClass );

                    if ( hintWrapperNode.length )
                    {
                        hintWrapperNode.prev( 'div' ).append( opener.clone( true ) );
                    }

                    // Directly removed placeholder looks bad. It jumps up if the hint is below.
                    if ( isHintTarget )
                    {
                        // !!! Do not use local var cause it seems it creates a closure variables lakes in Chrome !!!
                        state.placeholderNode.slideUp( 150, function()
                        {
                            state.placeholderParentLi = ( ! state.placeholderNode.parent().is( state.rootEl.el ) ) ? state.placeholderNode.parent().closest( 'li' ) : null;

                            state.placeholderNode.remove();
                            tidyEmptyLists();

                            setting.onChange( cEl.el );
                            setting.complete( cEl.el ); // Have to be here cause is necessary to remove placeholder before complete call.
                            state.isDragged = false;

                            if( setting.maxLevels !== false )  // Has to be after placeholder remove.
                            {
                                recountLevels( cEl.el );
                                if( state.placeholderParentLi ) recountLevels( state.placeholderParentLi );
                            }
                        });
                    }
                    else
                    {
                        state.placeholderNode.remove();
                        tidyEmptyLists();
                        setting.complete( cEl.el );
                        state.isDragged = false;
                    }

                } );

            scrollStop( state );

            state.doc
                .unbind( "mousemove", dragging )
                .unbind( "mouseup", endDrag );
        }

        //////////////////////////////////////////////////////////////////////////////////////////////////////
        ////////Helpers///////////////////////////////////////////////////////////////////////////////////////
        //////////////////////////////////////////////////////////////////////////////////////////////////////

        //////// Scroll handlers /////////////////////////////////////////////////////////////////////////////

        /**
         * @desc Ensures autoscroll up.
         * @param e
         * @return No value
         */
        function setScrollUp( e )
        {
            if ( state.upScroll ) return;

            state.upScroll = setInterval( function()
            {
                state.doc.trigger( 'mousemove' );
            }, 50 );
        }

        /**
         * @desc Ensures autoscroll down.
         * @param e
         * @return No value
         */
        function setScrollDown( e )
        {
            if ( state.downScroll ) return;

            state.downScroll = setInterval( function()
            {
                state.doc.trigger( 'mousemove' );
            }, 50 );
        }

        /**
         * @desc This properties are used when setScrollUp()/Down() calls trigger('mousemove'), cause trigger() produce event object without pageY/Y and clientX/Y.
         * @param e
         * @return No value
         */
        function setCursorPos( e )
        {
            state.pY = e.pageY;
            state.pX = e.pageX;
            state.cY = e.clientY;
            state.cX = e.clientX;
        }

        /**
         * @desc Necessary while scrolling, cause trigger('mousemove') does not set cursor XY values in event object
         * @param e
         * @return No value
         */
        function setEventPos( e )
        {
            e.pageY = state.pY;
            e.pageX = state.pX;
            e.clientY = state.cY;
            e.clientX = state.cX;

        }

        /**
         * @desc Stops scrolling and sets variables
         * @param state
         * @return No value
         */
        function scrollStop( state )
        {
            clearInterval( state.upScroll );
            clearInterval( state.downScroll );
            // clearInterval have to be before upScroll/downScroll is set to false
            state.upScroll = state.downScroll = false;
        }

        /////// End of Scroll handlers //////////////////////////////////////////////////////////////
        /////// Current element handlers //////////////////////////////////////////////////////////////

        /**
         * @desc Sets the position of dragged element
         * @param e event object
         * @param state state object
         * @return No value
         */
        function setCElPos( e, state )
        {
            var cEl = state.cEl;

            cEl.el.css( {
                'top': e.pageY - cEl.xyOffsetDiff.Y - cEl.mT,
                'left': e.pageX - cEl.xyOffsetDiff.X - cEl.mL
            } );
        }

        /**
         * @desc Return elementFromPoint() result as jQuery object
         * @param x e.pageX
         * @param y e.pageY
         * @return null|jQuery object
         */
        function elFromPoint( x, y )
        {
            if ( ! document.elementFromPoint ) return null;

            // FF/IE/CH needs coordinates relative to the window, unlike
            // Opera/Safari which needs absolute coordinates of document in elementFromPoint()
            var isRelEFP = state.isRelEFP;

            // isRelative === null means it is not checked yet
            if ( isRelEFP === null )
            {
                var s, res;
                if ( (s = state.doc.scrollTop()) > 0 )
                {
                    isRelEFP = ( (res = document.elementFromPoint( 0, s + $( window ).height() - 1 ) ) == null
                    || res.tagName.toUpperCase() == 'HTML');  // IE8 returns html
                }
                if ( (s = state.doc.scrollLeft()) > 0 )
                {
                    isRelEFP = ( (res = document.elementFromPoint( s + $( window ).width() - 1, 0 ) ) == null
                    || res.tagName.toUpperCase() == 'HTML');  // IE8 returns html
                }
            }

            if ( isRelEFP )
            {
                x -= state.doc.scrollLeft();
                y -= state.doc.scrollTop();
            }

            // Returns jQuery object
            var el = $( document.elementFromPoint( x, y ) );

            if ( ! state.rootEl.el.find( el ).length ) // el is outside the rootEl
            {
                return null;
            }
            else if ( el.is( '#s-l-placeholder' ) || el.is( '#s-l-hint' ) ) // el is #placeholder/#hint
            {
                return null;
            }
            else if ( ! el.is( 'li' ) ) // el is ul or div or something else in li elem.
            {
                el = el.closest( 'li' );
                return el[0] ? el : null;
            }
            else if ( el.is( 'li' ) ) // el is most wanted li
            {
                return el;
            }
        }

        //////// End of current element handlers //////////////////////////////////////////////////////
        //////// Show hint handlers //////////////////////////////////////////////////////

        /**
         * @desc Shows or hides or does not show hint element
         * @param e event
         * @param state
         * @return No value
         */
        function showHint( e, state )
        {
            var oEl = state.oEl;

            // If oEl is null or if this is the first call in dragging
            if ( ! oEl || ! state.oElOld )  return;

            var oElH = oEl.outerHeight( false ),
                relY = e.pageY - oEl.offset().top;

            if ( setting.insertZonePlus )
            {
                if ( 14 > relY )  // Inserting on top
                {
                    showOnTopPlus( e, oEl, 7 > relY );  // Last bool param express if hint insert outside/inside
                }
                else if ( oElH - 14 < relY )  // Inserting on bottom
                {
                    showOnBottomPlus( e, oEl, oElH - 7 < relY );
                }
            }
            else
            {
                if ( 5 > relY )  // Inserting on top
                {
                    showOnTop( e, oEl );
                }
                else if ( oElH - 5 < relY )  // Inserting on bottom
                {
                    showOnBottom( e, oEl );
                }
            }
        }

        /**
         * @desc Called from showHint method. Displays or hides hint element
         * @param e event
         * @param oEl oElement
         * @return No value
         */
        function showOnTop( e, oEl )
        {
            if ( $( '#s-l-hint-wrapper', state.rootEl.el ).length )
            {
                hint.unwrap();  // If hint is wrapped by ul/ol #s-l-hint-wrapper
            }

            // Hint outside the oEl
            if ( e.pageX - oEl.offset().left < setting.insertZone )
            {
                // Ensure display:none if hint will be next to the placeholder
                if ( (oEl.prev( '#s-l-placeholder' ).length) || (setting.maxLevels !== false && ! checkMaxLevels( false )) )
                {
                    hint.css( 'display', 'none' );
                    return;
                }
                oEl.before( hint );
            }
            // Hint inside the oEl
            else
            {
                var children = oEl.children(),
                    list = oEl.children( setting.listSelector ).first();

                if ( (list.children().first().is( '#s-l-placeholder' )) || ( setting.maxLevels !== false && ! checkMaxLevels( true )) )
                {
                    hint.css( 'display', 'none' );
                    return;
                }

                // Find out if is necessary to wrap hint by hintWrapper
                if ( ! list.length )
                {
                    children.first().after( hint );
                    hint.wrap( hintWrapper );
                }
                else
                {
                    list.prepend( hint );
                }

                if ( state.oEl )
                {
                    open( oEl ); // TODO:animation??? .children('ul,ol').css('display', 'block');
                }

            }

            hint.css( 'display', 'block' );
            // Ensures posible formating of elements. Second call is in the endDrag method.
            state.isAllowed = setting.isAllowed( state.cEl.el, hint, hint.parents( 'li' ).first() );

        }

        /**
         * @desc Called from showHint method. Displays or hides hint element
         * @param e event
         * @param oEl oElement
         * @param outside bool
         * @return No value
         */
        function showOnTopPlus( e, oEl, outside )
        {
            if ( $( '#s-l-hint-wrapper', state.rootEl.el ).length )
            {
                hint.unwrap();  // If hint is wrapped by ul/ol #s-l-hint-wrapper
            }

            // Hint inside the oEl
            if ( ! outside && e.pageX - oEl.offset().left > setting.insertZone )
            {
                var children = oEl.children(),
                    list = oEl.children( setting.listSelector ).first();

                if ( (list.children().first().is( '#s-l-placeholder' )) || (setting.maxLevels !== false && ! checkMaxLevels( true )) )
                {
                    hint.css( 'display', 'none' );
                    return;
                }

                // Find out if is necessary to wrap hint by hintWrapper
                if ( ! list.length )
                {
                    children.first().after( hint );
                    hint.wrap( hintWrapper );
                }
                else
                {
                    list.prepend( hint );
                }

                if ( state.oEl )
                {
                    open( oEl ); // TODO:animation??? .children('ul,ol').css('display', 'block');
                }
            }
            // Hint outside the oEl
            else
            {
                // Ensure display:none if hint will be next to the placeholder
                if ( (oEl.prev( '#s-l-placeholder' ).length) || (setting.maxLevels !== false && ! checkMaxLevels( false )) )
                {
                    hint.css( 'display', 'none' );
                    return;
                }
                oEl.before( hint );

            }

            hint.css( 'display', 'block' );
            // Ensures posible formating of elements. Second call is in the endDrag method.
            state.isAllowed = setting.isAllowed( state.cEl.el, hint, hint.parents( 'li' ).first() );

        }

        /**
         * @desc Called from showHint function. Displays or hides hint element.
         * @param e event
         * @param oEl oElement
         * @return No value
         */
        function showOnBottom( e, oEl )
        {
            if ( $( '#s-l-hint-wrapper', state.rootEl.el ).length )
            {
                hint.unwrap();  // If hint is wrapped by ul/ol s-l-hint-wrapper
            }

            // Hint outside the oEl
            if ( e.pageX - oEl.offset().left < setting.insertZone )
            {
                // Ensure display:none if hint will be next to the placeholder
                if ( (oEl.next( '#s-l-placeholder' ).length) || (setting.maxLevels !== false && ! checkMaxLevels( false )) )
                {
                    hint.css( 'display', 'none' );
                    return;
                }
                oEl.after( hint );
            }
            // Hint inside the oEl
            else
            {
                var children = oEl.children(),
                    list = oEl.children( setting.listSelector ).last();  // ul/ol || empty jQuery obj

                if ( (list.children().last().is( '#s-l-placeholder' )) || (setting.maxLevels !== false && ! checkMaxLevels( true )) )
                {
                    hint.css( 'display', 'none' );
                    return;
                }

                // Find out if is necessary to wrap hint by hintWrapper
                if ( list.length )
                {
                    children.last().append( hint );
                }
                else
                {
                    oEl.append( hint );
                    hint.wrap( hintWrapper );
                }

                if ( state.oEl )
                {
                    open( oEl ); // TODO: animation???
                }

            }

            hint.css( 'display', 'block' );
            // Ensures posible formating of elements. Second call is in the endDrag method.
            state.isAllowed = setting.isAllowed( state.cEl.el, hint, hint.parents( 'li' ).first() );

        }

        /**
         * @desc Called from showHint function. Displays or hides hint element.
         * @param e event
         * @param oEl oElement
         * @param outside bool
         * @return No value
         */
        function showOnBottomPlus( e, oEl, outside )
        {
            if ( $( '#s-l-hint-wrapper', state.rootEl.el ).length )
            {
                hint.unwrap();  // If hint is wrapped by ul/ol s-l-hint-wrapper
            }

            // Hint inside the oEl
            if ( ! outside && e.pageX - oEl.offset().left > setting.insertZone )
            {
                var children = oEl.children(),
                    list = oEl.children( setting.listSelector ).last();  // ul/ol || empty jQuery obj

                if ( (list.children().last().is( '#s-l-placeholder' )) || (setting.maxLevels !== false && ! checkMaxLevels( true )) )
                {
                    hint.css( 'display', 'none' );
                    return;
                }

                // Find out if is necessary to wrap hint by hintWrapper
                if ( list.length )
                {
                    children.last().append( hint );
                }
                else
                {
                    oEl.append( hint );
                    hint.wrap( hintWrapper );
                }

                if ( state.oEl )
                {
                    open( oEl ); // TODO: animation???
                }

            }
            // Hint outside the oEl
            else
            {
                // Ensure display:none if hint will be next to the placeholder
                if ( (oEl.next( '#s-l-placeholder' ).length) || (setting.maxLevels !== false && ! checkMaxLevels( false )) )
                {
                    hint.css( 'display', 'none' );
                    return;
                }
                oEl.after( hint );

            }

            hint.css( 'display', 'block' );
            // Ensures posible formating of elements. Second call is in the endDrag method.
            state.isAllowed = setting.isAllowed( state.cEl.el, hint, hint.parents( 'li' ).first() );

        }

        //////// End of show hint handlers ////////////////////////////////////////////////////
        //////// Open/close handlers //////////////////////////////////////////////////////////

        /**
         * @desc Handles opening nested lists
         * @param li
         */
        function open( li )
        {
            li.removeClass( 's-l-closed' ).addClass( 's-l-open' );
            li.children( setting.listSelector ).css( 'display', 'block' );

            var opener = li.children( 'div' ).children( '.s-l-opener' ).first();

            if ( setting.opener.as == 'html' )
            {
                opener.html( setting.opener.close );
            }
            else if ( setting.opener.as == 'class' )
            {
                opener.addClass( setting.opener.close ).removeClass( setting.opener.open );
            }
        }

        /**
         * @desc Handles opening nested lists
         * @param li
         */
        function close( li )
        {
            li.removeClass( 's-l-open' ).addClass( 's-l-closed' );
            li.children( setting.listSelector ).css( 'display', 'none' );

            var opener = li.children( 'div' ).children( '.s-l-opener' ).first();

            if ( setting.opener.as == 'html' )
            {
                opener.html( setting.opener.open );
            }
            else if ( setting.opener.as == 'class' )
            {
                opener.addClass( setting.opener.open ).removeClass( setting.opener.close );
            }

        }

        /////// Enf of open/close handlers //////////////////////////////////////////////
        /////// Levels handlers /////////////////////////////////////////////////////////

        function getInsideLevels( li )
        {
            var levs = 0;

            var list = li.children( setting.listSelector );

            if( list.length )
            {
                levs++;
                var maxNestedLevs = 0;
                var currLiLevs = 0;
                list.find( 'li' ).each( function( i )
                {
                    currLiLevs = getInsideLevels($(this));
                    if( maxNestedLevs < currLiLevs ) maxNestedLevs = currLiLevs;
                });

                if( maxNestedLevs ) levs = levs + maxNestedLevs;
            }

            return levs;
        }

        function setInsideLevels( li, levs )
        {
            li.data('inside-levels', levs);
        }

        function getUpperLevels( li )
        {
            var levs = 0;
            var rootEl = state.rootEl.el;
            var parentList = li.closest( setting.listSelector );

            while( ! parentList.is( rootEl ) )
            {
                levs++;
                parentList = parentList.parent().closest( setting.listSelector );
            }

            return levs;
        }

        function setUpperLevels( li, levs )
        {
            li.data('upper-levels', levs);
        }

        function checkMaxLevels( inside )
        {
            var insideLevs = state.cEl.el.data( 'inside-levels' );
            var upperLevs = state.oEl.data( 'upper-levels' );

            return setting.maxLevels > upperLevs + insideLevs + (inside ? 1 : 0);
        }

        function recountLevels( li )
        {
            var rootEl = state.rootEl.el;
            var parentList = li.parent( setting.listSelector );

            setInsideLevels( li, getInsideLevels( li ) );
            setUpperLevels( li, getUpperLevels( li ) );

            var i = 0;
            li.find( 'li' ).each( function()
            {
                var li = $(this);
                setInsideLevels( li, getInsideLevels( li ) );
                setUpperLevels( li, getUpperLevels( li ) );
            });

            while( ! parentList.is( rootEl ) && i < 50 )
            {
                var li = parentList.parent( 'li' );
                setInsideLevels( li, getInsideLevels( li ) ); // No need to set upper levels
                parentList = li.parent( setting.listSelector );
                i++;
            }
        }

        /////// End of levels handlers //////////////////////////////////////////////////
        /////// Tidy handlers ///////////////////////////////////////////////////////////

        /**
         * @desc Places the currEl to the target place
         * @param cEl
         */
        function tidyCurrEl( cEl )
        {
            var cElStyle = cEl.el[0].style;

            cEl.el.removeClass( setting.currElClass + ' s-l-current' );
            cElStyle.top = '0';
            cElStyle.left = '0';
            cElStyle.position = 'relative';
            cElStyle.width = 'auto';

        }

        /**
         * @desc Removes empty lists and redundant openers
         */
        function tidyEmptyLists()
        {
            // Remove every empty ul/ol from root and also with .s-l-opener
            // hintWrapper can not be removed before the hint
            $( setting.listSelector, state.rootEl.el ).each( function( i )
                {
                    if ( ! $( this ).children().length )
                    {
                        $( this ).prev( 'div' ).children( '.s-l-opener' ).first().remove();
                        $( this ).remove();
                    }
                }
            );

        }

    };


    //// toArray /////////////////////////////////////////////////////////////////////////////////////

    /**
     * @desc jQuery plugin
     * @returns this to unsure chaining
     */
    $.fn.sortableListsToArray = function( arr, parentId )
    {
        arr = arr || [];
        var order = 0;

        this.children( 'li' ).each( function()
        {
            var li = $( this ),
                listItem = {},
                id = li.attr( 'id' );

            if ( ! id )
            {
                console.log( li ); // Have to be here! Read next exception message.
                throw 'Previous item in console.log has no id. It is necessary to create the array.';
            }

            listItem.id = id;
            listItem.parentId = parentId;
            listItem.value = li.data( 'value' );
            listItem.order = order;
            listItem.filename = li.data( 'filename' );
            listItem.column_data = li.data( 'column_data' );
            arr.push( listItem );
            li.children( 'ul,ol' ).sortableListsToArray( arr, id );
            order ++;
        } );

        return arr;

    };

    /**
     * @desc jQuery plugin
     * @returns this to unsure chaining
     */
    $.fn.sortableListsToHierarchy = function()
    {
        var arr = [],
            order = 0;

        $( this ).children( 'li' ).each( function()
        {
            var li = $( this ),
                listItem = {},
                id = li.attr( 'id' );

            if ( ! id )
            {
                console.log( li ); // Have to be here! Read next exception message.
                throw 'Previous item in console.log has no id. It is necessary to create the array.';
            }
            listItem.id = id;
            listItem.value = li.data( 'value' );
            listItem.order = order;
            listItem.filename = li.data( 'filename' );
            listItem.column_data = li.data( 'column_data' );
            arr.push( listItem );
            listItem.children = li.children( 'ul,ol' ).sortableListsToHierarchy();
            order ++;
        } );

        return arr;

    };

    /**
     * @desc jQuery plugin
     * @returns string
     */
    $.fn.sortableListsToString = function( arr, parentId )
    {
        arr = arr || [];
        parentId = parentId || 'no-parent'; // string "0" is evaluate to true and is valid

        $( this ).children( 'li' ).each( function()
        {
            var li = $( this ),
                id = li.attr( 'id' ),
                matches = id ? id.match( /(.+)[-=_](.+)/ ) : null; // string "0" is evaluate to true but is not valid

            if ( ! matches )
            {
                console.log( li );  // Have to be here. Read next exception message.
                throw 'Previous item in console.log has no id or id is not in required format xx_yy, xx-yy or xx=yy. It is necessary to create valid string.';
            }

            arr.push( matches[1] + '[' + matches[2] + ']=' + parentId );
            $( this ).children( 'ul,ol' ).sortableListsToString( arr, matches[2] );

        } );

        return arr.join( '&' );

    };

}( jQuery ));