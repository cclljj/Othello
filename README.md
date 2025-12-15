# Antigravity Othello (Black-White Chess)

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/python-3.7+-blue.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)
![Built By](https://img.shields.io/badge/Built%20By-Ling--Jyh%20Chen-blue)
![Powered By](https://img.shields.io/badge/Powered%20By-AntiGravity%20%26%20Gemini%203%20Pro-purple)

> This project was created by **Ling-Jyh Chen** using **AntiGravity** and the **Gemini 3 Pro** model.
> 本專案由 **陳伶志 (Ling-Jyh Chen)** 使用 **AntiGravity** 與 **Gemini 3 Pro** 模型開發。

[English](#english) | [繁體中文](#繁體中文)

---

## English

A modern, web-based Othello (Reversi) game built with a **zero-dependency** Python backend and a polished frontend.

### Features

*   **Classic Gameplay**: Full Othello rules implementation including flanking, turn switching, legal move validation, and game-over detection.
*   **"Antigravity" Backend**:
    *   Powered purely by Python's standard library (`http.server` & `socketserver`).
    *   **No external dependencies** (no Flask, Django, or FastAPI required).
    *   **Multi-threaded**: Handles concurrent requests using `ThreadingTCPServer`.
    *   **Robust**: Custom error handling and JSON API responses.
*   **Modern UI**:
    *   Responsive Green felt-style board.
    *   3D-effect discs with shadow animations.
    *   Glassmorphism scorecards.
    *   Visual indicators for valid moves and current turn.

### Prerequisites

*   Python 3.7 or higher.

### How to Run

1.  **Open a terminal** in the project directory:
    ```bash
    cd /path/to/Black-White-Chess
    ```

2.  **Start the server**:
    ```bash
    python3 main.py
    ```

3.  **Play**:
    Open your web browser and navigate to: [http://localhost:8000](http://localhost:8000)

### Troubleshooting

*   **"Address already in use" Error**:
    *   This means the port 8000 is occupied.
    *   The server is configured to reuse the address, so simply stopping the previous process (Ctrl+C) and restarting should work.
    *   If it persists, find the process using port 8000 (`lsof -i :8000`) and kill it.

*   **Browser Errors**:
    *   If you see "Error making move", check the terminal output where you started `main.py` for debug logs.

### Project Structure

*   `main.py`: The entry point. Multi-threaded web server and API handler.
*   `othello.py`: Core game logic (board state, rules, flip mechanics).
*   `static/`: Frontend assets (HTML, CSS, JS).
*   `verify_game.py`: Unit tests to ensure game logic correctness.

---

## 繁體中文

這是一個現代化的網頁版黑白棋（Othello/Reversi）遊戲，採用 **零依賴** 的 Python 後端與精緻的前端介面構建。

### 功能特色

*   **經典玩法**：完整實作黑白棋規則，包含夾擊吃子、輪流下棋、合法步數驗證以及遊戲結束判斷。
*   **"Antigravity" 後端**：
    *   完全基於 Python 標準函式庫 (`http.server` & `socketserver`)。
    *   **無需外部依賴** (不需要安裝 Flask, Django, 或 FastAPI)。
    *   **多執行緒**：使用 `ThreadingTCPServer` 處理並發請求。
    *   **穩健設計**：自定義錯誤處理與 JSON API 回應。
*   **現代化介面**：
    *   響應式設計的綠色絨布風格棋盤。
    *   具備陰影動畫的 3D 棋子效果。
    *   玻璃擬態 (Glassmorphism) 計分板。
    *   合法步數提示與當前玩家指示。

### 環境需求

*   Python 3.7 或更高版本。

### 如何執行

1.  **開啟終端機** 並進入專案目錄：
    ```bash
    cd /path/to/Black-White-Chess
    ```

2.  **啟動伺服器**：
    ```bash
    python3 main.py
    ```

3.  **開始遊戲**：
    打開瀏覽器並前往：[http://localhost:8000](http://localhost:8000)

### 疑難排解 (Troubleshooting)

*   **"Address already in use" 錯誤**：
    *   這表示 8000 連接埠已被佔用。
    *   伺服器已設定為可重複使用地址，因此通常只需停止前一個程序 (Ctrl+C) 並重新啟動即可。
    *   如果問題持續，請找出佔用 8000 埠的程序 (`lsof -i :8000`) 並將其強制結束。

*   **瀏覽器錯誤**：
    *   如果您看到 "Error making move"，請檢查啟動 `main.py` 的終端機輸出以查看除錯日誌。

### 專案結構

*   `main.py`: 程式入口點。多執行緒網頁伺服器與 API 處理器。
*   `othello.py`: 核心遊戲邏輯（棋盤狀態、規則、翻轉機制）。
*   `static/`: 前端資源（HTML, CSS, JS）。
*   `verify_game.py`: 用於確保遊戲邏輯正確性的單元測試。

---

## License

[MIT License](LICENSE)
