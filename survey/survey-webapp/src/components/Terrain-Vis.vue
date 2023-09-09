<template>
  <div class="three-container" ref="container"></div>
</template>

<script>
import * as THREE from 'three';

export default {
  name: 'TerrainVis',
  props: {
    heightmap: {
      type: String,
      required: true
    },
    strength: {
      type: Number,
      default: 5
    }
  },
  mounted() {
    // Create a Three.js scene
    const scene = new THREE.Scene();

    // Create a Three.js camera
    const camera = new THREE.PerspectiveCamera(75, this.$refs.container.clientWidth / this.$refs.container.clientHeight, 0.1, 1000);
    camera.position.set(0, 1, 10);

    // Create a Three.js renderer
    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(this.$refs.container.clientWidth, this.$refs.container.clientHeight);
    this.$refs.container.appendChild(renderer.domElement);

    // Load the heightmap texture
    const loader = new THREE.TextureLoader();
    loader.load(this.heightmap, (texture) => {
      // Create a Three.js plane geometry
      const width = texture.image.width;
      const height = texture.image.height;
      const geometry = new THREE.PlaneGeometry(40, 40, width - 1, height - 1);

      // Create a Three.js material
      const material = new THREE.MeshStandardMaterial({
        color: 0xffffff,
        //displacementMap: texture,
        //displacementScale: this.strength,
        roughness: 0.8,
        metalness: 0.2
      });

      // Read the pixel data from the heightmap texture using a canvas element
      const canvas = document.createElement('canvas');
      canvas.width = width;
      canvas.height = height;
      const context = canvas.getContext('2d');
      context.drawImage(texture.image, 0, 0);
      const imageData = context.getImageData(0, 0, width, height).data;

      // Adjust the vertices to match the heightmap
      const vertices = geometry.attributes.position.array;
      for (let i = 0; i < vertices.length; i += 3) {
        const x = (i / 3) % width;
        const y = Math.floor((i / 3) / width);
        const height = imageData[(y * width + x) * 4] / 255;
        vertices[i + 2] = height * this.strength;
      }
      geometry.computeVertexNormals();

      // Create a Three.js mesh
      const mesh = new THREE.Mesh(geometry, material);
      mesh.rotation.x = -Math.PI / 2;
      scene.add(mesh);

      // Create a Three.js directional light
      const light = new THREE.DirectionalLight(0xffffff, 1);
      light.position.set(0, 1, 1);
      light.rotateX(-Math.PI / 4)
      light.rotateZ(-Math.PI / 4)
      scene.add(light);

      // Set background color to blue
      renderer.setClearColor(0x6699ff);

      // Render the scene
      renderer.render(scene, camera);
    });
  }
}
</script>

<style>
div.three-container {
  width: 400px;
  height: 400px;
}
</style>