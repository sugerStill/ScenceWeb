function Weather(idname, dataList) {
//元素格式["16日20时", "多云", "21℃", "无持续风向,<3级"]
    // 以颜色来区分天气，高度为气温
    var colordic = {
        '晴': '#F4D03F',
        '多云转晴': '#FEF9E7',
        '多云': '#D6EAF8',
        '阴': "#5F6A6A",
        '多云转雨': '#2E86C1',
        '小雨转雨': '#2E86C1',
        "雨": '#2874A6'

    };
    var colorList = []; //颜色
    var tempture = [];//温度
    var weatherstate = [];
    var time = [];//时间
    var max = 0;//最高温度
    for (let weather of dataList) {
        colorList.push(colordic[weather.state]);
        time.push(weather.date);
        temperature = weather.temperature.replace('℃', '');
        tempture.push(temperature);
        weatherstate.push(weather.state);

        if (temperature > max) {
            max =temperature;
        }
    }
    mychart = echarts.init(document.getElementById(idname));
    option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                crossStyle: {
                    color: '#999'
                }
            }
        },
        color: ['red'],

        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        legend: {
            data: ['天气情况'],//用来显示数据的名字
            textStyle: {
                color: 'white'

            }
        },
        xAxis: [
            {
                name: "时间",
                nameLocation: "middle",
                nameTextStyle: {
                    color: "white",
                    fontSize: 15
                },
                nameGap: 20,

                type: 'category',
                data: time,
                axisTick: {
                    alignWithLabel: true
                },
                axisLabel: {
                    color: "white",
                    fontSize: 8,
                }

            },


        ],
        yAxis: [

            {
                type: 'value',
                name: '温度',
                min: 0,
                max: max,
                interval: 5,
                axisLabel: {
                    formatter: '{value} °C',
                    color: "white",

                },
                nameTextStyle: {
                    color: "white",
                    fontSize: 15
                },
                nameGap: 20,
            },
            {
                type: 'category',
                name: "天气",
                // nameLocation: "middle",
                nameTextStyle: {
                    color: "white",
                    fontSize: 15
                },
                nameGap: 20,
                axisLabel: {
                    color: "white",
                    fontSize: 8,

                },
                // 所有类目名称列表,这里应该动态添加数据
                data: ['晴', '多云', '阴', '雨', '多云转晴', '多云转雨', '小雨转雨'],

            }
        ],
        series: [
            {
                name: '温度',
                type: 'line',
                data: tempture,
            },
            {
                name: '天气情况',
                type: 'bar',
                data: weatherstate,
                //设置每条item的颜色
                itemStyle: {
                    color: function (params) {

                        return colorList[params.dataIndex]
                    },
                },
                barWidth: 5,

            },


        ]
    };
    mychart.setOption(option);
}