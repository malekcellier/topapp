import Qt3D.Core 2.0
import Qt3D.Render 2.0
import Qt3D.Input 2.0
import Qt3D.Extras 2.0

import QtQuick 2.0 as QQ2

import "effects"

Entity {
  id: grid
  property alias transform3d: transform
  property real width
  property real height
  property real gridResolution: 0.2
  property real lineWidth: 1.0
  property color lineColor: "white"

  GridMaterial {
    id: gridMaterial
    lineColor: grid.lineColor
    lineWidth: grid.lineWidth
    gridResolution: grid.gridResolution
  }

  PlaneMesh {
    id: planeMesh
    width: grid.width
    height: grid.height
  }

  Transform {
    id: transform
  }

  components: [ planeMesh, gridMaterial, transform ]
}
