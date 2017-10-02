//stock search
$(function() {
    $('#form-search').on('submit', function(e) {
        e.preventDefault();
        var stock = $('#stock-symbol').val();
        // console.log('STOCK: ', stock)

        $.ajax({
            url: 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20yahoo.finance.quotes%20where%20symbol%20in%20(%22' + stock + '%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys&callback=',
            type: 'POST',
            success: function(response) {
                let quote = response.query.results.quote;
                // console.log(quote)
                if(quote.LastTradePriceOnly == null) {
                    console.log('Bad Search');
                    $('.hidden-flash').show();
                    return
                } else {
                $.ajax({
                    url: '/search',
                    data: JSON.stringify(quote),
                    type: 'POST',
                    contentType: "application/json; charset=utf-8",
                    success: function() {
                        console.log('Successful API post');
                    },
                    error: function(error) {
                        console.log(error);
                    }
                });
                }
            },
            error: function(error) {
                console.log(error);
            }
        });

    });
});

//stock delete
$(function() {
    $('.delete').on('click', function(e) {
        e.preventDefault();
        var symbol = $(this).closest('.delete').attr("id");
        console.log('SYMBOL: ', symbol)
        $.ajax({
            url: '/delete',
            data: JSON.stringify(symbol),
            type: 'POST',
            contentType: "application/json; charset=utf-8",
            success: function() {
                console.log('Successful DELETE post');
                // $('.delete').remove();
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});

$(document).ready(function(){
    setTimeout(function() {
    $(".flash").delay(5000).fadeOut();
    });
});

// reload after stock search
$(document).ajaxStop(function(){
    window.location.reload();
});
