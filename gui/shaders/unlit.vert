#version 330 core

in vec3 vertexPosition;
in vec3 vertexNormal;

out EyeSpaceVertex {
    vec3 position;
    vec3 normal;
} vs_out;

uniform mat4 modelView;
uniform mat3 modelViewNormal;
uniform mat4 mvp;
varying vec3 vertex;

void main()
{
    vs_out.normal = normalize( modelViewNormal * vertexNormal );
    vs_out.position = vec3( modelView * vec4( vertexPosition, 1.0 ) );

    vertex = vertexPosition;
    gl_Position = mvp * vec4( vertexPosition, 1.0 );

    // always on top
    gl_Position.z = 0;
}
