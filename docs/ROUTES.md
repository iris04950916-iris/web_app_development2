# 路由設計文件 (API Design)

根據系統架構與資料庫設計，以下為食譜收藏夾系統的路由（Route）與頁面規劃。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 首頁 (食譜列表) | GET | `/` | `templates/index.html` | 顯示所有食譜，支援分類篩選 |
| 新增食譜頁面 | GET | `/recipes/new` | `templates/form.html` | 顯示新增表單 |
| 建立食譜 | POST | `/recipes/new` | — | 接收表單，存入 DB，重導向至詳情頁 |
| 食譜詳情 | GET | `/recipes/<id>` | `templates/detail.html` | 顯示材料、步驟、評論、營養資訊 |
| 編輯食譜頁面 | GET | `/recipes/<id>/edit` | `templates/form.html` | 顯示編輯表單，預填資料 |
| 更新食譜 | POST | `/recipes/<id>/edit` | — | 接收表單，更新 DB，重導向至詳情頁 |
| 刪除食譜 | POST | `/recipes/<id>/delete`| — | 刪除後重導向至首頁 |
| 新增評論 | POST | `/recipes/<id>/reviews`| — | 接收評論與評分，重導向至詳情頁 |

## 2. 每個路由的詳細說明

### 首頁 (`GET /`)
- **輸入**：`category_id` (Query Parameter，可選，用於分類篩選)
- **處理邏輯**：呼叫 `Recipe.get_all()` 獲取所有食譜；若有 `category_id` 則只篩選該分類下的食譜。同時獲取所有 `Category` 供分類選單使用。
- **輸出**：渲染 `index.html`。

### 新增食譜頁面 (`GET /recipes/new`)
- **輸入**：無
- **處理邏輯**：取得所有分類 (`Category.get_all()`) 以供表單提供核取方塊或下拉選單。
- **輸出**：渲染 `form.html`。

### 建立食譜 (`POST /recipes/new`)
- **輸入**：表單資料包含 `title`, `description`, `image`, 營養資訊 (`calories`, etc.)，以及陣列形式的 `ingredients` 與 `steps`。
- **處理邏輯**：
  1. 驗證 `title` 等必填欄位。
  2. 處理圖片上傳（如有）。
  3. 呼叫 `Recipe.create()` 建立食譜本體。
  4. 將對應的材料 (`Ingredient`) 與步驟 (`Step`) 關聯寫入。
- **輸出**：成功後重導向至 `/recipes/<id>`。
- **錯誤處理**：驗證失敗則帶著錯誤訊息返回 `form.html`。

### 食譜詳情 (`GET /recipes/<id>`)
- **輸入**：`id` (URL 參數)
- **處理邏輯**：呼叫 `Recipe.get_by_id(id)`，並由 ORM 取得關聯的材料、步驟、評論。
- **輸出**：渲染 `detail.html`。
- **錯誤處理**：若該 id 不存在則返回 HTTP 404 頁面。

### 編輯食譜頁面 (`GET /recipes/<id>/edit`)
- **輸入**：`id` (URL 參數)
- **處理邏輯**：查詢原本的 `Recipe` 以及關聯的材料/步驟。
- **輸出**：渲染 `form.html`，將取得的資料填入作為預設值。
- **錯誤處理**：若該 id 不存在則返回 404。

### 更新食譜 (`POST /recipes/<id>/edit`)
- **輸入**：`id` (URL 參數)、表單更新內容。
- **處理邏輯**：呼叫 `recipe.update(...)`，並且更新、刪除或新增對應的材料與步驟資料。
- **輸出**：重導向至 `/recipes/<id>`。

### 刪除食譜 (`POST /recipes/<id>/delete`)
- **輸入**：`id` (URL 參數)
- **處理邏輯**：呼叫 `recipe.delete()`，資料庫的 `ON DELETE CASCADE` 將連帶刪除底下相關的材料、步驟與評論。
- **輸出**：重導向至首頁 (`/`)。

### 新增評論 (`POST /recipes/<id>/reviews`)
- **輸入**：`id` (URL 參數)，以及表單資料 `rating`, `content`。
- **處理邏輯**：呼叫 `Review.create()` 將評價存入資料庫。
- **輸出**：重導向回原本的食譜詳細頁 (`/recipes/<id>`)。

## 3. Jinja2 模板清單

- `templates/base.html`: 共用版型（包含 `<head>`、導覽列 navbar、頁尾 footer 等）。
- `templates/index.html` (繼承 `base.html`): 首頁，顯示多個食譜卡片與分類篩選器。
- `templates/detail.html` (繼承 `base.html`): 食譜詳細內容，包含材料清單、步驟列表、營養標示、評分表單與評論區塊。
- `templates/form.html` (繼承 `base.html`): 食譜表單，供新增與編輯共用（透過傳入的變數判斷是 Create 或 Update 模式）。

## 4. 路由骨架程式碼
請參考以下檔案，其中已準備好包含裝飾器與 docstring 的骨架程式碼：
- `app/routes/__init__.py`
- `app/routes/index.py`
- `app/routes/recipe.py`
