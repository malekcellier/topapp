import Qt3D.Core 2.0
import Qt3D.Render 2.0
import Qt3D.Input 2.0
import Qt3D.Extras 2.0

import QtQuick 2.0 as QQ2

import "effects"

Entity {
  property alias transform: transform

  GridMaterial {
    id: gridMaterial
    lineWidth: 1.0
    lineColor: "white"
    gridResolution: 0.2
  }

  PlaneMesh {
    id: planeMesh
    width: 100
    height: 100
  }

  Transform {
    id: transform
    scale3D: Qt.vector3d(1, 1, 1)
    rotation: fromAxisAndAngle(Qt.vector3d(1, 0, 0), 90)
  }

  components: [ planeMesh, gridMaterial, transform ]
}
