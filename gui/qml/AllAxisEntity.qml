import Qt3D.Core 2.0
import Qt3D.Render 2.0
import Qt3D.Input 2.0
import Qt3D.Extras 2.0

import QtQuick 2.0 as QQ2

// This file creates the 3 axes x, y, z with y pointing up

Entity {
    property vector3d axesPosition: Qt.vector3d(0, 0, 0)
    property real axesScale: 1


    Entity {
        AxisEntity {
            id: xaxis
            axisColor: 'red'        
        }

        Transform {
            id: xaxisTransform
            rotationZ: -90
            translation: axesPosition
            scale3D: Qt.vector3d(axesScale, axesScale, axesScale)
        }

        id: xAxisEntity
        components: [xaxis, xaxisTransform]
    }

    Entity {
        AxisEntity {
            id: yaxis
            axisColor: 'green'        
        }

        Transform {
            id: yaxisTransform
            translation: axesPosition
            scale3D: Qt.vector3d(axesScale, axesScale, axesScale)
        }
        id: yAxisEntity
        components: [yaxis, yaxisTransform]
    }

    Entity {
        AxisEntity {
            id: zaxis
            axisColor: 'blue'        
        }
            
        Transform {
            id: zaxisTransform
            rotationX: 90
            translation: axesPosition
            scale3D: Qt.vector3d(axesScale, axesScale, axesScale)
        }
        id: zAxisEntity
        components: [zaxis, zaxisTransform]
    }

}
