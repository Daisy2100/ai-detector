# AI Content Detector

## 專案：AI 或人類文章檢測器 (HW5: Advanced topic on AI) - 前後端整合

**參考網站：** [justdone.com/ai-detector](https://justdone.com/ai-detector)

**部署網址：** [ai-detector.daisy2100.com](https://ai-detector.daisy2100.com)

### 📋 專案說明

這是一個 AI 內容檢測 Web 應用程式，可以分析輸入的文本，判斷該文本是由「AI 生成」或「人類撰寫」。

### 🏗️ 專案架構

- **前端技術：** Angular 19 + Tailwind CSS + PrimeNG
- **後端技術：** Python + TF-IDF + Logistic Regression
- **部署平台：** Vercel (前後端皆使用 Vercel 部署)

### 📁 專案結構

```
ai-detector/
├── backend/
│   ├── detect.py          # Python API (Vercel Serverless Function)
│   └── requirements.txt   # Python 依賴
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/    # Angular 共用元件
│   │   │   ├── pages/         # 頁面元件
│   │   │   └── services/      # API 服務
│   │   └── assets/            # 靜態資源
│   ├── angular.json           # Angular 設定
│   └── package.json           # NPM 依賴
├── vercel.json                # Vercel 部署設定 (前後端)
└── README.md
```

### 🚀 本地開發

#### 環境需求

- Node.js 20+
- npm 9+
- Python 3.9+

#### 前端開發

```bash
# 進入前端目錄
cd frontend

# 安裝依賴
npm install

# 啟動開發伺服器
npm run start

# 或使用 ng serve
npx ng serve
```

開啟瀏覽器訪問 http://localhost:4200

#### 前端建置

```bash
cd frontend

# 建置生產版本
npm run build
```

建置產物會輸出到 `frontend/dist/` 目錄

#### 後端開發

```bash
# 進入後端目錄
cd backend

# Python 標準庫已足夠，無需額外安裝
# 如需測試 AI 檢測模型
python3 -c "
from detect import AIDetectorModel
model = AIDetectorModel()
result = model.predict('Your test text here with at least 50 characters for analysis.')
print(result)
"
```

#### 啟動本地後端伺服器

如需本地測試 API，可以使用以下 Python 腳本啟動簡易伺服器：

```bash
cd backend

# 建立並執行本地伺服器 (port 3000)
python3 << 'EOF'
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from detect import AIDetectorModel

detector = AIDetectorModel()

class APIHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/detect':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)
            result = detector.predict(data.get('text', ''))
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())

print('Backend server running on http://localhost:3000')
HTTPServer(('localhost', 3000), APIHandler).serve_forever()
EOF
```

#### 前後端整合開發

1. 啟動後端伺服器 (Terminal 1)：
```bash
cd backend
# 執行上述 Python 伺服器腳本
```

2. 啟動前端開發伺服器 (Terminal 2)：
```bash
cd frontend
npm install
npm run start -- --proxy-config proxy.conf.json
```

3. 開啟瀏覽器訪問 http://localhost:4200

### 🔧 API 端點

**POST /api/detect**

請求格式：
```json
{
  "text": "要分析的文本內容..."
}
```

回應格式：
```json
{
  "prediction": "AI" | "Human" | "Uncertain",
  "confidence": 85.5,
  "ai_probability": 85.5,
  "human_probability": 14.5,
  "word_count": 150,
  "features": {
    "avg_sentence_length": 18.5,
    "vocabulary_richness": 72.3,
    "formality_score": 68.2
  },
  "message": "Analysis complete. The text appears to be ai-generated."
}
```

### 🧠 AI 檢測原理

本專案使用 TF-IDF + Logistic Regression 模型來分析文本特徵：

1. **平均句子長度** - AI 生成的文本通常有更一致的句子長度
2. **詞彙豐富度** - 人類撰寫的文本通常詞彙變化更多
3. **標點符號密度** - 人類使用更多樣化的標點符號
4. **連接詞頻率** - AI 傾向使用更多連接詞
5. **第一人稱代名詞** - 人類撰寫更常使用第一人稱
6. **被動語態** - AI 傾向使用更多被動語態
7. **平均詞長** - AI 通常使用稍長的詞彙
8. **句子複雜度** - AI 傾向有一致的複雜度
9. **重複度** - AI 傾向重複某些片語
10. **正式度** - AI 傾向更正式的寫作風格

### 🚀 部署

本專案使用 Vercel 進行前後端部署：

```bash
# 安裝 Vercel CLI
npm install -g vercel

# 部署到 Vercel
vercel

# 部署到生產環境
vercel --prod
```

### 📝 License

MIT License

---

**物聯網應用與資料分析 HW5**

