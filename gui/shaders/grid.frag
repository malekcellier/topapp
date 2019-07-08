// License: CC0 (http://creativecommons.org/publicdomain/zero/1.0/)
#extension GL_OES_standard_derivatives : enable

varying vec3 vertex;
uniform float lineWidth;
uniform vec4 lineColor;
uniform float gridResolution;

void main() {
  // Pick a coordinate to visualize in a grid
  vec2 coord = vertex.xz * gridResolution;

  // Compute anti-aliased world-space grid lines
  vec2 grid = abs(fract(coord - 0.5) - 0.5) / fwidth(coord) / lineWidth;
  float line = min(grid.x, grid.y);

  // Just visualize the grid lines directly
  float intensity = 1.0 - min(line, 1.0);
  gl_FragColor = vec4(1, 1, 1, intensity) * lineColor;
}
