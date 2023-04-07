## [Pynecone](https://github.com/pynecone-io/pynecone)  範例專案

### 安裝套件
```
python >= 3.7
nodejs >= 12.22
```


### 建議環境 python 3.10
```
pandas
numpy
pynecone
redis >= 4.5.1
```

## 運行設定

1. 在 vscode 中選擇自己的虛擬環境後, run and debug 中選擇 `運行 pynecone fullstack` 選項。

2. 使用 F5 進行 debug 或是在 terminal 直接執行 `pc run`

3. 所有在 `pynecone_sample` 底下的程式碼在運行過程中，如果有修改並儲存，框架會自動刷新並 compile (框架會重新建立subprocess)


## 運行 State 說明

1. 需要在網頁上顯示的變數要使用 `class YourState(pc.State)`，其中定義的變數必須是 json serializable。

2. 定期更新可以使用 [官網範例](https://pynecone.io/docs/state/events)中提到的 
```
Triggering Events From Event Handlers

在on_blur事件觸發中回傳async函式 -> 回傳下一個async函式 -> ...
```

3. 可以宣告全域變數作為整個程式後台的運行，在[範例](pynecone_sample/pynecone_sample.py)中使用了gstate作為暫存全域counter以及能使用redis的功能。

