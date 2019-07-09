
import Qt3D.Core 2.0
import Qt3D.Render 2.0

Material {
    id: root

    property color diffuseColor: Qt.rgba( 0.0, 0.0, 0.0, 1.0 )

    effect: UnlitEffect {
      diffuseColor: root.diffuseColor
    }
}
