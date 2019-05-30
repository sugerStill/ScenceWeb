function D40Chart(IdName) {
    this.IdName = IdName;
    this.mychart = echarts.init(document.getElementById(IdName));
    this.option = {
        title: {
            text: '天气情况',
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
                    backgroundColor: '#6a7985'
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


            }]
    };

}

D40Chart.prototype.setData = function dealData(json, num = -1) {
    var time = '';
    var data = '';

    this.option.xAxis.data = ['1.1', '1.2', '1.3', '1.4', '1.5', '1.6', '1.7', '1.8'];
    this.option.series[0].data = [1, 2, 3, 4, 4, 4, 5, 5];

    this.mychart.setOption(this.option);

};