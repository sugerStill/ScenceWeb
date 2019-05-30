function request_(url, IdName, flag) {
    let p1 = new Promise(function (resolve, reject) {

        var request = new XMLHttpRequest();

        request.open("GET", url);
        request.responseType = "json";
        request.onload = function () {
            if (request.status === 200) {

                setInterval(() => begin(request.response), 1000 * 1800);
                resolve(request.response);
            } else {
                // If it fails, reject the promise with a error message
                reject(Error('Image didn\'t load successfully; error code:' + request.statusText));
            }
        };
        request.onerror = function () {
            // Also deal with the case when the entire request fails to begin with
            // This is probably a network error, so reject the promise with an appropriate message
            reject(Error('There was a network error.'));
        };
        request.send();
    });
    p1.then(function (response) {
        if (flag == 1) {


            new Listen(response, IdName);
            new loaddata(response);

        }
        var CC = new CityChart(IdName);
        CC.setData(response);

    });


}



