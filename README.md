# AI Content Detector

## 專案：AI 或人類文章檢測器 (HW5: Advanced topic on AI) - 前後端整合

**參考網站：** [justdone.com/ai-detector](https://justdone.com/ai-detector)

### 📋 專案說明

這是一個 AI 內容檢測 Web 應用程式，可以分析輸入的文本，判斷該文本是由「AI 生成」或「人類撰寫」。

### 🏗️ 專案架構

- **前端技術：** Angular 19 + Tailwind CSS + PrimeNG
- **後端技術：** Python (FastAPI) + TF-IDF + Logistic Regression
- **部署環境：** Vercel Serverless Function

### 📁 專案結構

```
ai-detector/
├── api/
│   └── detect.py          # Python API (Vercel Serverless Function)
├── src/
│   ├── app/
│   │   ├── components/    # Angular 共用元件
│   │   ├── pages/         # 頁面元件
│   │   └── services/      # API 服務
│   └── assets/            # 靜態資源
├── vercel.json            # Vercel 部署設定
├── angular.json           # Angular 設定
└── package.json           # NPM 依賴
```

### 🚀 本地開發

1. 安裝依賴
```bash
npm install
```

2. 啟動開發伺服器
```bash
npm start
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

### 📝 License

MIT License

---

**物聯網應用與資料分析 HW5**

