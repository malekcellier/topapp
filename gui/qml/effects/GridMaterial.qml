
import Qt3D.Core 2.0
import Qt3D.Render 2.0

Material {
    id: root

    property real lineWidth: 0.8
    property real gridResolution: 1.0
    property color lineColor: Qt.rgba( 0.0, 0.0, 0.0, 1.0 )

    effect: GridEffect {
      lineWidth: root.lineWidth
      gridResolution: root.gridResolution
      lineColor: root.lineColor
    }
}
