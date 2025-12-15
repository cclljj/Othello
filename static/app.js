const boardElement = document.getElementById('board');
const blackScoreEl = document.getElementById('black-score');
const whiteScoreEl = document.getElementById('white-score');
const blackCard = document.getElementById('black-score-card');
const whiteCard = document.getElementById('white-score-card');
const turnDisplayEl = document.getElementById('turn-display');
const messageEl = document.getElementById('game-message');
const resetBtn = document.getElementById('reset-btn');

let currentState = null;

async function fetchState() {
    try {
        const response = await fetch('/api/state');
        const data = await response.json();
        updateUI(data);
    } catch (error) {
        showMessage("Error fetching game state", true);
    }
}

async function makeMove(row, col) {
    try {
        const response = await fetch('/api/move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ row, col })
        });

        if (!response.ok) {
            let errorMsg = `Server Error: ${response.status} ${response.statusText}`;
            try {
                const err = await response.json();
                if (err.detail) errorMsg = err.detail;
            } catch (e) {
                console.error("Failed to parse error JSON:", e);
                // Try to get text if JSON fails
                const text = await response.text();
                console.error("Raw error response:", text);
            }
            showMessage(errorMsg, true);
            return;
        }

        const data = await response.json();
        updateUI(data);
    } catch (error) {
        console.error("Network or parsing error:", error);
        showMessage("Error making move: " + error.message, true);
    }
}

async function resetGame() {
    try {
        const response = await fetch('/api/new_game', { method: 'POST' });
        const data = await response.json();
        updateUI(data);
        hideMessage();
    } catch (error) {
        showMessage("Error resetting game", true);
    }
}

function updateUI(state) {
    currentState = state;
    renderBoard(state.board, state.valid_moves);
    updateScores(state.scores);
    updateTurnInfo(state.current_turn, state.game_over, state.winner);
}

function renderBoard(board, validMoves) {
    boardElement.innerHTML = '';

    // Create a set of valid moves for O(1) lookup
    const validMovesSet = new Set(validMoves.map(m => `${m[0]},${m[1]}`));

    for (let r = 0; r < 8; r++) {
        for (let c = 0; c < 8; c++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');
            cell.dataset.row = r;
            cell.dataset.col = c;

            const val = board[r][c];
            if (val !== 0) {
                const disc = document.createElement('div');
                disc.classList.add('disc');
                disc.classList.add(val === 1 ? 'black' : 'white');
                cell.appendChild(disc);
            } else if (validMovesSet.has(`${r},${c}`)) {
                cell.classList.add('valid');
                cell.onclick = () => makeMove(r, c);
            }

            boardElement.appendChild(cell);
        }
    }
}

function updateScores(scores) {
    blackScoreEl.textContent = scores.black;
    whiteScoreEl.textContent = scores.white;
}

function updateTurnInfo(turn, gameOver, winner) {
    if (gameOver) {
        let winnerText = "It's a Tie!";
        if (winner === 1) winnerText = "Black Wins!";
        else if (winner === 2) winnerText = "White Wins!";

        turnDisplayEl.innerHTML = `<strong style="color: var(--accent-color)">GAME OVER: ${winnerText}</strong>`;
        blackCard.classList.remove('active');
        whiteCard.classList.remove('active');
        showMessage(winnerText);
    } else {
        const player = turn === 1 ? "Black" : "White";
        turnDisplayEl.innerHTML = `Current Turn: <span id="current-player">${player}</span>`;

        if (turn === 1) {
            blackCard.classList.add('active');
            whiteCard.classList.remove('active');
        } else {
            whiteCard.classList.add('active');
            blackCard.classList.remove('active');
        }
        hideMessage();
    }
}

function showMessage(msg, isError = false) {
    messageEl.textContent = msg;
    messageEl.classList.remove('hidden');
    if (isError) {
        messageEl.style.borderColor = 'red';
        messageEl.style.color = 'red';
    } else {
        messageEl.style.borderColor = 'var(--accent-color)';
        messageEl.style.color = '#ffadb8';
    }
}

function hideMessage() {
    messageEl.classList.add('hidden');
}

resetBtn.onclick = resetGame;

// Initial Load
fetchState();
