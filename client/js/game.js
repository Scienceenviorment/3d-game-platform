// 3D Game Client
class GameClient {
    constructor() {
        // Three.js setup
        this.scene = null;
        this.camera = null;
        this.renderer = null;
        this.controls = null;
        
        // Game state
        this.playerId = this.generatePlayerId();
        this.playerName = `Player_${this.playerId.substring(0, 8)}`;
        this.players = new Map();
        this.worldChunks = new Map();
        
        // Network
        this.socket = null;
        this.connected = false;
        
        // Input
        this.keys = {};
        this.mousePressed = false;
        this.pointerLocked = false;
        
        // Player movement
        this.velocity = new THREE.Vector3();
        this.moveSpeed = 20;
        this.jumpSpeed = 10;
        this.gravity = -30;
        this.onGround = false;
        
        // Initialize
        this.init();
    }

    generatePlayerId() {
        return Math.random().toString(36).substring(2) + Date.now().toString(36);
    }

    init() {
        this.setupThreeJS();
        this.setupControls();
        this.createWorld();
        this.connectToServer();
        this.animate();
        
        // Hide loading screen after a short delay
        setTimeout(() => {
            document.getElementById('loadingScreen').classList.add('hidden');
        }, 2000);
    }

    setupThreeJS() {
        // Scene
        this.scene = new THREE.Scene();
        this.scene.fog = new THREE.Fog(0xcccccc, 100, 1000);

        // Camera
        this.camera = new THREE.PerspectiveCamera(
            75, 
            window.innerWidth / window.innerHeight, 
            0.1, 
            1000
        );
        this.camera.position.set(0, 5, 10);

        // Renderer
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.setClearColor(0x87CEEB);
        this.renderer.shadowMap.enabled = true;
        this.renderer.shadowMap.type = THREE.PCFSoftShadowMap;
        
        document.getElementById('gameContainer').appendChild(this.renderer.domElement);

        // Lighting
        const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
        this.scene.add(ambientLight);

        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
        directionalLight.position.set(50, 100, 50);
        directionalLight.castShadow = true;
        directionalLight.shadow.mapSize.width = 2048;
        directionalLight.shadow.mapSize.height = 2048;
        this.scene.add(directionalLight);

        // Handle window resize
        window.addEventListener('resize', () => {
            this.camera.aspect = window.innerWidth / window.innerHeight;
            this.camera.updateProjectionMatrix();
            this.renderer.setSize(window.innerWidth, window.innerHeight);
        });
    }

    setupControls() {
        // Keyboard controls
        document.addEventListener('keydown', (event) => {
            this.keys[event.code] = true;
            
            if (event.code === 'Enter') {
                this.toggleChat();
            } else if (event.code === 'Escape') {
                this.exitPointerLock();
            }
        });

        document.addEventListener('keyup', (event) => {
            this.keys[event.code] = false;
        });

        // Mouse controls
        document.addEventListener('click', () => {
            if (!this.pointerLocked) {
                this.requestPointerLock();
            }
        });

        document.addEventListener('pointerlockchange', () => {
            this.pointerLocked = document.pointerLockElement === this.renderer.domElement;
        });

        document.addEventListener('mousemove', (event) => {
            if (this.pointerLocked) {
                const sensitivity = 0.002;
                this.camera.rotation.y -= event.movementX * sensitivity;
                this.camera.rotation.x -= event.movementY * sensitivity;
                this.camera.rotation.x = Math.max(-Math.PI/2, Math.min(Math.PI/2, this.camera.rotation.x));
            }
        });

        // Chat input
        const chatInput = document.getElementById('chatInput');
        chatInput.addEventListener('keydown', (event) => {
            if (event.code === 'Enter') {
                const message = chatInput.value.trim();
                if (message && this.connected) {
                    this.sendMessage({
                        type: 'chat',
                        message: message
                    });
                    chatInput.value = '';
                }
                this.toggleChat();
                event.preventDefault();
            } else if (event.code === 'Escape') {
                this.toggleChat();
                event.preventDefault();
            }
        });
    }

    createWorld() {
        // Ground plane
        const groundGeometry = new THREE.PlaneGeometry(1000, 1000);
        const groundMaterial = new THREE.MeshLambertMaterial({ color: 0x90EE90 });
        const ground = new THREE.Mesh(groundGeometry, groundMaterial);
        ground.rotation.x = -Math.PI / 2;
        ground.receiveShadow = true;
        this.scene.add(ground);

        // Add some basic scenery
        this.addTrees();
        this.addRocks();
    }

    addTrees() {
        for (let i = 0; i < 50; i++) {
            const tree = this.createTree();
            tree.position.set(
                (Math.random() - 0.5) * 800,
                0,
                (Math.random() - 0.5) * 800
            );
            this.scene.add(tree);
        }
    }

