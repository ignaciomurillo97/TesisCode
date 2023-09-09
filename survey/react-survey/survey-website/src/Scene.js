import React, { useRef, useEffect } from 'react';
import { Canvas, useLoader, useFrame } from '@react-three/fiber';
import * as THREE from 'three';

function Heightmap({ heightmapPath }) {
  const meshRef = useRef();
  const texture = useLoader(THREE.TextureLoader, heightmapPath);

  useEffect(() => {
    if (meshRef.current && texture) {
      const geometry = meshRef.current.geometry;
      const vertices = geometry.attributes.position.array;
      const canvas = document.createElement('canvas');
      const context = canvas.getContext('2d');
      
      canvas.width = texture.image.width;
      canvas.height = texture.image.height;
      context.drawImage(texture.image, 0, 0);

      const imageData = context.getImageData(0, 0, canvas.width, canvas.height).data;

      for (let i = 0, j = 0; i < vertices.length; i += 3, j += 4) {
        const intensity = 50 * imageData[j] / 255.0;  // Assuming a grayscale heightmap
        //if (i % 10 === 0 & j % 10 === 0) console.log('intensity', intensity);
        vertices[i + 2] = intensity; // Scale for height displacement
      }

      geometry.attributes.position.needsUpdate = true;
    }
  }, [texture]);

  useFrame(() => {
    if (meshRef.current) {
      meshRef.current.rotation.z += 0.001;
    }
  });

  return (
    <mesh ref={meshRef} geometry={new THREE.PlaneGeometry(texture.image.width, texture.image.height, texture.image.width - 1, texture.image.height - 1)} rotation={[-Math.PI / 2, 0, 0]} castShadow receiveShadow>
      <meshPhongMaterial attach="material" color="green" shadowSide={THREE.DoubleSide} flatShading shadows castShadow receiveShadow/>
    </mesh>
  );
}

function Scene(props) {
  return (
    <Canvas aspect={1} camera={{ aspect: 1, position: [0, 10, 30], rotation: [0, 0, 0], fov: 30 }} shadows>
      <directionalLight position={[10,50,0]} intensity={2} castShadow />
      <Heightmap heightmapPath={props.heightmapPath} />
    </Canvas>
  );
}

export default Scene;
