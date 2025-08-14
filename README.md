Projenin Adı: Kariyer Koçu AI
Vizyon: Bireylerin kariyer gelişim süreçlerinde, yapay zekanın sunduğu veri analizi ve kişiselleştirme gücünden faydalanarak onlara akıllı, empatik ve eyleme geçirilebilir bir rehberlik sunmaktır.
Temel Amaç: "Kariyer Koçu AI" projesi, kullanıcıların kendi kariyer verilerini (günlükler, hedefler, CV'ler) tek bir platformda toplamalarını ve bu veriler üzerinden yapay zeka destekli, objektif geri bildirimler almalarını sağlamak amacıyla geliştirilmiştir. Uygulama, kariyer yolculuğunun getirdiği belirsizlikler ve zorluklar karşısında kullanıcıya bir "dijital yol arkadaşı" olmayı hedefler.
Projenin Çözmeyi Hedeflediği Sorunlar
Bu proje, kariyer gelişim sürecinde olan bireylerin sıkça karşılaştığı aşağıdaki temel sorunlara çözüm üretmeyi amaçlamaktadır:
Objektif Geri Bildirim Eksikliği: Bireyler, kendi CV'lerini veya durumlarını değerlendirirken genellikle öznel davranırlar. Proje, yapay zeka kullanarak tarafsız bir "üçüncü göz" sunar ve kullanıcının fark edemediği hataları veya gelişim alanlarını ortaya çıkarır.
Kişiselleştirilmiş Yol Haritası Yokluğu: Genel kariyer tavsiyeleri genellikle kişinin özel durumuna, hedeflerine ve ruh haline uymaz. Bu uygulama, kullanıcının kendi girdilerini analiz ederek ona özel, kişiselleştirilmiş eylem planları ve stratejiler sunar.
Stres ve Motivasyon Yönetimi: Kariyer süreçleri, özellikle iş arama veya zorlu projeler sırasında stresli olabilir. "Akıllı Günlük" modülü, kullanıcının duygusal durumunu analiz ederek stres yönetimi için pratik öneriler sunar ve motivasyonunu artırmaya yardımcı olur.
Belirsizlik ve Eylemsizlik: "Sırada ne yapmalıyım?" veya "Bu hedefe nasıl ulaşırım?" gibi sorular, bireyleri eylemsizliğe itebilir. "Hedefler" ve "Genel Öneriler" modülleri, büyük hedefleri küçük, yönetilebilir adımlara bölerek ve bütünsel bir yol haritası sunarak bu belirsizliği ortadan kaldırmayı hedefler.
Hedef Kitle
Öğrenciler ve Yeni Mezunlar: Kariyerlerinin başlangıcında olan, CV hazırlama ve hedef belirleme konusunda rehberliğe ihtiyaç duyan gençler.
Kariyerinde Değişiklik Yapmak İsteyenler: Farklı bir sektöre veya pozisyona geçmek isteyen ancak nereden başlayacağını bilemeyen profesyoneller.
Mevcut Kariyerinde İlerlemek İsteyenler: Kendi performansını ve durumunu objektif bir şekilde değerlendirerek gelişim alanlarını keşfetmek isteyen çalışanlar.
Kendini Geliştirmeyi Amaç Edinmiş Herkes: Sürekli öğrenme ve kişisel gelişim motivasyonuna sahip olan tüm bireyler.

Kariyer Koçu AI" Projesinde Kullanılan Teknolojiler ve Araçlar Raporu
Bu rapor, "Kariyer Koçu AI" adlı web uygulamasının geliştirilmesinde kullanılan temel teknolojileri, kütüphaneleri ve araçları detaylandırmaktadır.
1. Arka Plan (Backend) Teknolojileri
Arka plan, projenin sunucu tarafında çalışan, iş mantığını yürüten ve verileri işleyen motorudur.
•	Python: Projenin ana programlama dilidir. Esnek yapısı, geniş kütüphane desteği ve okunabilirliği nedeniyle tercih edilmiştir.
•	Flask: Hafif ve modüler bir web çatısıdır (framework). Gelen web isteklerini karşılamak, URL yollarını (/login, /dashboard vb.) yönetmek ve kullanıcılara HTML sayfaları göndermek için kullanılmıştır.
•	Gunicorn: Canlı sunucu ortamında (PythonAnywhere), Flask uygulamasını birden çok isteğe aynı anda cevap verebilecek şekilde performanslı ve stabil bir şekilde çalıştıran bir "WSGI HTTP Server"dır.
2. Ön Yüz (Frontend) Teknolojileri
Ön yüz, kullanıcının doğrudan tarayıcısında gördüğü ve etkileşime girdiği görsel arayüzdür.
•	HTML5 (HyperText Markup Language): Web sayfalarının iskeletini ve temel yapısını (başlıklar, formlar, butonlar, metin alanları) oluşturmak için kullanılmıştır.
•	CSS3 (Cascading Style Sheets): HTML iskeletini biçimlendirmek, renklendirmek, hizalamak ve uygulamanın modern, temiz ve kullanıcı dostu bir tasarıma sahip olmasını sağlamak için kullanılmıştır.
•	JavaScript: Kullanıcı deneyimini interaktif hale getiren dildir.
o	AJAX (Fetch API ile): Sayfanın tamamen yenilenmesine gerek kalmadan sunucuyla (ve dolayısıyla yapay zeka ile) arka planda iletişim kurmayı sağlamıştır. Bu sayede "Analiz Et" butonuna basıldığında sonuçlar anında ilgili kutucuğa gelmiştir.
o	DOM Manipulation: Dosya seçildiğinde adını gösterme, bildirim kutularını (modal) gösterme/gizleme gibi dinamik arayüz değişiklikleri için kullanılmıştır.
•	Jinja2: Flask ile birlikte gelen bir şablon motorudur. Arka plandan (Python) gelen verileri (örn: kullanıcı bilgileri, analiz sonuçları) HTML sayfalarının içine dinamik olarak yerleştirmemizi sağlamıştır.
3. Yapay Zeka (AI) Teknolojileri
Projenin "akıllı" özelliklerini sağlayan teknolojilerdir.
•	Büyük Dil Modeli (LLM - Large Language Model): Projenin zeka katmanıdır.
o	Kullanılan Model: Google Gemini (gemini-1.5-flash-latest).
o	Görevi: Metin anlama, analiz etme (duygu, içerik), özetleme ve kullanıcı girdilerine göre yeni, anlamlı metinler (öneriler, eylem planları) üretme.
•	Google Generative AI API: Gemini modeline ağ üzerinden istek gönderip cevap almamızı sağlayan arayüzdür.
•	google-generativeai Kütüphanesi: Python kodumuzun, bu API ile doğrudan ve kolayca iletişim kurmasını sağlayan resmi Google kütüphanesidir.
•	Prompt Engineering (Komut Tasarımı): LLM'den istediğimiz spesifik rolleri (İK uzmanı, empatik koç vb.) üstlenmesini ve istediğimiz formatta cevaplar vermesini sağlamak için ai/analyzer.py dosyası içinde her görev için özel olarak tasarladığımız detaylı metin komutlarıdır.
4. Veritabanı Teknolojileri
Kullanıcı bilgilerini ve uygulama verilerini kalıcı olarak saklamak için kullanılmıştır.
•	SQLite: Geliştirme sürecinde ve PythonAnywhere'in ücretsiz planında kullanılan, basit, sunucusuz ve dosya tabanlı bir veritabanı motorudur.
•	SQLAlchemy: Python'un en güçlü ORM (Object-Relational Mapper) kütüphanesidir. Veritabanı tablolarını (User, Goal, Cv vb.) Python sınıfları olarak tanımlamamızı ve karmaşık SQL sorguları yazmadan tüm veritabanı işlemlerini (veri ekleme, silme, güncelleme, sorgulama) Python koduyla yapmamızı sağlamıştır.
5. Geliştirme ve Dağıtım (DevOps) Araçları
Projenin geliştirme sürecini yönetmek ve internette yayınlamak için kullanılan araçlardır.
•	PyCharm: Proje kodlarını yazdığımız, düzenlediğimiz ve test ettiğimiz Entegre Geliştirme Ortamıdır (IDE).
•	Git: Kodumuzda yaptığımız tüm değişiklikleri kaydetmemizi ve takip etmemizi sağlayan versiyon kontrol sistemidir.
•	GitHub: Git ile yönettiğimiz projemizi bulutta sakladığımız, yedeklediğimiz ve sunucuya aktarmak için kullandığımız web tabanlı bir hizmettir.
•	PythonAnywhere: Projemizi localhost'tan çıkarıp, tüm dünyanın bir web adresi üzerinden erişebileceği gerçek bir sunucuda barındırmak (hosting) ve çalıştırmak için kullandığımız Platform-as-a-Service (PaaS) sağlayıcısıdır.
•	Diğer Kütüphaneler:
o	bcrypt: Şifreleri güvenli bir şekilde hash'leyerek veritabanında saklamak için.
o	PyPDF2: CV yükleme özelliğinde, PDF dosyalarının içeriğini okumak için.
o	python-dotenv: Gizli API anahtarını .env dosyasında güvenli bir şekilde saklamak için

