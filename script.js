// Initialize the scene
const scene = new THREE.Scene();

// Initialize the camera
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.z = 5;

// Initialize the renderer
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Initialize the GLTFLoader
const loader = new THREE.GLTFLoader();

// Load a brain model
loader.load('path/to/brain_model.gltf', function(gltf) {
    const brain = gltf.scene;
    brain.position.set(0, 0, 0);
    scene.add(brain);
}, undefined, function(error) {
    console.error(error);
});

// Load a heart model
loader.load('path/to/heart_model.gltf', function(gltf) {
    const heart = gltf.scene;
    heart.position.set(2, 0, 0);
    scene.add(heart);
}, undefined, function(error) {
    console.error(error);
});

// Load a liver model
loader.load('path/to/liver_model.gltf', function(gltf) {
    const liver = gltf.scene;
    liver.position.set(-2, 0, 0);
    scene.add(liver);
}, undefined, function(error) {
    console.error(error);
});

// Render the scene
function animate() {
    requestAnimationFrame(animate);

    // Optional: Rotate the models for better visualization
    scene.rotation.y += 0.01;

    renderer.render(scene, camera);
}
animate();

// Handle window resize
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});
