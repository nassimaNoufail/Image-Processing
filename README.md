# Image-Processing
Smoothing and noise removal based on spatial filtering
## 介紹：
針對影像雜訊的問題，參考上課講義中第六章影像強化的空間區域強化技術-空間濾波器，運用遮罩運算搭配不同的方法可以解決雜訊問題，比較多種方法找出適用情況、處理效果好壞和影像模糊的狀況。
## 怎麼做：
- 先將彩色影像轉換成灰階影像：
取得彩色影像的RGB數值，再依照以下公式：  
Gray = 0.2989 * Red + 0.587 * Green + 0.114 * Blue  
把轉換後的灰階取代原本的RGB數值  
- 實作空間濾波器的五種方法：
  - 相鄰像素平均法：
  將目前要處理的像素及其周邊共(2m+1)2個像素相加平均，再以g(x, y)取代f(x, y)。
  ![Formula](https://raw.githubusercontent.com/timmycheng1221/Image-Processing/master/images/formula/2-a1.jpg)
    例如，m = 1的3x3遮罩：
    
    ![Formula](https://raw.githubusercontent.com/timmycheng1221/Image-Processing/master/images/formula/2-a2.jpg)
  - 中值濾波：
  將目前要處理的像素及其周邊共(2m+1)2個像素根據灰階數值大小排序，再以排在最中間的灰階取代要處理像素的灰階。
  ![Formula](https://raw.githubusercontent.com/timmycheng1221/Image-Processing/master/images/formula/2-b.jpg) 
  - 雙側濾波器：
  做高斯平滑化時，不只考慮鄰近點的距離，還考慮鄰近點的灰階差異，距離越遠，平均值的貢獻度越低；灰階差異越大，貢獻度也是越低。  
    雙側濾波器公式：
  
    ![Formula](https://raw.githubusercontent.com/timmycheng1221/Image-Processing/master/images/formula/2-c1.jpg)
    x為目前要處理的像素，x '為x周邊的像素，l(x)為x的灰階，Ωx為x周邊的範圍
  
    ![Formula](https://raw.githubusercontent.com/timmycheng1221/Image-Processing/master/images/formula/2-c2.jpg)
  
    c(x, x ')為計算x '對x的距離差異貢獻度
  
    ![Formula](https://raw.githubusercontent.com/timmycheng1221/Image-Processing/master/images/formula/2-c3.jpg)
    
    s(f, f ')為計算x'對x的灰階差異貢獻度
  
    ![Formula](https://raw.githubusercontent.com/timmycheng1221/Image-Processing/master/images/formula/2-c4.jpg)
    
    k(x)為x周邊像素貢獻度(距離差異和灰階差異)的總和
  - 最小/最大濾波：
  最小濾波為將目前要處理的像素及其周邊共8個像素根據灰階數值大小排序，再以排在最小的灰階取代要處理像素的灰階，而最大濾波則是以排在最大的灰階取代要處理像素的灰階。
  - 波峰波谷濾波器：
  波峰濾波器為將目前要處理的像素及其周邊共8個像素根據灰階數值大小排序，若最大的灰階像素為目前要處理的像素，則以8鄰點中的最大灰階取代要處理像素的灰階，而波谷濾波器則是若最小的灰階像素為目前要處理的像素，則以8鄰點中的最小灰階取代要處理像素的灰階。
 
## 程式說明：
- 一開始的畫面：
  ![GUI](https://raw.githubusercontent.com/timmycheng1221/Image-Processing/master/images/GUI/1.jpg)
- 選單介紹：
  - File：Open為開啟檔案，Exit為關閉程式
  - Edit：Add noise為加入黑白雜訊，機率為30%
  Add pepper noise為加入黑雜訊，機率為30%
  Add salt noise為加入白雜訊，機率為30%
  Reset為恢復原本影像的狀態
  - Tool：各種空間濾波器，在結果會再詳細的說明
- 執行畫面：
  ![GUI](https://raw.githubusercontent.com/timmycheng1221/Image-Processing/master/images/GUI/2.jpg) 
  Process顯示目前應用的空間濾波器  
  下方左邊的圖片為最初讀取的圖片，並加入雜訊  
  下方右邊的圖片為經過空間濾波器的結果
## 結果：
基本上都使用影像處理中常見的Lena照片來呈現結果，若效果不明顯，則以其他影像呈現
 
- 相鄰像素平均法：
  - 做一次3x3遮罩：
    ![result](https://raw.githubusercontent.com/timmycheng1221/Image-Processing/master/images/result/1-a.jpg)
  - 做兩次3x3遮罩：
    ![result](https://raw.githubusercontent.com/timmycheng1221/Image-Processing/master/images/result/1-b.jpg)
  - 做一次5x5遮罩：
    ![result](https://raw.githubusercontent.com/timmycheng1221/Image-Processing/master/images/result/1-c.jpg)

- 中值濾波：
  - 做一次3x3遮罩：
    ![result](https://raw.githubusercontent.com/timmycheng1221/Image-Processing/master/images/result/2-a.jpg)
  - 做一次5x5遮罩：
    ![result](https://raw.githubusercontent.com/timmycheng1221/Image-Processing/master/images/result/2-b.jpg)
  - 加入雜訊，並做一次3x3遮罩：
    ![result](https://raw.githubusercontent.com/timmycheng1221/Image-Processing/master/images/result/2-c.jpg)
  八成的雜訊都被去除
  - 加入雜訊，並做兩次3x3遮罩：
    ![result](https://raw.githubusercontent.com/timmycheng1221/Image-Processing/master/images/result/2-d.jpg)
  幾乎所有雜訊都被去除，僅剩零星的
 
- 雙側濾波器：
  - 做一次，σc = 50，σs = 3：
    ![result](https://raw.githubusercontent.com/timmycheng1221/Image-Processing/master/images/result/3-a.jpg)
  - 做兩次，σc = 50，σs = 3：
    ![result](https://raw.githubusercontent.com/timmycheng1221/Image-Processing/master/images/result/3-b.jpg)
  [參數參考網站](http://homepages.inf.ed.ac.uk/rbf/CVonline/LOCAL_COPIES/MANDUCHI1/Bilateral_Filtering.html)
- 最小/最大濾波
  - 加入白雜訊，先做最小濾波，再做最大濾波：
    ![result](https://raw.githubusercontent.com/timmycheng1221/Image-Processing/master/images/result/4-a1.jpg)
    ![result](https://raw.githubusercontent.com/timmycheng1221/Image-Processing/master/images/result/4-a2.jpg)
  - 加入黑雜訊，先做最大濾波，再做最小濾波： 
    ![result](https://raw.githubusercontent.com/timmycheng1221/Image-Processing/master/images/result/4-b1.jpg)
    ![result](https://raw.githubusercontent.com/timmycheng1221/Image-Processing/master/images/result/4-b2.jpg)
- 波峰/波谷濾波器：
  - 先做波峰濾波器，再做波谷濾波器：
    ![result](https://raw.githubusercontent.com/timmycheng1221/Image-Processing/master/images/result/5-a1.jpg)
    ![result](https://raw.githubusercontent.com/timmycheng1221/Image-Processing/master/images/result/5-a2.jpg)
  - 先做波谷濾波器，再做波峰濾波器：
    ![result](https://raw.githubusercontent.com/timmycheng1221/Image-Processing/master/images/result/5-b1.jpg)
    ![result](https://raw.githubusercontent.com/timmycheng1221/Image-Processing/master/images/result/5-b2.jpg)
## 討論/結論：
雖然這幾種空間濾波器可以解決影像雜訊的問題，但同時也帶來影像模糊的副作用，如何降低模糊的副作用依然是個可以研究的方向。  
在這次實作的過程中，我覺得印象最深的是中值濾波，即使影像的雜訊多到讓人有點無法辨識影像，經過一兩次的中值濾波還是可以把原本影像的輪廓還原回來，去雜訊的效果是最好的。  
而其他的空間濾波器感覺變化不大，也許需要更極端的影像做處理，才能看出空間濾波器造成的影響。
