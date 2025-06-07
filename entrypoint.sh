#!/bin/sh
# 先把所有 migration 套到資料庫
flask db upgrade  
# 再啟動 Flask
exec flask run --host=0.0.0.0
