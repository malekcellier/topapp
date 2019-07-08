import Qt3D.Core 2.0
import Qt3D.Render 2.0

Effect {
  id: root

  property real lineWidth: 1.0
  property real gridResolution: 1.0
  property color lineColor: "white"

  techniques: [
    Technique {
      graphicsApiFilter {
        api: GraphicsApiFilter.OpenGL
        profile: GraphicsApiFilter.CoreProfile
        majorVersion: 3
        minorVersion: 1
      }

      filterKeys: [ FilterKey { name: "renderingStyle"; value: "forward" } ]

      parameters: [
        Parameter { name: "lineWidth"; value: lineWidth },
        Parameter { name: "gridResolution"; value: gridResolution },
        Parameter { name: "lineColor"; value: Qt.vector4d(
                                                lineColor.r,
                                                lineColor.g,
                                                lineColor.b,
                                                lineColor.a) }
      ]

      renderPasses: [
        RenderPass {
          shaderProgram: ShaderProgram {
            vertexShaderCode:   loadSource(Qt.resolvedUrl("../../shaders/grid.vert"))
            fragmentShaderCode: loadSource(Qt.resolvedUrl("../../shaders/grid.frag"))
          }
          renderStates: [
            CullFace { mode: CullFace.NoCulling },
            DepthTest { depthFunction: DepthTest.Less },
            BlendEquationArguments {
              sourceRgb: BlendEquationArguments.SourceAlpha
              destinationRgb: BlendEquationArguments.OneMinusSourceAlpha
              sourceAlpha: BlendEquationArguments.SourceAlpha
              destinationAlpha: BlendEquationArguments.OneMinusSourceAlpha
            },
            BlendEquation { blendFunction: BlendEquation.DontTrackValues }
          ]
        }
      ]
    }
  ]
}
