import QtQuick 2.0
import QtQuick.Scene3D 2.0

Item {

    Rectangle {
        id: scene
        anchors.fill: parent
        anchors.margins: 5
        color: '#206080'

        transform: Rotation {
            id: sceneRotation
            axis.x: 0
            axis.y: 0
            axis.z: 0
            origin.x: scene.width / 2
            origin.y: scene.height / 2
        }

        Scene3D {
            id: scene3d
            anchors.fill: parent
            anchors.margins: 10
            focus: true
            aspects: ["input", "logic"]
            cameraAspectRatioMode: Scene3D.AutomaticAspectRatio

            SceneEntity {}

        }
    } 
}
