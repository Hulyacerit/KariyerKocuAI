import os
import google.generativeai as genai
from dotenv import load_dotenv

# .env dosyasındaki API anahtarını yükle
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")

# API anahtarı ile Gemini'yi yapılandır
genai.configure(api_key=GEMINI_API_KEY)

# Üretken modelimizi seçiyoruz
model = genai.GenerativeModel('gemini-1.5-flash-latest')

def get_analysis(text: str) -> str:
    """
    Verilen metni objektif bir şekilde analiz eder.
    """
    prompt = f"""
    Aşağıdaki metin, bir kullanıcının günlüğünden alınmıştır. Bu metni bir kariyer koçu gibi, 
    ancak tamamen objektif ve duygusal olmayan bir perspektiften analiz et. 
    Kullanıcının durumunu, duygusal tepkilerini ve olayın potansiyel nedenlerini yorumla. 
    Kullanıcının haklı veya haksız olduğuna dair kesin bir yargıda bulunmak yerine, 
    durumu farklı açılardan değerlendir. Analizini maddeler halinde sun.

    Metin: "{text}"
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API hatası (Analiz): {e}")
        return "Analiz sırasında bir hata oluştu. Lütfen API anahtarınızı ve bağlantınızı kontrol edin."

def get_suggestion(text: str) -> str:
    """
    Verilen metne göre yapıcı ve sakinleştirici öneriler sunar.
    """
    prompt = f"""
    Aşağıdaki metin, bir kullanıcının günlüğünden alınmıştır ve stresli veya olumsuz bir durumu anlatmaktadır. 
    Empatik ve destekleyici bir kariyer koçu gibi davranarak, kullanıcının stresini ve öfkesini yönetmesine yardımcı olacak, 
    uygulanabilir ve somut önerilerde bulun. Önerilerin hem durumu çözmeye yönelik (iletişim gibi) hem de 
    kişisel rahatlamaya yönelik (meditasyon, fiziksel aktivite gibi) olsun. Önerilerini maddeler halinde sun.

    Metin: "{text}"
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API hatası (Öneri): {e}")
        return "Öneri getirilirken bir hata oluştu. Lütfen API anahtarınızı ve bağlantınızı kontrol edin."

def get_goal_suggestion(text: str) -> str:
    """
    Verilen bir hedefi gerçekleştirmek için adım adım öneriler sunar.
    """
    prompt = f"""
    Bir kullanıcı kariyeri veya kişisel gelişimi için aşağıdaki hedefi belirlemiştir. 
    Proaktif ve yol gösterici bir kariyer koçu gibi davran. Bu hedefi, S.M.A.R.T. 
    (Özgül, Ölçülebilir, Ulaşılabilir, Gerçekçi, Zamanında) prensiplerine uygun, 
    küçük ve yönetilebilir adımlara ayırarak bir eylem planı oluştur. 
    Kullanıcıya motivasyonunu yüksek tutması için ipuçları da ver. 
    Cevabını net başlıklar ve maddeler halinde sun.

    Hedef: "{text}"
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API hatası (Hedef Önerisi): {e}")
        return "Hedef önerisi getirilirken bir hata oluştu. Lütfen API anahtarınızı ve bağlantınızı kontrol edin."

def analyze_cv(cv_text: str) -> str:
    """
    Verilen CV metnini yazım, format ve içerik açısından analiz eder.
    """
    prompt = f"""
    Profesyonel bir İnsan Kaynakları (İK) uzmanı gibi davran. Aşağıdaki CV metnini incele.
    - Yazım ve dil bilgisi hatalarını bul ve düzeltmelerini öner.
    - Anlaşılması güç veya zayıf ifadeleri belirle ve daha etkili alternatifler sun.
    - CV'nin genel formatı ve okunabilirliği hakkında geri bildirimde bulun.
    Bulgularını net başlıklar altında ("Yazım Hataları", "İfade Önerileri", "Format") maddeler halinde sun.

    CV Metni: "{cv_text}"
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API hatası (CV Analizi): {e}")
        return "CV analizi sırasında bir hata oluştu."

