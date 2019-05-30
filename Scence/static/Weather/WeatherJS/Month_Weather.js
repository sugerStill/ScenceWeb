function MonthChart(IdName) {
    this.IdName = IdName;
    this.mychart = echarts.init(document.getElementById(IdName));
    this.option = {
        title: {
            text: '月天气情况',
            x: 'center',
            textStyle: {
                color: 'white',
            }
        },
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',

                label: {
                    backgroundColor: '#6a7985',
                }
            }
        },
        xAxis: {
            type: 'category',
            name: "时间",
            nameLocation: "middle",
            nameGap: 30,
            nameTextStyle: {
                color: "white",
                fontSize: 15
            },
            boundaryGap: false,

            axisLabel: {
                color: "white",
            }

        },
        yAxis: {
            type: 'value',

            name: "天气情况",
            nameLocation: "middle",
            nameGap: 50,
            nameTextStyle: {
                color: "white",
                fontSize: 15,

            },

            axisLabel: {
                color: "white",
            }

        },

        series: [
            {
                name: "温度",
                // data: data,
                type: 'line',


            }, {
                name: "AQI",
                // data: data,
                type: 'line',


            },
            {
                name: "PM10",
                // data: data,
                type: 'line',


            },
            {
                name: "CO",
                // data: data,
                type: 'line',


            }, {
                name: "NO2",
                // data: data,
                type: 'line',


            }, {
                name: "SO2",
                // data: data,
                type: 'line',


            }, {
                name: "O3",
                // data: data,
                type: 'line',


            },]
    };

}

MonthChart.prototype.setData = function dealData(json, num = -1) {
    var time = '';
    var data = '';

    this.option.xAxis.data = ['1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '1.8'];
    this.option.series[0].data = [1, 2, 3, 4, 4, 4, 5, 5];
    this.option.series[1].data = [3, 1, 4, 5, 3, 2, 1, 6];
    this.option.series[2].data = [1, 4, 3, 2, 7, 4, 3, 7];
    this.option.series[3].data = [2, 2, 4, 3, 3, 4, 5, 5];
    this.option.series[4].data = [1, 4, 2, 6, 8, 3, 2, 5];
    this.option.series[5].data = [3, 5, 4, 6, 3, 1, 1, 6];
    this.option.series[6].data = [4, 4, 5, 2, 4, 1, 3, 7];
    this.mychart.setOption(this.option);

};