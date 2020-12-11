$(document).ready(function() {
    var table = $('#protocols').DataTable( {
        "order": [[ 0, "desc" ]]
    } );

    $('#protocols tbody').on('click', 'tr', function () {
        var data = table.row( this ).data();
		window.open(data[0]+"/","_self");
 //       alert( 'You clicked on '+data[0]+'\'s row' );
    } );
} );