// License: CC0 (http://creativecommons.org/publicdomain/zero/1.0/)
#extension GL_OES_standard_derivatives : enable

varying vec3 vertex;
uniform vec4 diffuse;

void main() {
  gl_FragColor = diffuse;
}
