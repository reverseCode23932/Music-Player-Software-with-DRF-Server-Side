// --- Global Token Storage (Must be outside any function/listener) ---
let userAccessToken = null; 
let userRefreshToken = null; 

// --- Helper for Authorization Headers ---
function getAuthHeaders() {
    if (userAccessToken) {
        return {
            'Authorization': `Bearer ${userAccessToken}` 
        };
    }
    return {};
}

// --- Popup Control Functions (Must be globally accessible or passed) ---
// These functions look up the elements every time they are called.
function showLogin() {
    const loginPopup = document.getElementById('loginPopup');
    const loginOverlay = document.getElementById('loginOverlay');
    if (loginPopup) loginPopup.style.display = 'flex'; // Use 'flex' for vertical stacking via CSS
    if (loginOverlay) loginOverlay.style.display = 'block';
}

function hideLogin() {
    const loginPopup = document.getElementById('loginPopup');
    const loginOverlay = document.getElementById('loginOverlay');
    if (loginPopup) loginPopup.style.display = 'none';
    if (loginOverlay) loginOverlay.style.display = 'none';
}

// --- Login Handler ---
async function handleLogin() {
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    
    // Check if elements exist and have values
    const username = usernameInput ? usernameInput.value : '';
    const password = passwordInput ? passwordInput.value : '';

    if (!window.api || !window.api.login) {
         console.error("Login API is not defined.");
         alert("Login functionality is not available.");
         return;
    }

    const result = await window.api.login("http://127.0.0.1:8000/token/", { username, password });
    
    if (result && result.access) { 
        userAccessToken = result.access; 
        userRefreshToken = result.refresh; 
        
        console.log("Logged in successfully. Token obtained.");
        
        loadSongs();
        loadPlaylists(); 
        
        hideLogin();
    } else {
        alert("Login failed! Please check your credentials.");
    }
}


function playSong(song) {
    const audioPlayer = document.getElementById('audioPlayer');
    const playPauseButton = document.getElementById('playPauseButton');
    const titleElement = document.querySelector('.player .song-info .title');
    const artistElement = document.querySelector('.player .song-info .artist');
    
    if (!audioPlayer) return;

    titleElement.textContent = song.title || 'Unknown Title';
    artistElement.textContent = song.artist || 'Unknown Artist';
    
    audioPlayer.src = song.file; 
    audioPlayer.play().catch(err => console.error('Playback failed:', err));
    
    if(playPauseButton) playPauseButton.textContent = '⏸'; 
}



async function loadSongs() {
    const headers = getAuthHeaders();
    
    try {
        const response = await fetch('http://127.0.0.1:8000/songs/', { headers });
        
        if (!response.ok) {
            if (response.status === 401) {
    
                showLogin(); 
                return;
            }
            throw new Error(`HTTP error: ${response.status}`);
        }
        
        const songs = await response.json();
        const list = document.querySelector('.song-list');
        
        if (list) {
            list.innerHTML = ''; 
            songs.forEach(song => {
                const item = document.createElement('div');
                item.className = 'song-item';
                
                item.addEventListener('click', () => {
                    playSong(song); 
                });
                
                const title = document.createElement('span');
                title.textContent = song.title || 'Untitled';
                const duration = document.createElement('span');
                duration.textContent = song.duration || '--:--';
                
                item.appendChild(title);
                item.appendChild(duration);
                list.appendChild(item);
            });
        }
    } catch (err) {
        console.error('Failed to load songs:', err);
    }
}

async function loadPlaylists() {
    const headers = getAuthHeaders();
    
    try {
        const response = await fetch('http://127.0.0.1:8000/playlists/', { headers });
        
        if (!response.ok) {
            if (response.status === 401) return; 
            throw new Error(`HTTP error: ${response.status}`);
        }
        
        const playlists = await response.json();
        console.log('Playlists:', playlists);
    } catch (err) {
        console.error('Failed to load playlists:', err);
    }
}



window.addEventListener('DOMContentLoaded', () => {
    
    let user = window.currentUser ? window.currentUser.username : null;
    
    const loginButton = document.getElementById('loginButton');
    const audioPlayer = document.getElementById('audioPlayer');
    const playPauseButton = document.getElementById('playPauseButton');

    loadSongs();
    loadPlaylists();

    if (loginButton) {
        loginButton.addEventListener('click', handleLogin);
    }

    if (!user && !userAccessToken) { 
        showLogin();
    }
  
    if (playPauseButton && audioPlayer) {
        playPauseButton.addEventListener('click', () => {
            if (audioPlayer.paused) {
                audioPlayer.play();
                playPauseButton.textContent = '⏸'; 
            } else {
                audioPlayer.pause();
                playPauseButton.textContent = '⏯'; 
            }
        });
    }

    document.querySelector('.close')?.addEventListener('click', () => { window.controls?.close(); });
    document.querySelector('.minimize')?.addEventListener('click', () => { window.controls?.minimize(); });
    document.querySelector('.maximize')?.addEventListener('click', () => { window.controls?.maximize(); });
});