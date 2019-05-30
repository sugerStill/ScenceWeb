function Air_element() {
    var data = {
        legendData: ["一氧化碳", '臭氧', '二氧化硫', '二氧化氮', 'PM10', 'PM2.5'],
        seriesData: [{name: '一氧化碳', value: 10}, {name: '臭氧', value: 20}, {name: '二氧化硫', value: 30}, {
            name: '二氧化氮',
            value: 23
        }, {name: 'PM10', value: 32}, {name: 'PM2.5', value: 12}],
        selected: {'一氧化碳': true, '臭氧': true, '二氧化硫': true, '二氧化氮': true, 'PM10': true, 'PM2.5': true}

    };

    mychart = echarts.init(document.getElementById("Air_element"));

    option = {
        title: {
            text: '空气中主要污染物浓度',
            x: 'center',
            textStyle: {
                color: 'white',
            }
        },
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b} : {c} ({d}%)",
            color: 'white'
        },
        legend: {
            type: 'scroll',
            orient: 'vertical',
            right: 10,
            top: 20,
            bottom: 20,
            data: data.legendData,

            selected: data.selected,
            textStyle: {
                color: 'white'

            }
        },
        series: [
            {
                name: '污染物',
                type: 'pie',
                radius: '55%',
                center: ['40%', '50%'],
                data: data.seriesData,

                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }

            }
        ]
    };


    mychart.setOption(option);
    // setInterval(function () {
    //     option.series[0].data[0].value[Math.floor(Math.random()*10)] = 20+Math.floor(Math.random()*50)
    //     mychart.setOption(option);
    //     mychart2.setOption(option);
    // }, 1000);
}


 