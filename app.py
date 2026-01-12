import streamlit as st
import google.generativeai as genai
import os

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="Eco-Gemini: Karbon Ayak İzi Ölçer", page_icon="🌱")

# --- API KURULUMU ---
# Not: Bu uygulamanın çalışması için Google AI Studio'dan bir API anahtarı almalısınız.
# Gerçek uygulamada API anahtarını st.secrets içine koymalısınız.
api_key = st.sidebar.text_input("Google Gemini API Anahtarınızı Girin:", type="password")

if api_key:
    genai.configure(api_key=api_key)

# --- BAŞLIK VE AÇIKLAMA ---
st.title("🌍 Eco-Gemini: Günlük Karbon Ayak İzi Asistanı")
st.markdown("""
Bu uygulama, günlük aktivitelerinizi analiz eder, karbon ayak izinizi hesaplar ve
dünyayı korumanız için size özel tavsiyeler verir.
""")

st.divider()

# --- KULLANICI GİRDİSİ ---
user_input = st.text_area(
    "Bugün neler yaptınız? (Örn: 10km araba kullandım, kırmızı et yedim, 1 saat oyun oynadım...)",
    height=150
)

# --- YAPAY ZEKA ANALİZ FONKSİYONU ---
def analyze_carbon_footprint(text):
    # Gemini Modeli Tanımlama
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    Sen uzman bir çevre mühendisi ve sürdürülebilirlik danışmanısın.
    Aşağıdaki metinde kullanıcının günlük aktiviteleri yer alıyor.
    
    Görevlerin:
    1. Metindeki aktiviteleri analiz et.
    2. Her aktivite için tahmini karbon ayak izini (kg CO2e cinsinden) hesapla.
    3. Toplam karbon ayak izini hesapla.
    4. Bu karbon ayak izini azaltmak için kullanıcıya özel, uygulanabilir 3 tavsiye ver.
    
    Çıktıyı şu formatta ver (Markdown kullanarak):
    
    ### 📊 Günlük Analiz
    * **Aktivite 1:** [Miktar] kg CO2e
    * **Aktivite 2:** [Miktar] kg CO2e
    ...
    
    **📉 Toplam Tahmini Karbon Ayak İzi:** [Toplam Sayı] kg CO2e
    
    ---
    ### 🌱 Yeşil Tavsiyeler
    1. [Tavsiye 1]
    2. [Tavsiye 2]
    3. [Tavsiye 3]
    
    Kullanıcı Metni: "{text}"
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Hata oluştu: {str(e)}"

# --- HESAPLA BUTONU ---
if st.button("Karbon Ayak İzimi Hesapla"):
    if not api_key:
        st.warning("Lütfen önce sol menüden Gemini API anahtarınızı girin.")
    elif not user_input:
        st.warning("Lütfen günlük aktivitelerinizi yazın.")
    else:
        with st.spinner("Gemini aktivitelerini analiz ediyor..."):
            result = analyze_carbon_footprint(user_input)
            st.markdown(result)
            
            # Motivasyon Mesajı
            st.success("Gezegen için attığın her adım değerli! 🌍")

# --- FOOTER ---
st.divider()
st.caption("Bu uygulama Google Gemini API kullanılarak oluşturulmuştur.")
