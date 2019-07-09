import QtQuick 2.0
import QtQuick.Layouts 1.3
import QtQuick.Scene3D 2.0
import QtCharts 2.3

Item {
    id: root


    property var chartData: [
        [
            { x: 0, y: 0 },
            { x: 1, y: 3},
            { x: 2, y: 7},
            { x: 3, y: 3},
            { x: 4, y: 10}
        ],
        [
            { x: 6, y: 0 },
            { x: 7, y: 3},
            { x: 8, y: 7},
            { x: 9, y: 3},
            { x: 10, y: 10}
        ]
    ]

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

                        Component.onCompleted: {
                            chartContainer.chartData.forEach(function(item) {
                                append(item.x, item.y)
                            })
                            chart.axisX(series).min = 0
                            chart.axisX(series).max = 10
                            chart.axisY(series).min = 0
                            chart.axisY(series).max = 10
                        }
                    }

                    LineSeries {
                        id: series2
                        name: "LineSeries"

                        Component.onCompleted: {
                            chartContainer.chartData.forEach(function(item) {
                                append(item.x, item.y + 5)
                            })
                            chart.axisX(series).min = 0
                            chart.axisX(series).max = 10
                            chart.axisY(series).min = 0
                            chart.axisY(series).max = 10
                        }
                    }
                }

            }
        }
    }




}
