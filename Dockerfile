# 1. 選擇基底映像
FROM python:3.12-slim

# 2. 設定工作目錄
WORKDIR /app

# 3. 複製需求檔並安裝相依套件
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 複製程式碼
COPY . .

# 5. 設定環境變數（告訴 Flask 啟動哪個 app）
ENV FLASK_APP=run.py \
    FLASK_ENV=production

# 6. 暴露對外的 port
EXPOSE 5000

# 7. 啟動指令
CMD ["flask", "run", "--host=0.0.0.0"]
