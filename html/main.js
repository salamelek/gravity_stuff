const G = 6.67430e-11;

let particles = [];
let canvas;
let ctx;
let canvasWidth;
let canvasHeight;

function sleep(milliseconds) {
    return new Promise(resolve => setTimeout(resolve, milliseconds));
}

class Particle {
    x;
    y;
    r;
    vx;
    vy;
    fx;
    fy;
    mass;

    constructor(x, y, r=5, vx=0, vy=0, fx=0, fy=0, mass=1) {
        this.x = x;
        this.y = y;
        this.r = r;
        this.vx = vx;
        this.vy = vy;
        this.fx = fx;
        this.fy = fy;
        this.mass = mass;
    }
}

function run() {
    canvas = document.getElementById("myCanvas");
    ctx = canvas.getContext("2d");

    canvasWidth = document.getElementById("canvas-div").offsetWidth;
    canvasHeight = document.getElementById("canvas-div").offsetHeight;

    particles.push(
        new Particle(100, 100),
        new Particle(500, 500)
    );

    window.requestAnimationFrame(update);
}

async function update() {
    ctx.canvas.width = canvasWidth;
    ctx.canvas.height = canvasHeight;

    for (let i=0; i<particles.length; i++) {
        let particle = particles[i];

        ctx.fillRect(particle.x, particle.y, particle.r, particle.r);

        particle.ax = particle.fx / particle.mass;
        particle.ay = particle.fy / particle.mass;

        particle.vx += particle.ax;
        particle.vy += particle.ay;

        particle.x += particle.vx;
        particle.y += particle.vy;

        particle.fx = 0;
        particle.fy = 0;
    }

    for (let i=0; i<particles.length; i++) {
        for (let j=0; i<(particles.length - (i + 1)); j++) {
            let a = particles[i];
            let b = particles[i + j + 1];

            // TODO WTF WHY IS B UNDEFINED AND WHY DOES EVERYTHING CRASH
            let r = Math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2);
            let f = G * ((a.mass * b.mass) / r ** 2);
            a.Fx += ((b.x - a.x) * f) / r;
            a.Fy += ((b.y - a.y) * f) / r;
            b.Fx += ((a.x - b.x) * f) / r;
            b.Fy += ((a.y - b.y) * f) / r;
        }
    }

    // window.requestAnimationFrame(update);
}