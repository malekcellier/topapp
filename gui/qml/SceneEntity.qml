
import QtQuick 2.0

import Qt3D.Core 2.0
import Qt3D.Render 2.0
import Qt3D.Input 2.0
import Qt3D.Extras 2.0

import "."

Entity {
    id: sceneRoot

    Camera {
        id: camera
        projectionType: CameraLens.PerspectiveProjection
        fieldOfView: 45
        nearPlane : 0.1
        farPlane : 1000.0
        position: Qt.vector3d( 100.0, 100, 45.0 )
        upVector: Qt.vector3d( 0.0, 0.0, 1.0 )
        viewCenter: Qt.vector3d( 0.0, 0.0, 0.0 )
    }

    OrbitCameraController { 
        camera: camera
        lookSpeed: 1000
        linearSpeed: 1000
        }

    components: [
        RenderSettings {
            activeFrameGraph: ForwardRenderer {
                camera: camera
                clearColor: "transparent"
            }
        },
        InputSettings { }
    ]

    PhongMaterial {
        id: material
    }



    // in 3D, use NodeInstantiator instead of Repeater
    // topologyModle is a list of nodes, which contain a list of positions, which contain a list of X/Y coordinates:
    NodeInstantiator {
        model: topologyModel.nodes

        NodeInstantiator {
            model: modelData.positions

            NodeInstantiator {
                id: pos
                property var xPositions: modelData.x
                property var yPositions: modelData.y
                model: xPositions.length

                TypeANodeEntity {
                    modelPosition {
                        x: pos.xPositions[index]
                        y: pos.yPositions[index]
                    }
                }
            }
        }
    }

    Grid {
        id: grid
        height: 100
        width: 100
        transform3d.rotationX: 90
    }

    AllAxisEntity {
        id: allaxis
    }

}
