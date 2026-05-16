function update_range() {
    start_year = $("#start_year").val();
    start_month = $("#start_month").val();
    end_year = $("#end_year").val();
    end_month = $("#end_month").val();
    window.location.href = `${period_balances_url}?start_year=${start_year}&start_month=${start_month}&end_year=${end_year}&end_month=${end_month}`;
}
function key_press_update_range(code) {
    //エンターキーなら
    if (code === 13) {
        update_range();
    }
}

let root = null;
function drawGraph() {
    const divId = "lineplot_monthly_balance";
    if (document.getElementById(divId) === null) {
        return;
    }

    if (root) {
        root.dispose();
    }

    // データ収集
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

    root = am5.Root.new(divId);

    // テーマ
    root.setThemes([
        am5themes_Animated.new(root),
        am5themes_Kelly.new(root)
    ]);

    let chart = root.container.children.push(am5xy.XYChart.new(root, {
        panX: false,
        panY: false,
        wheelX: "none",
        wheelY: "none",
        layout: root.verticalLayout
    }));

    let xRenderer = am5xy.AxisRendererX.new(root, {
        minGridDistance: 30
    });
    xRenderer.labels.template.setAll({
        rotation: -90,
        centerY: am5.p50,
        centerX: am5.p100,
        paddingRight: 15
    });

    let xAxis = chart.xAxes.push(am5xy.CategoryAxis.new(root, {
        categoryField: "month",
        renderer: xRenderer
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
            labelText: "{categoryX}\n{valueY}円"
        })
    }));

    series.strokes.template.setAll({
        strokeWidth: 3
    });

    series.data.setAll(chartData);

    series.bullets.push(function () {
        return am5.Bullet.new(root, {
            sprite: am5.Circle.new(root, {
                radius: 5,
                fill: am5.color("#0f0")
            })
        });
    });

    // アニメーション
    series.appear(1000);
    chart.appear(1000, 100);
}
