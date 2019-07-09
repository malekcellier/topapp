import Qt3D.Core 2.0
import Qt3D.Render 2.0

Effect {
    id: root

    property color diffuseColor: "white"

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
                Parameter { name: "diffuse"; value: Qt.vector4d(
                                                        diffuseColor.r,
                                                        diffuseColor.g,
                                                        diffuseColor.b,
                                                        diffuseColor.a) }
            ]

            renderPasses: [
                RenderPass {
                    shaderProgram: ShaderProgram {
                        vertexShaderCode:   loadSource(Qt.resolvedUrl("../../shaders/unlit.vert"))
                        fragmentShaderCode: loadSource(Qt.resolvedUrl("../../shaders/unlit.frag"))
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
                        BlendEquation { blendFunction: BlendEquation.TrackFinalValues }
                    ]
                }
            ]
        }
    ]
}
