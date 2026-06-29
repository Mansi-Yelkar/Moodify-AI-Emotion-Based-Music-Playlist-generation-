// Harmonia Interactive Music Background
class HarmoniaBackground {
    constructor() {
        this.canvas = document.getElementById('harmonia-bg');
        if (!this.canvas) return;
        this.ctx = this.canvas.getContext('2d');
        
        this.particles = [];
        this.numParticles = 65;
        this.maxDistance = 130;
        this.mouse = { x: null, y: null, active: false };
        
        // Sound waves
        this.waves = [];
        this.numWaves = 3;
        
        // Equalizer visualizer bars
        this.eqBars = [];
        this.numBars = 45;
        
        this.init();
        this.resize();
        this.bindEvents();
        this.animate();
    }
    
    init() {
        // Init particles
        this.particles = [];
        for (let i = 0; i < this.numParticles; i++) {
            this.particles.push({
                x: Math.random() * window.innerWidth,
                y: Math.random() * window.innerHeight,
                vx: (Math.random() - 0.5) * 0.35,
                vy: (Math.random() - 0.5) * 0.35,
                radius: Math.random() * 2 + 1,
                color: Math.random() > 0.5 ? 'rgba(139, 92, 246, 0.45)' : 'rgba(56, 189, 248, 0.45)'
            });
        }
        
        // Init sound waves
        this.waves = [];
        for (let i = 0; i < this.numWaves; i++) {
            this.waves.push({
                radius: 0,
                maxRadius: 220 + i * 110,
                speed: 0.45 + Math.random() * 0.45,
                opacity: 0.12 - i * 0.03,
                grow: true
            });
        }
        
        // Init equalizer bars
        this.eqBars = [];
        for (let i = 0; i < this.numBars; i++) {
            this.eqBars.push({
                height: 5 + Math.random() * 25,
                speed: 0.08 + Math.random() * 0.08,
            });
        }
    }
    
    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }
    
    bindEvents() {
        window.addEventListener('resize', () => this.resize());
        
        window.addEventListener('mousemove', (e) => {
            this.mouse.x = e.clientX;
            this.mouse.y = e.clientY;
            this.mouse.active = true;
        });
        
        window.addEventListener('mouseleave', () => {
            this.mouse.x = null;
            this.mouse.y = null;
            this.mouse.active = false;
        });
    }
    
    drawParticles() {
        // Update and draw particles
        for (let i = 0; i < this.particles.length; i++) {
            const p = this.particles[i];
            
            p.x += p.vx;
            p.y += p.vy;
            
            // Boundary collisions
            if (p.x < 0 || p.x > this.canvas.width) p.vx *= -1;
            if (p.y < 0 || p.y > this.canvas.height) p.vy *= -1;
            
            this.ctx.beginPath();
            this.ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            this.ctx.fillStyle = p.color;
            this.ctx.fill();
        }
        
        // Draw constellation lines
        for (let i = 0; i < this.particles.length; i++) {
            for (let j = i + 1; j < this.particles.length; j++) {
                const p1 = this.particles[i];
                const p2 = this.particles[j];
                
                const dx = p1.x - p2.x;
                const dy = p1.y - p2.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                
                if (dist < this.maxDistance) {
                    const alpha = (1 - dist / this.maxDistance) * 0.14;
                    this.ctx.beginPath();
                    this.ctx.moveTo(p1.x, p1.y);
                    this.ctx.lineTo(p2.x, p2.y);
                    this.ctx.strokeStyle = `rgba(139, 92, 246, ${alpha})`;
                    this.ctx.lineWidth = 0.8;
                    this.ctx.stroke();
                }
            }
            
            // Connect to mouse if close
            if (this.mouse.active) {
                const p = this.particles[i];
                const dx = p.x - this.mouse.x;
                const dy = p.y - this.mouse.y;
                const dist = Math.sqrt(dx * dx + dy * dy);
                
                if (dist < this.maxDistance * 1.3) {
                    const alpha = (1 - dist / (this.maxDistance * 1.3)) * 0.18;
                    this.ctx.beginPath();
                    this.ctx.moveTo(p.x, p.y);
                    this.ctx.lineTo(this.mouse.x, this.mouse.y);
                    this.ctx.strokeStyle = `rgba(56, 189, 248, ${alpha})`;
                    this.ctx.lineWidth = 1;
                    this.ctx.stroke();
                }
            }
        }
    }
    
    drawWaves() {
        const centerX = this.canvas.width * 0.35;
        const centerY = this.canvas.height * 0.45;
        
        for (let i = 0; i < this.waves.length; i++) {
            const w = this.waves[i];
            
            if (w.grow) {
                w.radius += w.speed;
                if (w.radius > w.maxRadius) {
                    w.radius = 0;
                }
            }
            
            this.ctx.beginPath();
            this.ctx.arc(centerX, centerY, w.radius, 0, Math.PI * 2);
            
            const currentOpacity = w.opacity * (1 - w.radius / w.maxRadius);
            this.ctx.strokeStyle = `rgba(139, 92, 246, ${currentOpacity})`;
            this.ctx.lineWidth = 1.5;
            this.ctx.stroke();
        }
    }
    
    drawEqualizer() {
        const barWidth = 6;
        const gap = 4;
        const totalWidth = (barWidth + gap) * this.numBars - gap;
        const startX = (this.canvas.width - totalWidth) / 2;
        const startY = this.canvas.height - 20;
        
        const time = Date.now() * 0.0012;
        
        for (let i = 0; i < this.numBars; i++) {
            const bar = this.eqBars[i];
            
            // Pulsate based on compound math equations (visualizes sound wave variance)
            const factor = Math.sin(time * 2.5 + i * 0.12) * Math.cos(time * 1.2 + i * 0.08);
            const heightMultiplier = Math.max(0.1, (factor + 1) / 2);
            
            bar.height += (heightMultiplier * 55 - bar.height) * bar.speed;
            
            const ratio = i / this.numBars;
            const r = Math.floor(139 + ratio * 85);
            const g = Math.floor(92 - ratio * 45);
            const b = Math.floor(246 - ratio * 105);
            
            this.ctx.fillStyle = `rgba(${r}, ${g}, ${b}, 0.22)`;
            
            const x = startX + i * (barWidth + gap);
            const y = startY - bar.height;
            
            this.ctx.beginPath();
            if (typeof this.ctx.roundRect === 'function') {
                this.ctx.roundRect(x, y, barWidth, bar.height, 3);
            } else {
                this.ctx.rect(x, y, barWidth, bar.height);
            }
            this.ctx.fill();
        }
    }
    
    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        this.drawWaves();
        this.drawParticles();
        this.drawEqualizer();
        
        requestAnimationFrame(() => this.animate());
    }
}

// Instantiate on load
document.addEventListener('DOMContentLoaded', () => {
    new HarmoniaBackground();
});
