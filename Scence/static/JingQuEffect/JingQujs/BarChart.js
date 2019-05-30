//绘画与其它景区对比的优缺点
function drawBar() {
    var mychart = echarts.init(document.getElementById("compare"));


    var option = {
        // title: {
        //     text: '景区对比',
        //     x: 'center',
        //     y:'top',
        //     textStyle: {
        //         color: 'white',
        //     }
        //
        // },
        color: ['#003366', '#006699', '#4cabce', '#e5323e'],
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            },
            color: 'white'

        },
        legend: {
            data: ['Forest', 'Steppe', 'Desert', 'Wetland'],
            textStyle: {
                color: 'white'

            }
        },
        toolbox: {
            show: true,
            orient: 'vertical',
            left: 'right',
            top: 'center',
            feature: {
                mark: {show: true},
                dataView: {show: true, readOnly: false},
                magicType: {show: true, type: ['line', 'bar', 'stack', 'tiled']},
                restore: {show: true},
                saveAsImage: {show: true}
            }
        },
        calculable: true,
        xAxis: [
            {
                type: 'category',
                axisTick: {show: false},
                data: ['设备条件', '环境幽静', '干净整洁', '游客拥挤', '交通方便'],

                axisLabel: {
                    color: "white",
                }
            }
        ],
        yAxis: [
            {
                type: 'value',

                axisLabel: {
                    color: "white",
                }
            }
        ],

        series: [
            {
                name: 'Forest',
                type: 'bar',
                barGap: 0,
                data: [320, 332, 301, 334, 390],


            },
            {
                name: 'Steppe',
                type: 'bar',
                data: [220, 182, 191, 234, 290]
            },
            {
                name: 'Desert',
                type: 'bar',
                data: [150, 232, 201, 154, 190]
            },
            {
                name: 'Wetland',
                type: 'bar',
                data: [98, 77, 101, 99, 40]
            }
        ]
    };
    mychart.setOption(option);
}