// ===== REAL TIME CLOCK =====
function updateClock() {
    const now = new Date();
    const options = { 
        day: '2-digit', month: 'short', year: 'numeric',
        hour: '2-digit', minute: '2-digit', second: '2-digit',
        hour12: true 
    };
    const timeStr = now.toLocaleString('en-IN', options);
    const el = document.getElementById('live-clock');
    if (el) el.textContent = timeStr;
}
setInterval(updateClock, 1000);
updateClock();

// ===== BLOCKCHAIN STATUS DOT =====
function showBlockchainStatus() {
    const el = document.getElementById('blockchain-status');
    if (el) {
        el.innerHTML = `<span class="status-dot"></span> Blockchain: Live`;
    }
}
showBlockchainStatus();