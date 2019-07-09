import QtQuick 2.0
import QtQuick.Layouts 1.3
import QtQuick.Scene3D 2.0
import QtCharts 2.3

Item {
    id: root

    property var chartData: [kpiModel]

    GridLayout {
        id: grid
        columns: 3
        rows: 2
        anchors.fill: parent

        Repeater {
            model: 6

            Item {
                id: chartContainer

                property var chartData: root.chartData[index]
                onChartDataChanged: series.loadData()

                Layout.fillHeight: true
                Layout.fillWidth: true

                ChartView {
                    id: chart
                    title: "Line"
                    antialiasing: true
                    anchors.fill: parent
                    visible: !!chartContainer.chartData

                    LineSeries {
                        id: series
                        name: "LineSeries"

                        Component.onCompleted: loadData()

                        function loadData() {
                            if(!chartContainer.chartData) return

                            chartContainer.chartData.forEach(function(item, index) {
                                append(index, item)
                            })
                            chart.axisX(series).min = 0
                            chart.axisX(series).max = chartContainer.chartData.length
                            chart.axisY(series).min = 0
                            chart.axisY(series).max = 1
                        }
                    }
                }

            }
        }
    }
}
