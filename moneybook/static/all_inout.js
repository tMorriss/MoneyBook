function drawGraph() {
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

function moveYear() {
    year = $("#jump_year").val();
    window.location.href = all_inout_url + "/" + year;
}
function keyPressMove(code) {
    //エンターキーなら
    if (code === 13) {
        moveYear();
    }
}
