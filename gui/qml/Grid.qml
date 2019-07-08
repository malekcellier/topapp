import Qt3D.Core 2.0
import Qt3D.Render 2.0
import Qt3D.Input 2.0
import Qt3D.Extras 2.0

import QtQuick 2.0 as QQ2

import "effects"

Entity {
  id: grid
  property alias transform: transform
  property real width
  property real height

  GridMaterial {
    id: gridMaterial
    lineWidth: 1.0
    lineColor: "white"
    gridResolution: 0.2
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