    createTree() {
        const group = new THREE.Group();

        // Trunk
        const trunkGeometry = new THREE.CylinderGeometry(1, 2, 8);
        const trunkMaterial = new THREE.MeshLambertMaterial({ color: 0x8B4513 });
        const trunk = new THREE.Mesh(trunkGeometry, trunkMaterial);
        trunk.position.y = 4;
        trunk.castShadow = true;
        group.add(trunk);

        // Leaves
        const leavesGeometry = new THREE.SphereGeometry(6);
        const leavesMaterial = new THREE.MeshLambertMaterial({ color: 0x228B22 });
        const leaves = new THREE.Mesh(leavesGeometry, leavesMaterial);
        leaves.position.y = 10;
        leaves.castShadow = true;
        group.add(leaves);

        return group;
    }

    addRocks() {
        for (let i = 0; i < 30; i++) {
            const rock = this.createRock();
            rock.position.set(
                (Math.random() - 0.5) * 800,
                0,
                (Math.random() - 0.5) * 800
            );
            this.scene.add(rock);
        }
    }

    createRock() {
        const geometry = new THREE.DodecahedronGeometry(2 + Math.random() * 3);
        const material = new THREE.MeshLambertMaterial({ color: 0x696969 });
        const rock = new THREE.Mesh(geometry, material);
        rock.castShadow = true;
        rock.receiveShadow = true;
        return rock;
    }

    connectToServer() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const host = window.location.hostname === 'localhost' ? 'localhost:8000' : window.location.host;
        
        this.socket = new WebSocket(`${protocol}//${host}/ws`);

