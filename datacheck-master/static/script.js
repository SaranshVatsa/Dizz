$(document).ready(function() {
    var text = $('#text');
    text.html("<b>Email Recieved: </b>");

    var expand = $('#close');
    expand.hide();

    var sec1 = $('#sec1-sql');
    var sec2 = $('#sec2-sql');
    var sec3 = $('#sec3-sql');


    var close = $('#close-sql');
    close.on('click', function() {
        sec2.hide();
        sec3.removeClass("col-md-5");
        sec3.addClass("col-md-10");
        sec3.css('transition-duration','1s');
        sec3.css('transition-timing-function','linear');
        $('.main1').css('border-left', '8px solid rgb(114, 114, 114)');
        expand.show();  
    });

    expand.on('click', function() {
        sec2.show();
        sec3.removeClass("col-md-10");
        sec3.addClass("col-md-5");
        sec3.css('transition-duration','0s');
        $('.main1').css('border-left', '0px solid rgb(114, 114, 114)');
        expand.hide();
    });

    var str = "> SELECT * FROM Customers WHERE CustomerID=1;";
    $('#run-query').click(function() {
        console.log("Hey");
        $('#area').val(str);
    });

    
    
});