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
    var dic = new Array();
    var colorList = []; //颜色
    var tempture = [];//温度
    var weatherstate = [];
    var time = [];//时间
    var detailTimeList = [];//具体时间

    var max = 0;//最高温度
    for (let weather of dataList) {
        colorList.push(colordic[weather.state]);
        time.push(weather.date);
        detailTimeList.push(weather.detailTime);
        temperature = weather.temperature.replace('℃', '');
        temperature = parseInt(temperature);
        tempture.push(temperature);

        weatherstate.push(weather.state);

        dic[temperature] = weatherstate;
        if (temperature > max) {
            max = temperature;
        }
    }

    max = max + 5;
    mychart = echarts.init(document.getElementById(idname));
    option = {


        tooltip: {

            show: true,
            trigger: 'axis',
            axisPointer: {
                type: 'cross',
                crossStyle: {
                    color: '#999'
                }
            },
            formatter: function (params) {
                tip1 = params[0].seriesName;
                tip1Data = params[0].value;
                tip2 = params[1].seriesName;
                Index = params[1].dataIndex;
                WeatherInfo = weatherstate[Index];
                date = time[Index];
                detailTime = detailTimeList[Index];
                return tip1 + ":" + tip1Data + "°C" + '<br/>' + tip2 + ":" + WeatherInfo +
                    '<br/>' + "日期:" + date + '<br/>' + "时段:"+detailTime;


            },

        },
        color: ['red'],

        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        legend: {
            type: "scroll",
            show: true,
            data: ['天气情况', '温度'],//用来显示数据的名字
            textStyle: {
                color: 'white'

            },
            pageIconColor: 'red'
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
                data: detailTimeList,
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
                data: weatherstate,

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
                data: tempture, // 高度
                //设置每条item的颜色
                itemStyle: {
                    normal: {
                        color: function (params) {
                            return colorList[params.dataIndex]
                        }
                    }
                },
                barWidth: 5,
                barMinHeight: 20,

            },


        ]
    };
    mychart.setOption(option);
}