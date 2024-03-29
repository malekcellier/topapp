import Qt3D.Core 2.0
import Qt3D.Render 2.0
import Qt3D.Input 2.0
import Qt3D.Extras 2.0

import QtQuick 2.0 as QQ2
import "effects"

Entity {

    property color axisColor: 'black'
    
    UnlitMaterial {
        id: material
        diffuseColor: axisColor
    }

    CylinderMesh {
        id: cylinderMesh
        radius: 0.2
        length: 10
    }

    Transform {
        id: cylinderTransform
        translation: Qt.vector3d(0, cylinderMesh.length/2, 0)
    }

    Entity {
        components: [cylinderMesh, material, cylinderTransform]
    }

    ConeMesh {
        id: coneMesh
        bottomRadius: cylinderMesh.radius*4
        topRadius: 0
        length: cylinderMesh.length/3
    }

    Transform {
        id: coneTransform
        translation: Qt.vector3d(0, cylinderMesh.length + coneMesh.length/2, 0)
    }

    Entity {
        components: [coneMesh, material, coneTransform]
    }
}
