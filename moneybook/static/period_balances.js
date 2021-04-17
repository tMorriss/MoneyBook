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

function drawGraph() {
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
        categoryAxis.renderer.labels.template.horizontalCenter = "right";
        categoryAxis.renderer.labels.template.verticalCenter = "middle";
        categoryAxis.renderer.labels.template.rotation = 270;

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
        bullet.tooltipText = "{categoryX}\n{valueY}円";
        let circle = bullet.createChild(am4core.Circle);
        circle.radius = 5;
        circle.fill = series.stroke;
    });

}
