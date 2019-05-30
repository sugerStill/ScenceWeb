function RequestTrafficHttp(url, IdName) {

    let p1 = new Promise(function (resolve, reject) {

        var request = new XMLHttpRequest();

        request.open("GET", url);
        request.responseType = "json";
        request.onload = function () {
            if (request.status === 200) {

                setInterval(() => begin(request.response), 1000 * 1800);
                resolve(request.response);
            } else {
                reject(Error('Image didn\'t load successfully; error code:' + request.statusText));
            }
        };
        request.onerror = function () {
            reject(Error('There was a network error.'));
        };
        request.send();
    });
    p1.then(function (response) {

        var CC = new CityChart(IdName);
        CC.setData(response);

    });


}



