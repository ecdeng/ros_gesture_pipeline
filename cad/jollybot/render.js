// Headless three.js renderer for out/render/scene.json → PNGs. Usage: node render.js out/render
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const OUT = process.argv[2];
const THREE_SRC = fs.readFileSync(path.join(process.env.THREE_DIR || '/tmp/claude-0/-home-user-ros-gesture-pipeline/61a9b275-20a7-5366-acb2-cbafd1e99403/scratchpad/render/node_modules/three/build', 'three.min.js'), 'utf8');
const scene = fs.readFileSync(path.join(OUT, 'scene.json'), 'utf8');
const VIEWS = [
  { name: '01_front_quarter_skin', cam: [-330, 330, 260], skin: 0.28, clip: null, explode: 0 },
  { name: '02_front_quarter', cam: [-330, 330, 260], skin: 0, clip: null, explode: 0 },
  { name: '03_front', cam: [0.01, 520, 150], skin: 0, clip: null, explode: 0 },
  { name: '04_rear_quarter', cam: [300, -330, 240], skin: 0, clip: null, explode: 0 },
  { name: '05_half_section', cam: [380, 260, 230], skin: 0.35, clip: 'x', explode: 0 },
  { name: '06_exploded', cam: [-520, 520, 500], skin: 0, clip: null, explode: 1 },
];
const html = `<!doctype html><html><body style="margin:0;background:#F6F1E7"><canvas id="c" width="1600" height="1400"></canvas>
<script>${THREE_SRC}</script>
<script>
const bodies = ${scene};
const canvas = document.getElementById('c');
const renderer = new THREE.WebGLRenderer({canvas, antialias:true, preserveDrawingBuffer:true});
renderer.setSize(1600, 1400, false); renderer.localClippingEnabled = true; renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
const scene = new THREE.Scene(); scene.background = new THREE.Color('#F6F1E7');
scene.add(new THREE.HemisphereLight(0xffffff, 0x998877, 0.9));
const sun = new THREE.DirectionalLight(0xffffff, 1.6); sun.position.set(-250, 300, 500); sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048); const sc = sun.shadow.camera; sc.left = sc.bottom = -260; sc.right = sc.top = 260; sc.near = 10; sc.far = 1500;
scene.add(sun);
const fill = new THREE.DirectionalLight(0xffffff, 0.5); fill.position.set(300, -300, 200); scene.add(fill);
const ground = new THREE.Mesh(new THREE.PlaneGeometry(1200, 1200), new THREE.ShadowMaterial({opacity: 0.18}));
ground.position.z = -3.5; ground.receiveShadow = true; scene.add(ground);
const EXPLODE = { tray: 0, puck: 40, tilt: 90, head: 170, skin: 0 };
const meshes = [];
for (const b of bodies) {
  const g = new THREE.BufferGeometry();
  g.setAttribute('position', new THREE.Float32BufferAttribute(b.v, 3)); g.setIndex(b.t); g.computeVertexNormals();
  const isSkin = b.group === 'skin';
  const m = new THREE.MeshStandardMaterial({ color: b.color, roughness: isSkin ? 0.9 : 0.55, metalness: ['#8A94A0','#C9A24A'].includes(b.color) ? 0.6 : 0.05,
      transparent: isSkin, opacity: isSkin ? 0.3 : 1, side: THREE.DoubleSide, depthWrite: !isSkin });
  const mesh = new THREE.Mesh(g, m); mesh.castShadow = !isSkin; mesh.receiveShadow = true; mesh.userData = b; scene.add(mesh); meshes.push(mesh);
  if (!isSkin && ['#8FA8BF','#A6C4A0','#D9B58C','#C7B5D8'].includes(b.color)) {
    const edges = new THREE.LineSegments(new THREE.EdgesGeometry(g, 35), new THREE.LineBasicMaterial({color: 0x2b2622, transparent:true, opacity:0.35}));
    mesh.add(edges);
  }
}
const camera = new THREE.PerspectiveCamera(32, 1600/1400, 1, 5000); camera.up.set(0,0,1);
window.renderView = function(v) {
  const clip = v.clip ? [new THREE.Plane(new THREE.Vector3(-1,0,0), 0)] : null;
  for (const m of meshes) {
    const b = m.userData; const isSkin = b.group === 'skin';
    m.visible = !(isSkin && v.skin === 0);
    if (isSkin) m.material.opacity = v.skin;
    m.material.clippingPlanes = (clip && !isSkin) ? clip : null; m.material.clipShadows = true;
    m.position.z = v.explode ? EXPLODE[b.group] : 0;
    m.children.forEach(c => { c.material.clippingPlanes = clip && !isSkin ? clip : null; });
  }
  const target = new THREE.Vector3(0, 0, v.explode ? 200 : 100);
  camera.position.set(v.cam[0], v.cam[1], v.cam[2]); camera.lookAt(target);
  renderer.render(scene, camera);
  return renderer.info.render.triangles;
};
</script></body></html>`;
fs.writeFileSync(path.join(OUT, 'scene.html'), html);
(async () => {
  const browser = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader', '--ignore-gpu-blocklist'] });
  const page = await browser.newPage({ viewport: { width: 1600, height: 1400 } });
  page.on('pageerror', e => console.log('pageerror', e.message));
  await page.goto('file://' + path.join(OUT, 'scene.html'));
  await page.waitForFunction(() => typeof window.renderView === 'function', null, { timeout: 120000 });
  for (const v of VIEWS) {
    const tris = await page.evaluate(v => window.renderView(v), v);
    await page.screenshot({ path: path.join(OUT, v.name + '.png'), clip: { x: 0, y: 0, width: 1600, height: 1400 } });
    console.log(v.name, tris, 'triangles');
  }
  await browser.close();
})();