        this.socket.onopen = () => {
            console.log('Connected to game server');
            this.connected = true;
            this.updateConnectionStatus('connected');
            
            // Send initial connection message
            this.sendMessage({
                type: 'connect',
                player_id: this.playerId,
                player_name: this.playerName
            });
        };

        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };

        this.socket.onclose = () => {
            console.log('Disconnected from game server');
            this.connected = false;
            this.updateConnectionStatus('disconnected');
            
            // Attempt to reconnect after 3 seconds
            setTimeout(() => {
                if (!this.connected) {
                    this.connectToServer();
                }
            }, 3000);
        };

        this.socket.onerror = (error) => {
            console.error('WebSocket error:', error);
            this.updateConnectionStatus('disconnected');
        };
    }

    sendMessage(data) {
        if (this.socket && this.socket.readyState === WebSocket.OPEN) {
            this.socket.send(JSON.stringify(data));
        }
    }

    handleMessage(data) {
        switch (data.type) {
            case 'welcome':
                console.log('Welcome message received');
                break;
                
            case 'player_joined':
                this.addPlayer(data.player);
                this.addChatMessage(`${data.player.name} joined the game`);
                break;
                
            case 'player_left':
                this.removePlayer(data.player_id);
                break;
                
            case 'player_moved':
                this.updatePlayerPosition(data.player_id, data.position, data.rotation);
                break;
                
            case 'chat':
                this.addChatMessage(`${data.player_name}: ${data.message}`);
                break;
        }
        
        this.updatePlayerCount();
    }

    addPlayer(playerData) {
        if (playerData.id === this.playerId) return;

        // Create player representation
        const geometry = new THREE.CapsuleGeometry(1, 3);
        const material = new THREE.MeshLambertMaterial({ 
            color: this.generatePlayerColor(playerData.id) 
        });
        const playerMesh = new THREE.Mesh(geometry, material);
        playerMesh.castShadow = true;
        playerMesh.receiveShadow = true;

        // Add name tag
        const nameTag = this.createNameTag(playerData.name);
        nameTag.position.y = 4;
        playerMesh.add(nameTag);

        playerMesh.position.set(
            playerData.position.x,
            playerData.position.y + 2,
            playerData.position.z
        );

        this.scene.add(playerMesh);
        this.players.set(playerData.id, {
            mesh: playerMesh,
            data: playerData
        });
    }

    removePlayer(playerId) {
        if (this.players.has(playerId)) {
            const player = this.players.get(playerId);
            this.scene.remove(player.mesh);
            this.players.delete(playerId);
            this.addChatMessage(`${player.data.name} left the game`);
        }
    }

    updatePlayerPosition(playerId, position, rotation) {
        if (this.players.has(playerId)) {
            const player = this.players.get(playerId);
            player.mesh.position.set(position.x, position.y + 2, position.z);
            
            if (rotation) {
                player.mesh.rotation.set(rotation.x, rotation.y, rotation.z);
            }
        }
    }

    generatePlayerColor(playerId) {
        // Generate a consistent color based on player ID
        let hash = 0;
        for (let i = 0; i < playerId.length; i++) {
            hash = playerId.charCodeAt(i) + ((hash << 5) - hash);
        }
        
        const hue = Math.abs(hash % 360);
        return new THREE.Color().setHSL(hue / 360, 0.7, 0.5);
    }

    createNameTag(name) {
        // Create a simple name tag using a plane
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        canvas.width = 256;
        canvas.height = 64;
        
        context.fillStyle = 'rgba(0, 0, 0, 0.8)';
        context.fillRect(0, 0, canvas.width, canvas.height);
        
        context.fillStyle = 'white';
        context.font = '24px Arial';
        context.textAlign = 'center';
        context.fillText(name, canvas.width / 2, canvas.height / 2 + 8);
        
        const texture = new THREE.CanvasTexture(canvas);
        const material = new THREE.MeshBasicMaterial({ 
            map: texture, 
            transparent: true 
        });
        const geometry = new THREE.PlaneGeometry(4, 1);
        const nameTag = new THREE.Mesh(geometry, material);
        
        return nameTag;
    }

    updateMovement(deltaTime) {
        if (!this.pointerLocked) return;

        const moveVector = new THREE.Vector3();
        
        // Calculate movement direction
        if (this.keys['KeyW']) moveVector.z -= 1;
        if (this.keys['KeyS']) moveVector.z += 1;
        if (this.keys['KeyA']) moveVector.x -= 1;
        if (this.keys['KeyD']) moveVector.x += 1;

        // Normalize movement vector
        if (moveVector.length() > 0) {
            moveVector.normalize();
            
            // Apply camera rotation to movement
            const cameraDirection = new THREE.Vector3();
            this.camera.getWorldDirection(cameraDirection);
            
            const forward = new THREE.Vector3(cameraDirection.x, 0, cameraDirection.z).normalize();
            const right = new THREE.Vector3().crossVectors(forward, new THREE.Vector3(0, 1, 0));
            
            const movement = new THREE.Vector3()
                .addScaledVector(forward, moveVector.z)
                .addScaledVector(right, moveVector.x)
                .multiplyScalar(this.moveSpeed * deltaTime);
            
            this.camera.position.add(movement);
            
            // Send movement to server
            if (this.connected) {
                this.sendMessage({
                    type: 'move',
                    position: {
                        x: this.camera.position.x,
                        y: this.camera.position.y,
                        z: this.camera.position.z
                    },
                    rotation: {
                        x: this.camera.rotation.x,
                        y: this.camera.rotation.y,
                        z: this.camera.rotation.z
                    }
                });
            }
        }

        // Jumping
        if (this.keys['Space'] && this.onGround) {
            this.velocity.y = this.jumpSpeed;
            this.onGround = false;
        }

        // Apply gravity
        this.velocity.y += this.gravity * deltaTime;
        this.camera.position.y += this.velocity.y * deltaTime;

        // Ground collision
        if (this.camera.position.y <= 2) {
            this.camera.position.y = 2;
            this.velocity.y = 0;
            this.onGround = true;
        }
    }

    requestPointerLock() {
        this.renderer.domElement.requestPointerLock();
    }

    exitPointerLock() {
        document.exitPointerLock();
    }

    toggleChat() {
        const chatInput = document.getElementById('chatInput');
        
        if (chatInput.style.display === 'none') {
            chatInput.style.display = 'block';
            chatInput.focus();
            this.exitPointerLock();
        } else {
            chatInput.style.display = 'none';
            chatInput.blur();
        }
    }

    addChatMessage(message) {
        const chatMessages = document.getElementById('chatMessages');
        const messageElement = document.createElement('div');
        messageElement.textContent = message;
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Limit chat history
        while (chatMessages.children.length > 50) {
            chatMessages.removeChild(chatMessages.firstChild);
        }
    }

    updateConnectionStatus(status) {
        const statusElement = document.getElementById('connectionStatus');
        statusElement.className = status;
        
        switch (status) {
            case 'connected':
                statusElement.textContent = 'Connected';
                break;
            case 'connecting':
                statusElement.textContent = 'Connecting...';
                break;
            case 'disconnected':
                statusElement.textContent = 'Disconnected';
                break;
        }
    }

    updatePlayerCount() {
        const count = this.players.size + (this.connected ? 1 : 0);
        document.getElementById('playerCount').textContent = count;
    }

    animate() {
        requestAnimationFrame(() => this.animate());

        const deltaTime = 1/60; // Approximate 60fps
        
        this.updateMovement(deltaTime);
        
        // Make name tags always face camera
        this.players.forEach(player => {
            const nameTag = player.mesh.children[0];
            if (nameTag) {
                nameTag.lookAt(this.camera.position);
            }
        });

        this.renderer.render(this.scene, this.camera);
    }
}

// Start the game when page loads
window.addEventListener('load', () => {
    new GameClient();
});