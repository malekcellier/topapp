
import QtQuick 2.0

import Qt3D.Core 2.0
import Qt3D.Render 2.0
import Qt3D.Input 2.0
import Qt3D.Extras 2.0

import "."
import "nodes"

Entity {
    id: sceneRoot

    property point maxModelPosition: Qt.point(0, 0)
    property point minModelPosition: Qt.point(0, 0)

    Camera {
        id: camera
        projectionType: CameraLens.PerspectiveProjection
        fieldOfView: 45
        nearPlane : 0.1
        farPlane : 10000.0
        position: Qt.vector3d( 200.0, 100, 200.0 )
        upVector: Qt.vector3d( 0.0, 1.0, 0.0 )
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

    Component {
        id: typeAComponent

        TypeANodeEntity {
            modelPosition { x: modelData.x; y: modelData.y }
            onModelPositionChanged: updateModelBounds(modelPosition)
        }
    }

    Component {
        id: typeBComponent

        TypeBNodeEntity {
            modelPosition { x: modelData.x; y: modelData.y }
            onModelPositionChanged: updateModelBounds(modelPosition)
        }
    }

    Component {
        id: typeCComponent

        TypeCNodeEntity {
            modelPosition { x: modelData.x; y: modelData.y }
            onModelPositionChanged: updateModelBounds(modelPosition)
        }
    }

    // in 3D, use NodeInstantiator instead of Repeater
    // topologyModle is a list of nodes, which contain a list of positions, which contain a list of X/Y coordinates:
    NodeInstantiator {
        id: instantiator
        model: topologyModel.nodes

        property var componentMap: ({
                                        "type_a": typeAComponent,
                                        "type_b": typeBComponent
                                    })

        NodeInstantiator {
            id: node
            model: modelData.positions
            property string nodeType: modelData.nodeType
            onNodeTypeChanged: console.log("type", nodeType)

            NodeInstantiator {
                id: pos
                property var xPositions: modelData.x
                property var yPositions: modelData.y

                model: xPositions.map(function(x, i) {
                    return Qt.point(xPositions[i], yPositions[i])
                })
                delegate: instantiator.componentMap[node.nodeType] || typeAComponent
            }
        }
    }

    Grid {
        id: grid
        width: maxModelPosition.x - minModelPosition.x
        height: maxModelPosition.y - minModelPosition.y
        gridResolution: 0.05
    }

    AllAxisEntity {
        id: allaxis
        axesScale: (axesPosition.minus(camera.position)).length() / 80
    }

    function updateModelBounds(modelPosition) {
        maxModelPosition = Qt.point(
                    Math.max(modelPosition.x, maxModelPosition.x),
                    Math.max(modelPosition.y, maxModelPosition.y)
                    )
        minModelPosition = Qt.point(
                    Math.min(modelPosition.x, minModelPosition.x),
                    Math.min(modelPosition.y, minModelPosition.y)
                    )
    }
}
