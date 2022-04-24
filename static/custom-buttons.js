//------------------------------------------------------------------------------
// Sending AJAX request without reloading whole page
//
//  https://datatables.net/forums/discussion/67031/how-do-i-reload-data-for-a-single-row-via-ajax
//
//------------------------------------------------------------------------------
//  $('#dtSjob').on('click', 'a.editor_despall', function (e) {
//     e.preventDefault();
//  
//     var lsRow = sjobTable.row( $(this).closest('tr'));
//     var lsData = lsRow.data();
//     var rowID = lsData['recno'];
//  
//     var dataSL = {};
//     dataSL.job = lsData['sjob']['job'];
//     dataSL.urn = lsData['sjob']['urn'];
//  
//     $.ajax({ url: "AjaxGetData.wc?ti=rf&fl=DespAllQty&key=CallFunc;"+dataSL.job+"~C;"+dataSL.urn+"~C" ,
//        type: "POST",
//        success: function(data) {
//          refreshRow(rowID, lsRow);
//        }
//     });
//   });
//  
// function refreshRow(id, row) {
//     //console.log("Refreshing data for recno: "+id);
//         $.ajax( {
//             url: 'AjaxSjob.wc',
//             type: 'post',
//             dataType: 'json',
//             data: {
//                 refresh: 'rows',
//                 ids: id
//             },
//             success: function ( json ) {
//                 // On success update rows with data
//                 row.data(json.data[0]);
//                 sjobTable.draw(false);
//             }
//         } );
// }
//------------------------------------------------------------------------------

/*******************************************************************************
 * Icons used for custom table buttons are downloaded from IconPacks site.
 *
 *   https://iconpacks.net/?utm_source=link-attribution&utm_content=14217
 *
 */
// mark selected message to read
$.fn.dataTables.ext.buttons.markAsRead = {
  tag: 'img',
  attr: { src: "{{ url_for('static', filename='checklist-13197-32.png') }}" },
  className: 'customBtn',                     // styling: size, border, ...
  titleAttr: 'Mark selected entries to read', // tooltip
  action: function( e, dt, node, config ) {
    // get a list of entry id's of selecte rows

    // send request to server to mark them as read

    // reload the page (or change only selected rows)

    alert('to be implemented');
  }
};


// collapse all open rows (details rows) by generating 'click' events to them
//
// -- https://datatables.net/extensions/buttons/examples/styling/icons.html
//
$.fn.dataaTable.ext.buttons.collapseAll = {
  tag: 'img',
  //attr: { src: "{{ url_for('static', filename='north-arrow-235-32.png') }}" },
  attr: { src: "{{ url_for('static', filename='double-arrow-up-14217-32.png') }}" },
  className: 'customBtn',
  titleAttr: 'Collapse all open rows',
  action: function(e, dt, node, config) {
    dt.rows( ".details" ).nodes().to$().click(); // to$() convert to jQuery obj 
  }
};


// reload data belongs to current page number (?)
// <-- probably no use for logbook so do simple refresh.
// 
$.fn.dataaTable.ext.buttons.reload = {
  tag: 'img',
  attr: { src: "{{ url_for('static', filename='reset-14414-32.png') }}" },
  className: 'customBtn',
  titleAttr: 'Reload current page',
  action: function(e, dt, node, config) {
    dt.ajax.reload();              // reload the table data
    //dt.ajax.reload(null, fall);  // keep current paging position
  }
};


// show only unread messages
//
// NOTE: See 'https://datatables.net/examples/plug-ins/range_filtering.html'
//
//     Also 'https://makitweb.com/how-to-add-custom-filter-in-datatable-ajax-and-php/'
//
$.fn.dataTables.button.filterUnread = {
  tag: 'img',
  attr: { src: "{{ url_for('static', filename='') }}" },
  className: 'customBtn',  // size, border, ...
  titleAttr: 'Load Collapse all open rows',            // tooltip
  action: function(e, dt, node, config) {
    // on state change,
    //   reload page with given flag
    //   change text or icon
    
    // on reload (eg, change to next page, ...),
    // load messages with given flag
    alert('to be implemented');
  }
};
