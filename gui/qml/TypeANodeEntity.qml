import Qt3D.Core 2.0
import Qt3D.Render 2.0
import Qt3D.Input 2.0
import Qt3D.Extras 2.0

import QtQuick 2.0 as QQ2

import "effects"

Entity {
    property point modelPosition: Qt.point(0, 0)
    
    WireframeMaterial {
        id: material
        effect: WireframeEffect {}
    }

    ConeMesh {
        id: coneMesh
        bottomRadius: 10
        topRadius: 5
        length: 20
        slices: 4
    }

    Transform {
        id: modelPositionTransform
        rotationX: 90
        translation: Qt.vector3d(modelPosition.x, modelPosition.y, coneMesh.length / 2)
    }

    Entity {
        components: [coneMesh, material, modelPositionTransform]
    }
}
