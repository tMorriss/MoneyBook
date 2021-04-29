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
