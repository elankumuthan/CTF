function createMatrixRain() {
    const matrixBg = document.getElementById('matrixBg');
    const chars = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンERRORUPLOAD403DENIEDPERMISSION';

    for (let i = 0; i < 50; i++) {
        const char = document.createElement('div');
        char.className = 'matrix-char';
        char.textContent = chars[Math.floor(Math.random() * chars.length)];
        char.style.left = Math.random() * 100 + '%';
        char.style.animationDuration = (Math.random() * 3 + 2) + 's';
        char.style.animationDelay = Math.random() * 2 + 's';
        matrixBg.appendChild(char);
    }
}

function updateTimestamp() {
    const now = new Date();
    const el = document.getElementById('timestamp');
    if (el) {
        el.textContent = `TIME: ${now.toISOString().replace('T', ' ').split('.')[0]} UTC`;
    }
}

function addGlitchEffect() {
    const glitchElements = document.querySelectorAll('.glitch');
    glitchElements.forEach(el => {
        if (Math.random() < 0.1) {
            el.style.animation = 'none';
            setTimeout(() => {
                el.style.animation = 'glitch 0.5s infinite';
            }, 50);
        }
    });
}

document.addEventListener('DOMContentLoaded', function () {
    createMatrixRain();
    updateTimestamp();
    setInterval(updateTimestamp, 1000);
    setInterval(addGlitchEffect, 2000);
});

setInterval(() => {
    const matrixBg = document.getElementById('matrixBg');
    if (matrixBg && matrixBg.children.length < 50) {
        const chars = '01ACCESSDENIEDUPLOADFILEERRORRESTRICTEDVIOLATION';
        const char = document.createElement('div');
        char.className = 'matrix-char';
        char.textContent = chars[Math.floor(Math.random() * chars.length)];
        char.style.left = Math.random() * 100 + '%';
        char.style.animationDuration = (Math.random() * 3 + 2) + 's';
        matrixBg.appendChild(char);
    }
}, 1000);