def suggest_cv_improvements(cv_text: str, company: str, position: str) -> str:
    """
    CV'yi belirli bir şirket ve pozisyon için nasıl daha iyi hale getirileceğini önerir.
    """
    prompt = f"""
    "{company}" şirketindeki "{position}" pozisyonu için deneyimli bir İK yöneticisi gibi davran.
    Aşağıdaki CV metnini bu özel başvuru için değerlendir.
    - CV'deki mevcut yetenek ve deneyimlerin bu pozisyonla ne kadar örtüştüğünü vurgula.
    - Bu pozisyon için CV'de eksik olan veya daha fazla vurgulanması gereken anahtar kelimeleri, yetenekleri veya proje deneyimlerini belirle.
    - Adayın bu pozisyona daha uygun görünmesi için CV'sine ekleyebileceği somut öneriler sun.
    Cevabını "Güçlü Yönler" ve "Geliştirme Önerileri" olmak üzere iki ana başlık altında maddeler halinde sun.

    CV Metni: "{cv_text}"
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API hatası (CV Önerisi): {e}")
        return "CV için öneri getirilirken bir hata oluştu."

def get_holistic_analysis(user_profile: dict, diary_entries: list, goals: list, cv_text: str) -> str:
    """
    Kullanıcının tüm verilerini birleştirerek bütünsel bir kariyer analizi ve önerisi sunar.
    """
    full_context = f"""
    KULLANICI PROFİLİ:
    - Kariyer Hedefi: {user_profile.get('kariyer_hedefi', 'Belirtilmemiş')}
    - Eğitim Durumu: {user_profile.get('egitim_durumu', 'Belirtilmemiş')}
    - İş Deneyimi: {user_profile.get('is_deneyimi', 0)} yıl

    SON GÜNLÜK YAZILARI:
    {''.join([f'- {entry}\\n' for entry in diary_entries]) if diary_entries else 'Günlük yazısı yok.'}

    MEVCUT HEDEFLERİ:
    {''.join([f'- {goal}\\n' for goal in goals]) if goals else 'Belirlenmiş hedef yok.'}

    CV METNİ:
    {cv_text if cv_text else 'CV yüklenmemiş.'}
    """
    prompt = f"""
    Sen bir duayen, son derece deneyimli ve empatik bir kariyer koçusun. Aşağıda, bir kullanıcının uygulamaya girdiği tüm veriler bulunmaktadır. 
    Bu bütünsel bilgiyi kullanarak, kullanıcı için derinlemesine bir kariyer analizi yap ve yol haritası sun.
    Cevabını aşağıdaki 3 başlık altında, maddeler halinde ve profesyonel bir dille oluştur:

    1.  **Mevcut Durum Analizi:** Kullanıcının profili, günlüklerindeki ruh hali ve hedefleri arasındaki bağlantıyı veya çelişkileri yorumla. Güçlü yönlerini ve potansiyel engellerini belirle.
    2.  **Kariyer Hedefine Yönelik Strateji:** Belirttiği kariyer hedefine ulaşması için, mevcut hedeflerini ve CV'sini nasıl daha uyumlu hale getirebileceğini anlat. Hangi yeteneklerini geliştirmesi gerektiğini belirt.
    3.  **3 Somut Eylem Adımı:** Kullanıcının hemen bugün veya bu hafta başlayabileceği, motivasyonunu artıracak ve onu hedefine yaklaştıracak 3 adet net ve uygulanabilir tavsiye ver.

    Kullanıcının Verileri:
    {full_context}
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API hatası (Bütünsel Analiz): {e}")
        return "Genel analiz yapılırken bir hata oluştu."

def compare_cvs_for_job(cv_text_1: str, cv_text_2: str, company: str, position: str) -> str:
    """
    İki farklı CV metnini, belirli bir şirket ve pozisyon için karşılaştırır.
    """
    prompt = f"""
    Sen, "{company}" şirketinde "{position}" pozisyonu için işe alım yapan, çok deneyimli bir İK yöneticisisin. 
    Görevin, aşağıda metinleri verilen iki farklı CV'yi bu pozisyon için karşılaştırmak.
    Değerlendirmeni aşağıdaki formatta, net ve profesyonel bir dille yap:

    1.  **CV 1 - Genel Değerlendirme:**
        - Bu CV'nin pozisyon için en güçlü yönleri neler?
        - Bu CV'nin pozisyon için en zayıf yönleri veya eksikleri neler?

    2.  **CV 2 - Genel Değerlendirme:**
        - Bu CV'nin pozisyon için en güçlü yönleri neler?
        - Bu CV'nin pozisyon için en zayıf yönleri veya eksikleri neler?

    3.  **Karşılaştırma ve Sonuç:**
        - İki CV'yi yan yana değerlendir. Hangisi bu spesifik başvuru için daha etkili ve neden?
        - Nihai olarak hangi adayla mülakata devam etmeyi tercih ederdin? Kararını net bir şekilde gerekçelendir.

    ---
    CV 1 METNİ:
    "{cv_text_1}"
    ---
    CV 2 METNİ:
    "{cv_text_2}"
    ---
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini API hatası (CV Karşılaştırma): {e}")
        return "CV'ler karşılaştırılırken bir hata oluştu."