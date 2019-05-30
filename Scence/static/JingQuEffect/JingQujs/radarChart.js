function drawRadar() {

    var mychart = echarts.init(document.getElementById("evaluate"));
    var mychart2 = echarts.init(document.getElementById("keyword"));
    var option = {


        tooltip: {},
        backgroundcolor: "blue",
        radar: {
            indicator: [{
                name: "环境优美",
                max: 100
            },
                {
                    name: '设备齐全',
                    max: 100
                },
                {
                    name: '性价比高',
                    max: 100
                },
                {
                    name: '交通方便',
                    max: 100
                },
                {
                    name: '干净整洁',
                    max: 100
                },
                {
                    name: '人流拥挤',
                    max: 100
                }
            ]
        },
        series: [{

            type: 'radar',
            // areaStyle: {normal: {}},
            data: [{
                value: [80, 20, 38, 78, 93, 67],
                name: "景区评分"
            },
            ]
        }]
    };
    mychart.setOption(option);
    mychart2.setOption(option);
    setInterval(function () {
        option.series[0].data[0].value[Math.floor(Math.random()*10)] = 20+Math.floor(Math.random()*50)
        mychart.setOption(option);
        mychart2.setOption(option);
    }, 1000);
}


 