AÇIKLAMA

EsencanCoinTracker basit olarak Binance üzerinden verileri anlık olarak çekerek, 
istenilen coin'e ait grafik çizdirebilir. Çizilen grafik üzerine gelişme ve ekleme 
sürecinde olan indicatörler ekleyebilir. ARIMA öngörü modeli ile periyota 
bağlı olarak bir sonraki periyodun tahminlenmesini gerçekleştirir. Ayrıca ister kendinizin 
hazırladığı veya Binance'ta spot piyasada işlem gören tüm coinleri analiz ederek alım 
seviyesine uygun olan coinleri listeler.

COIN BULMA

Veriler LSE (Least Sequare Estimation) ile analiz edilerek periyoda bağlı olarak ana 
trend bilgisi elde edilir. Verilerin standart sapma değerleri hesaplanarak bu standart sapmalar
ana trend bilgisine eklenerek direnç ve destek seviyeleri oluşturulur. Anlık değeri destek 
seviyesinin altında kalması durumunda coin alıma uygun olarak listelenir.


ÖNGÖRÜ

Seçilen Coin'e ait belirli bir zaman aralığında ve belirli bir periyotda ARIMA öngörü modeli ile
tahminleme yapılır. Periyod örneğin 1 gün olarak işaretlenmiş ise 1 gün sonrası değeri tahminlemektedir.
Unutulmamalıdır ki geçmiş verisi nekadar optimum seçilirse, öngörü doğruluğu buna bağlı olarak değişir.
Yapılan işlemin bir öngörü olduğu ve canlı piyasalarda herşeyin anlık değişebileceği unutulmamalıdır.

İNDİKATÖRLER

Gelişme süresince daha fazla indikatör eklenecektir. Şimdilik Trend çizgileri, bollinger bantları ve ortalama
indikatörleri tasarlanmıştır. Gelişen süreçte bu indikatörlerde parametrelerin kullanıcı tarafından seçilmesi
olabilecektir.

GEREKSİNİMLER