let roots = {};

function disposeRoot(divId) {
    if (roots[divId]) {
        roots[divId].dispose();
        delete roots[divId];
    }
}

function drawGraph() {
    // 収入・支出・生活費・給与・食費
    (function () {
        const divId = "barplot_inout";
        disposeRoot(divId);

        // データ収集
        let monthData = {};
        let monthIoList = $("#month_io_list li");
        for (var i = 0; i < monthIoList.length; i++) {
            let data = monthIoList[i].textContent.split(',');
            monthData[data[0]] = { month: data[0], income: Number(data[1]), outgo: Number(data[2]) };
        }
        let livingCostsList = $("#living_costs li");
        for (var i = 0; i < livingCostsList.length; i++) {
            let data = livingCostsList[i].textContent.split(',');
            monthData[data[0]]["living"] = Number(data[1]);
        }
        let salaryList = $("#salary li");
        for (var i = 0; i < salaryList.length; i++) {
            let data = salaryList[i].textContent.split(',');
            monthData[data[0]]["salary"] = Number(data[1]);
        }
        let foodList = $("#food_costs li");
        for (var i = 0; i < foodList.length; i++) {
            let data = foodList[i].textContent.split(',');
            monthData[data[0]]["food"] = Number(data[1]);
        }
        let chartData = [];
        for (let i in monthData) {
            chartData.push(monthData[i]);
        }

        let root = am5.Root.new(divId);
        roots[divId] = root;
        root.setThemes([am5themes_Animated.new(root), am5themes_Kelly.new(root)]);

        let chart = root.container.children.push(am5xy.XYChart.new(root, {
            panX: false,
            panY: false,
            wheelX: "none",
            wheelY: "none",
            layout: root.verticalLayout
        }));

        let xAxis = chart.xAxes.push(am5xy.CategoryAxis.new(root, {
            categoryField: "month",
            renderer: am5xy.AxisRendererX.new(root, {
                minGridDistance: 30
            })
        }));
        xAxis.data.setAll(chartData);

        let yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {
            min: 0,
            renderer: am5xy.AxisRendererY.new(root, {})
        }));

        drawIOGraph(root, chart, xAxis, yAxis, chartData);

        let configLines = [
            { value: "living", name: "生活費", color: "#0f0" },
            { value: "salary", name: "給与", color: "#ff0" },
            { value: "food", name: "食費", color: "#e70" }
        ];

        configLines.forEach(function (conf) {
            let series = chart.series.push(am5xy.LineSeries.new(root, {
                name: conf.name,
                xAxis: xAxis,
                yAxis: yAxis,
                valueYField: conf.value,
                categoryXField: "month",
                stroke: am5.color(conf.color),
                tooltip: am5.Tooltip.new(root, {
                    labelText: "{name}: {valueY}円"
                })
            }));
            series.strokes.template.setAll({ strokeWidth: 3 });
            series.data.setAll(chartData);

            series.bullets.push(function () {
                return am5.Bullet.new(root, {
                    sprite: am5.Circle.new(root, {
                        radius: 5,
                        fill: am5.color(conf.color)
                    })
                });
            });
        });

        chart.set("legend", am5.Legend.new(root, {
            centerX: am5.p50,
            x: am5.p50
        }));
        chart.get("legend").data.setAll(chart.series.values);
    })();

    // インフラ
    (function () {
        const divId = "lineplot_infra";
        disposeRoot(divId);

        let infraList = $("#infra_costs li");
        let chartData = [];
        for (var i = 0; i < infraList.length; i++) {
            let data = infraList[i].textContent.split(',');
            chartData.push({
                month: data[0],
                electricity: Number(data[1]),
                gus: Number(data[2]),
                water: Number(data[3]),
                total: Number(data[4])
            });
        }

        let root = am5.Root.new(divId);
        roots[divId] = root;
        root.setThemes([am5themes_Animated.new(root), am5themes_Kelly.new(root)]);

        let chart = root.container.children.push(am5xy.XYChart.new(root, {
            layout: root.verticalLayout
        }));

        let xAxis = chart.xAxes.push(am5xy.CategoryAxis.new(root, {
            categoryField: "month",
            renderer: am5xy.AxisRendererX.new(root, { minGridDistance: 30 })
        }));
        xAxis.data.setAll(chartData);

        let yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {
            min: 0,
            renderer: am5xy.AxisRendererY.new(root, {})
        }));

        let config = [
            { value: "electricity", name: "電気代", color: "#ff0" },
            { value: "gus", name: "ガス代", color: "#f00" },
            { value: "water", name: "水道代", color: "#00f" },
            { value: "total", name: "合計", color: "#000" },
        ];

        config.forEach(function (conf) {
            let series = chart.series.push(am5xy.LineSeries.new(root, {
                name: conf.name,
                xAxis: xAxis,
                yAxis: yAxis,
                valueYField: conf.value,
                categoryXField: "month",
                stroke: am5.color(conf.color),
                tooltip: am5.Tooltip.new(root, {
                    labelText: "{name}: {valueY}円"
                })
            }));
            series.strokes.template.setAll({ strokeWidth: 3 });
            series.data.setAll(chartData);

            series.bullets.push(function () {
                return am5.Bullet.new(root, {
                    sprite: am5.Circle.new(root, {
                        radius: 5,
                        fill: am5.color(conf.color)
                    })
                });
            });
        });

        chart.set("legend", am5.Legend.new(root, {
            centerX: am5.p50,
            x: am5.p50
        }));
        chart.get("legend").data.setAll(chart.series.values);
    })();

    // 全収入・支出
    (function () {
        const divId = "barplot_inout_all";
        disposeRoot(divId);

        let allIOList = $("#month_all_io_list li");
        let chartData = [];
        for (var i = 0; i < allIOList.length; i++) {
            let data = allIOList[i].textContent.split(',');
            chartData.push({ month: data[0], income: Number(data[1]), outgo: Number(data[2]) });
        }

        let root = am5.Root.new(divId);
        roots[divId] = root;
        root.setThemes([am5themes_Animated.new(root), am5themes_Kelly.new(root)]);

        let chart = root.container.children.push(am5xy.XYChart.new(root, {
            layout: root.verticalLayout
        }));

        let xAxis = chart.xAxes.push(am5xy.CategoryAxis.new(root, {
            categoryField: "month",
            renderer: am5xy.AxisRendererX.new(root, { minGridDistance: 30 })
        }));
        xAxis.data.setAll(chartData);

        let yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {
            min: 0,
            renderer: am5xy.AxisRendererY.new(root, {})
        }));

        drawIOGraph(root, chart, xAxis, yAxis, chartData);

        chart.set("legend", am5.Legend.new(root, {
            centerX: am5.p50,
            x: am5.p50
        }));
        chart.get("legend").data.setAll(chart.series.values);
    })();

    // 途中残高
    (function () {
        const divId = "lineplot_monthly_balance";
        disposeRoot(divId);

        let balanceList = $("#monthly_balance li");
        let chartData = [];
        let minValue = null;
        for (var i = 0; i < balanceList.length; i++) {
            let data = balanceList[i].textContent.split(',');
            let val = Number(data[1]);
            chartData.push({ month: data[0], balance: val });
            if (minValue == null || minValue > val) {
                minValue = val;
            }
        }

        let root = am5.Root.new(divId);
        roots[divId] = root;
        root.setThemes([am5themes_Animated.new(root), am5themes_Kelly.new(root)]);

        let chart = root.container.children.push(am5xy.XYChart.new(root, {
            layout: root.verticalLayout
        }));

        let xAxis = chart.xAxes.push(am5xy.CategoryAxis.new(root, {
            categoryField: "month",
            renderer: am5xy.AxisRendererX.new(root, { minGridDistance: 30 })
        }));
        xAxis.data.setAll(chartData);

        let yAxis = chart.yAxes.push(am5xy.ValueAxis.new(root, {
            min: (minValue > 0) ? 0 : undefined,
            renderer: am5xy.AxisRendererY.new(root, {})
        }));

        let series = chart.series.push(am5xy.LineSeries.new(root, {
            name: "残高",
            xAxis: xAxis,
            yAxis: yAxis,
            valueYField: "balance",
            categoryXField: "month",
            stroke: am5.color("#0f0"),
            tooltip: am5.Tooltip.new(root, {
                labelText: "{valueY}円"
            })
        }));
        series.strokes.template.setAll({ strokeWidth: 3 });
        series.data.setAll(chartData);

        series.bullets.push(function () {
            return am5.Bullet.new(root, {
                sprite: am5.Circle.new(root, {
                    radius: 5,
                    fill: am5.color("#0f0")
                })
            });
        });
    })();
}

function drawIOGraph(root, chart, xAxis, yAxis, chartData) {
    let xRenderer = xAxis.get("renderer");
    xRenderer.setAll({
        cellStartLocation: 0.1,
        cellEndLocation: 0.9
    });

    let config = [
        { value: "income", name: "収入", color: "#00f" },
        { value: "outgo", name: "支出", color: "#f00" },
    ];

    config.forEach(function (conf) {
        let series = chart.series.push(am5xy.ColumnSeries.new(root, {
            name: conf.name,
            xAxis: xAxis,
            yAxis: yAxis,
            valueYField: conf.value,
            categoryXField: "month",
            fill: am5.color(conf.color),
            stroke: am5.color(conf.color),
            tooltip: am5.Tooltip.new(root, {
                labelText: "{name}: {valueY}円"
            })
        }));

        series.columns.template.setAll({
            width: am5.percent(100),
            strokeOpacity: 0
        });

        series.data.setAll(chartData);
    });
}

function move_year() {
    year = $("#jump_year").val();
    window.location.href = statistics_url + "/" + year;
}
function key_press_move(code) {
    //エンターキーなら
    if (code === 13) {
        move_year();
    }
}
