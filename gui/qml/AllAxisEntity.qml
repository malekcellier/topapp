import Qt3D.Core 2.0
import Qt3D.Render 2.0
import Qt3D.Input 2.0
import Qt3D.Extras 2.0

import QtQuick 2.0 as QQ2

// This file creates the 3 axes x, y, z with z pointing up

Entity {

    Entity {
        AxisEntity {
            id: xaxis
            axisColor: 'red'        
        }

        Transform {
            id: xaxisTransform
            rotationZ: -90
        }
        id: xAxisEntity
        components: [xaxis, xaxisTransform]
    }

    Entity {
        AxisEntity {
            id: yaxis
            axisColor: 'green'        
        }
        id: yAxisEntity
        components: [yaxis]
    }

    Entity {
        AxisEntity {
            id: zaxis
            axisColor: 'blue'        
        }
            
        Transform {
            id: zaxisTransform
            rotationX: 90
        }
        id: zAxisEntity
        components: [zaxis, zaxisTransform]
    }

}