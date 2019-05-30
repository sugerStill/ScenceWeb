function request_server(url) {
    var request = new XMLHttpRequest();

    request.open("GET", url);
    request.responseType = "json";
    request.onload = function () {
        try {
            // 记得取消注释
            begin(request.response);
            setInterval(()=>begin(request.response),1000*1800);

        }catch (e) {
             console.log(e);
        }

    };

    request.send()

}

function  begin(response) {
     new drawAreaChart(response);
}