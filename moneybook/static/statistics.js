function drawGraph() {
    // 収入・支出・生活費・給与・食費
    am4core.ready(function () {
        // テーマ
        am4core.useTheme(am4themes_animated);
        am4core.useTheme(am4themes_kelly);

        var chart = am4core.create("barplot_inout", am4charts.XYChart);

        // データ収集
        monthData = {};
        let monthIoList = $("#month_io_list li");
        for (var i = 0; i < monthIoList.length; i++) {
            let data = monthIoList[i].textContent.split(',');
            monthData[data[0]] = { month: data[0], income: data[1], outgo: data[2] };
        }
        let livingCostsList = $("#living_costs li");
        for (var i = 0; i < livingCostsList.length; i++) {
            let data = livingCostsList[i].textContent.split(',');
            monthData[data[0]]["living"] = data[1];
        }
        let salaryList = $("#salary li");
        for (var i = 0; i < salaryList.length; i++) {
            let data = salaryList[i].textContent.split(',');
            monthData[data[0]]["salary"] = data[1];
        }
        let foodList = $("#food_costs li");
        for (var i = 0; i < foodList.length; i++) {
            let data = foodList[i].textContent.split(',');
            monthData[data[0]]["food"] = data[1];
        }
        chart.data = [];
        for (let i in monthData) {
            chart.data.push(monthData[i]);
        }
        drawIOGraph(chart);

        let livingSeries = chart.series.push(new am4charts.LineSeries());
        livingSeries.stroke = am4core.color("#0f0");
        livingSeries.strokeWidth = 3;
        livingSeries.dataFields.valueY = "living";
        livingSeries.dataFields.categoryX = "month";
        livingSeries.name = "生活費";
        let livingBullet = livingSeries.bullets.push(new am4charts.Bullet());
        livingBullet.fill = livingSeries.stroke;
        livingBullet.tooltipText = livingSeries.name + ": {valueY}円";
        let livingCircle = livingBullet.createChild(am4core.Circle);
        livingCircle.radius = 5;
        livingCircle.fill = livingSeries.stroke;

        let salarySeries = chart.series.push(new am4charts.LineSeries());
        salarySeries.stroke = am4core.color("#ff0");
        salarySeries.strokeWidth = 3;
        salarySeries.dataFields.valueY = "salary";
        salarySeries.dataFields.categoryX = "month";
        salarySeries.name = "給与";
        let salaryBullet = salarySeries.bullets.push(new am4charts.Bullet());
        salaryBullet.fill = salarySeries.stroke;
        salaryBullet.tooltipText = salarySeries.name + ": {valueY}円";
        let salaryCircle = salaryBullet.createChild(am4core.Circle);
        salaryCircle.radius = 5;
        salaryCircle.fill = salarySeries.stroke;

        let foodSeries = chart.series.push(new am4charts.LineSeries());
        foodSeries.stroke = am4core.color("#e70");
        foodSeries.strokeWidth = 3;
        foodSeries.dataFields.valueY = "food";
        foodSeries.dataFields.categoryX = "month";
        foodSeries.name = "食費";
        let foodBullet = foodSeries.bullets.push(new am4charts.Bullet());
        foodBullet.fill = foodSeries.stroke;
        foodBullet.tooltipText = foodSeries.name + ": {valueY}円";
        let foodCircle = foodBullet.createChild(am4core.Circle);
        foodCircle.radius = 5;
        foodCircle.fill = foodSeries.stroke;

        chart.legend = new am4charts.Legend();
        chart.legend.position = "bottom";
    });

    // インフラ
    am4core.ready(function () {
        // テーマ
        am4core.useTheme(am4themes_animated);
        am4core.useTheme(am4themes_kelly);

        var chart = am4core.create("lineplot_infra", am4charts.XYChart);

        // データ収集
        let infraList = $("#infra_costs li");
        chart.data = [];
        for (var i = 0; i < infraList.length; i++) {
            data = infraList[i].textContent.split(',');
            chart.data.push({ month: data[0], electricity: data[1], gus: data[2], water: data[3], total: data[4] });
        }

        let categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
        categoryAxis.dataFields.category = "month";
        categoryAxis.renderer.minGridDistance = 1;

        let valueAxis = new am4charts.ValueAxis();
        valueAxis.min = 0;
        chart.yAxes.push(valueAxis);

        let config = [
            { value: "electricity", name: "電気代", color: "#ff0" },
            { value: "gus", name: "ガス代", color: "#f00" },
            { value: "water", name: "水道代", color: "#00f" },
            { value: "total", name: "合計", color: "#000" },
        ]
        for (var c in config) {
            var series = chart.series.push(new am4charts.LineSeries());
            series.stroke = am4core.color(config[c].color);
            series.strokeWidth = 3;
            series.dataFields.valueY = config[c].value;
            series.dataFields.categoryX = "month";
            series.name = config[c].name;

            var bullet = series.bullets.push(new am4charts.Bullet());
            bullet.fill = series.stroke;
            bullet.tooltipText = config[c].name + ": {valueY}円";
            var circle = bullet.createChild(am4core.Circle);
            circle.radius = 5;
            circle.fill = series.stroke;
        }
        chart.legend = new am4charts.Legend();
        chart.legend.position = "bottom";
    });

    am4core.ready(function () {
        // テーマ
        am4core.useTheme(am4themes_animated);
        am4core.useTheme(am4themes_kelly);

        var chart = am4core.create("lineplot_food", am4charts.XYChart);

        // データ収集

        let categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
        categoryAxis.dataFields.category = "month";
        categoryAxis.renderer.minGridDistance = 1;

        let valueAxis = new am4charts.ValueAxis();
        valueAxis.min = 0;
        chart.yAxes.push(valueAxis);

        var series = chart.series.push(new am4charts.ColumnSeries());
        series.dataFields.valueY = "food";
        series.dataFields.categoryX = "month";
        series.columns.template.tooltipText = "{valueY}円";
        series.columns.template.fill = am4core.color("#ee7700");
        series.columns.template.strokeWidth = 0;
        series.columns.template.width = am4core.percent(90);
        series.name = "食費";
    });

    // 全収入・支出
    am4core.ready(function () {
        // テーマ
        am4core.useTheme(am4themes_animated);
        am4core.useTheme(am4themes_kelly);

        var chart = am4core.create("barplot_inout_all", am4charts.XYChart);

        // データ収集
        let allIOList = $("#month_all_io_list li");
        chart.data = [];
        for (var i = 0; i < allIOList.length; i++) {
            data = allIOList[i].textContent.split(',');
            chart.data.push({ month: data[0], income: data[1], outgo: data[2] });
        }

        drawIOGraph(chart);
    });

    // 途中残高
    am4core.ready(function () {
        // テーマ
        am4core.useTheme(am4themes_animated);
        am4core.useTheme(am4themes_kelly);

        var chart = am4core.create("lineplot_monthly_balance", am4charts.XYChart);

        // データ収集
        let balanceList = $("#monthly_balance li");
        chart.data = [];
        minValue = null;
        for (var i = 0; i < balanceList.length; i++) {
            data = balanceList[i].textContent.split(',');
            chart.data.push({ month: data[0], balance: data[1] });
            if (minValue == null || minValue > Number(data[1])) {
                minValue = Number(data[1])
            }
        }

        let categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
        categoryAxis.dataFields.category = "month";
        categoryAxis.renderer.minGridDistance = 1;

        let valueAxis = new am4charts.ValueAxis();
        if (minValue > 0) {
            valueAxis.min = 0;
        }
        chart.yAxes.push(valueAxis);

        let series = chart.series.push(new am4charts.LineSeries());
        series.stroke = am4core.color("#0f0");
        series.strokeWidth = 3;
        series.dataFields.valueY = "balance";
        series.dataFields.categoryX = "month";
        series.name = "残高"

        let bullet = series.bullets.push(new am4charts.Bullet());
        bullet.fill = series.stroke;
        bullet.tooltipText = "{valueY}円";
        let circle = bullet.createChild(am4core.Circle);
        circle.radius = 5;
        circle.fill = series.stroke;
    });
}

function drawIOGraph(chart) {
    let categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
    categoryAxis.dataFields.category = "month";
    categoryAxis.renderer.cellStartLocation = 0.1
    categoryAxis.renderer.cellEndLocation = 0.9
    categoryAxis.renderer.grid.template.location = 0;
    categoryAxis.renderer.grid.template.marginLeft = 0;
    categoryAxis.renderer.grid.template.marginRight = 0;
    categoryAxis.renderer.minGridDistance = 1;

    let valueAxis = new am4charts.ValueAxis();
    valueAxis.min = 0;
    chart.yAxes.push(valueAxis);

    let config = [
        { value: "income", name: "収入", color: "#00f" },
        { value: "outgo", name: "支出", color: "#f00" },
    ];
    for (var c in config) {
        var series = chart.series.push(new am4charts.ColumnSeries())
        series.dataFields.valueY = config[c].value;
        series.dataFields.categoryX = 'month';
        series.columns.template.tooltipText = config[c].name + ": {valueY}円";
        series.columns.template.fill = am4core.color(config[c].color);
        series.columns.template.strokeWidth = 0;
        series.columns.template.width = am4core.percent(100);
        series.name = config[c].name;
    }
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
