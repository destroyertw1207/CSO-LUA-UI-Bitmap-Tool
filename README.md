Made by Destroyertw1207 (DestroyerI滅世I)

Just Share. No English Version.

-------------------------------------------------

【使用方式】

CSO STUDIO LUA 像素圖

-------------------------------------------------

【Convert（轉換）】

[1] 打開「Image Magick Install」並安裝裡面的檔案

[2] 打開「CSO STUDIO LUA 像素圖.exe」

[3] 點擊「Choose File（選擇檔案）」選擇要轉為像素的圖片檔

[4] 選擇大小（「Size 16x16」、「Size 32x32」）

[5] 點擊「Convert（轉換）」

[6] 看到「圖片.圖片副檔名.bitmap」就可以了

[※] 圖片檔案名稱不能使用中文

[※] 如果沒有安裝「Image Magick」則無法使用「Convert（轉換）」功能

-------------------------------------------------

【Bitmap（像素圖）】
[1] 打開「CSO STUDIO LUA 像素圖.exe」

[2] 選擇「BITMAP（像素圖）」

[3] 左半邊像素圖
　　左鍵單點可以一格一格的畫
　　右鍵單點後可以滑動滑鼠直接畫

[4] 右半邊設定
　　可以自行調整關於畫筆畫板的設定

　　「畫筆」
　　Draw：畫畫
　　Eraser：橡皮擦
　　Selece Color：選取單格顏色

　　「畫板」
　　16x16：將像素圖改為16x16的大小，並清除所有畫格
　　32x32：將像素圖改為32x32的大小，並清除所有畫格
　　Clear：清除所有畫格
　　Import：導入.bitmap檔案，並進行調整

　　「顏色」
　　R：紅
　　G：綠
　　B：藍
　　A：透明度
　　Color Picker：自動選取顏色

　　「輸出」
　　文字框：輸出後的檔案名稱
　　Export：輸出

[5] 輸出後會有以下幾個檔案：
　　bitmap_class.lua
	bitmap_data.lua
	檔案名稱.bitmap

[※] 輸出的檔案名稱字首不能為數字！

-------------------------------------------------

【導入CSO LUA】

[1] 將「Script Example」複製進「C:\Studio\Script」，可將「Script Example」重新命名

[2] 將輸出後的「.lua」檔案丟進「C:\Studio\Script\Script Example 或 重新命名的資料夾」

[3] 開啟CSO，並進入「1人」編輯模式

[4] 按下「V」再按「8」找到「Script Example 或 重新命名的資料夾」

[5] 點擊「開始測試」

[6] 按下「V」再按「8」並點擊「停止測試」

[7] 完成

[※] bitmap_data.lua 中的 xxx:Set() 可進行修改
　　xxx:Set(x, y, width(寬), height(高), spacing(每格間距)) 

-------------------------------------------------
