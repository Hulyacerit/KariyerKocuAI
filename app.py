import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
import bcrypt
from datetime import datetime
from database import SessionLocal, User, DiaryEntry, AnalysisResult, Goal, Cv, EgitimDurumu, Cinsiyet
from sqlalchemy import desc
from werkzeug.utils import secure_filename
import PyPDF2

# ai.analyzer modülünden TÜM fonksiyonları içeri aktarıyoruz
from ai.analyzer import (
    get_analysis, get_suggestion, get_goal_suggestion,
    analyze_cv, suggest_cv_improvements, compare_cvs_for_job,
    get_holistic_analysis
)

# YENİ VE DOĞRU HALİ:
app = Flask(__name__)

# Projenin ana dizininin tam yolunu alıyoruz (örn: /home/Hulya5/KariyerKocuAI)
basedir = os.path.abspath(os.path.dirname(__file__))
# 'uploads' klasörünün tam yolunu oluşturuyoruz
UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
ALLOWED_EXTENSIONS = {'pdf'}

app.secret_key = 'cok_gizli_bir_anahtar_buraya_yazin'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# --- GİRİŞ, KAYIT, ÇIKIŞ (Temel Fonksiyonlar) ---
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        email = request.form.get('email').strip()
        password = request.form.get('password')
        if not email or not password:
            flash('Lütfen tüm alanları doldurun.', 'danger')
            return redirect(url_for('home'))
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == email).first()
            if user and bcrypt.checkpw(password.encode('utf-8'), user.hashed_password.encode('utf-8')):
                session['user_id'] = user.id
                session['user_name'] = user.ad_soyad
                flash('Başarıyla giriş yaptınız!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('E-posta veya şifre hatalı.', 'danger')
                return redirect(url_for('home'))
        finally:
            db.close()
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        email = request.form.get('email').strip()
        ad_soyad = request.form.get('ad_soyad').strip()
        yas_str = request.form.get('yas').strip()
        cinsiyet = request.form.get('cinsiyet')
        egitim_durumu = request.form.get('egitim_durumu')
        is_deneyimi_str = request.form.get('is_deneyimi').strip()
        kariyer_hedefi = request.form.get('kariyer_hedefi').strip()
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        if not all([email, ad_soyad, yas_str, cinsiyet, egitim_durumu, password, password_confirm]):
            flash('Lütfen tüm zorunlu alanları doldurun.', 'danger')
            return redirect(url_for('register_page'))
        if password != password_confirm:
            flash('Girdiğiniz şifreler uyuşmuyor.', 'danger')
            return redirect(url_for('register_page'))
        try:
            yas = int(yas_str)
            is_deneyimi = int(is_deneyimi_str) if is_deneyimi_str else None
        except ValueError:
            flash('Yaş ve İş Deneyimi alanları sayısal bir değer olmalıdır.', 'danger')
            return redirect(url_for('register_page'))
        db = SessionLocal()
        try:
            existing_user = db.query(User).filter(User.email == email).first()
            if existing_user:
                flash('Bu e-posta adresi zaten kayıtlı.', 'danger')
                return redirect(url_for('register_page'))
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            yeni_kullanici = User(
                email=email, ad_soyad=ad_soyad, yas=yas, cinsiyet=cinsiyet, egitim_durumu=egitim_durumu,
                is_deneyimi=is_deneyimi, kariyer_hedefi=kariyer_hedefi, hashed_password=hashed_password.decode('utf-8')
            )
            db.add(yeni_kullanici)
            db.commit()
            flash('Kaydınız başarıyla oluşturuldu! Lütfen giriş yapın.', 'success')
            return redirect(url_for('home'))
        finally:
            db.close()
    egitim_seviyeleri = [e.value for e in EgitimDurumu]
    cinsiyetler = [c.value for c in Cinsiyet]
    return render_template('register.html', egitim_opsiyonlari=egitim_seviyeleri, cinsiyet_opsiyonlari=cinsiyetler)


@app.route('/logout')
def logout():
    session.clear()
    flash('Başarıyla çıkış yaptınız.', 'success')
    return redirect(url_for('home'))


# --- DASHBOARD (Tüm Sayfaların Verilerini Çeken Ana Fonksiyon) ---
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Bu sayfayı görüntülemek için giriş yapmalısınız.', 'danger')
        return redirect(url_for('home'))

    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == session['user_id']).first()
        if not user:
            session.clear()
            return redirect(url_for('home'))

        page = request.args.get('page', 'profil')
        data = {}

        if page == 'gunluk':
            data['entries'] = db.query(DiaryEntry).filter(DiaryEntry.user_id == user.id).order_by(
                desc(DiaryEntry.created_at)).all()
        elif page == 'hedefler':
            data['goals'] = db.query(Goal).filter(Goal.user_id == user.id).order_by(desc(Goal.end_date)).all()
        elif page == 'analiz_gecmisi':
            history_type = request.args.get('history_type')
            data['history_type'] = history_type
            if history_type == 'gunluk':
                data['results'] = db.query(AnalysisResult).filter(AnalysisResult.user_id == user.id,
                                                                  AnalysisResult.analysis_type.in_(
                                                                      ['Analiz', 'Öneri'])).order_by(
                    desc(AnalysisResult.created_at)).all()
            elif history_type == 'cv':
                data['results'] = db.query(AnalysisResult).filter(AnalysisResult.user_id == user.id,
                                                                  AnalysisResult.analysis_type.in_(
                                                                      ['CV Analizi', 'CV Önerisi'])).order_by(
                    desc(AnalysisResult.created_at)).all()
        elif page == 'genel_oneriler':
            suggestion_type = request.args.get('suggestion_type')
            data['suggestion_type'] = suggestion_type
            if suggestion_type == 'gunluk':
                data['results'] = db.query(AnalysisResult).filter(AnalysisResult.user_id == user.id,
                                                                  AnalysisResult.analysis_type == 'Öneri').order_by(
                    desc(AnalysisResult.created_at)).all()
            elif suggestion_type == 'hedefler':
                data['results'] = db.query(AnalysisResult).filter(AnalysisResult.user_id == user.id,
                                                                  AnalysisResult.analysis_type == 'Hedef Önerisi').order_by(
                    desc(AnalysisResult.created_at)).all()
            elif suggestion_type == 'cv':
                data['results'] = db.query(AnalysisResult).filter(AnalysisResult.user_id == user.id,
                                                                  AnalysisResult.analysis_type == 'CV Önerisi').order_by(
                    desc(AnalysisResult.created_at)).all()

        return render_template('dashboard.html', user=user, page=page, data=data)
    finally:
        db.close()


# --- HEDEF YÖNETİMİ (CRUD) ---
@app.route('/add_goal', methods=['POST'])
def add_goal():
    if 'user_id' not in session: return redirect(url_for('home'))
    content = request.form.get('content')
    start_date_str = request.form.get('start_date')
    end_date_str = request.form.get('end_date')
    if not all([content, start_date_str, end_date_str]):
        flash('Hedef içeriği ve tarihler boş bırakılamaz.', 'danger')
        return redirect(url_for('dashboard', page='hedefler'))
    db = SessionLocal()
    try:
        new_goal = Goal(content=content, start_date=datetime.strptime(start_date_str, '%Y-%m-%d').date(),
                        end_date=datetime.strptime(end_date_str, '%Y-%m-%d').date(), user_id=session['user_id'])
        db.add(new_goal)
        db.commit()
        flash('Yeni hedefiniz başarıyla eklendi.', 'success')
    finally:
        db.close()
    return redirect(url_for('dashboard', page='hedefler'))


@app.route('/update_goal/<int:goal_id>', methods=['POST'])
def update_goal(goal_id):
    if 'user_id' not in session: return redirect(url_for('home'))
    db = SessionLocal()
    try:
        goal = db.query(Goal).filter(Goal.id == goal_id, Goal.user_id == session['user_id']).first()
        if goal:
            goal.content = request.form.get('content')
            goal.start_date = datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date()
            goal.end_date = datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date()
            db.commit()
            flash('Hedefiniz güncellendi.', 'success')
    finally:
        db.close()
    return redirect(url_for('dashboard', page='hedefler'))


@app.route('/delete_goal/<int:goal_id>', methods=['POST'])
def delete_goal(goal_id):
    if 'user_id' not in session: return redirect(url_for('home'))
    db = SessionLocal()
    try:
        goal = db.query(Goal).filter(Goal.id == goal_id, Goal.user_id == session['user_id']).first()
        if goal:
            db.delete(goal)
            db.commit()
            flash('Hedefiniz silindi.', 'success')
    finally:
        db.close()
    return redirect(url_for('dashboard', page='hedefler'))


# --- CV YÖNETİMİ ---
@app.route('/upload_cv', methods=['POST'])
def upload_cv():
    if 'user_id' not in session: return jsonify({"error": "Lütfen giriş yapın."}), 401
    if 'cv_file' not in request.files: return jsonify({"error": "Dosya bulunamadı."}), 400
    file = request.files['cv_file']
    if file.filename == '': return jsonify({"error": "Dosya seçilmedi."}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        extracted_text = ""
        try:
            with open(filepath, 'rb') as f:
                for page in PyPDF2.PdfReader(f).pages: extracted_text += page.extract_text()
        except Exception as e:
            return jsonify({"error": f"PDF okuma hatası: {e}"}), 500
        return jsonify({"success": True, "extracted_text": extracted_text})
    return jsonify({"error": "Geçersiz dosya türü, sadece PDF kabul edilir."}), 400


@app.route('/compare_cvs', methods=['POST'])
def compare_cvs():
    if 'user_id' not in session: return jsonify({"error": "Lütfen giriş yapın."}), 401
    if 'cv_file_1' not in request.files or 'cv_file_2' not in request.files: return jsonify(
        {"error": "Lütfen karşılaştırmak için iki CV dosyası da seçin."}), 400
    file1, file2 = request.files['cv_file_1'], request.files['cv_file_2']
    company, position = request.form.get('target_company', ''), request.form.get('target_position', '')
    if file1.filename == '' or file2.filename == '': return jsonify({"error": "Lütfen iki dosya da seçin."}), 400
    if not position: return jsonify({"error": "Lütfen başvurulacak pozisyonu belirtin."}), 400
    cv_text_1, cv_text_2 = "", ""
    try:
        for page in PyPDF2.PdfReader(file1.stream).pages: cv_text_1 += page.extract_text()
        for page in PyPDF2.PdfReader(file2.stream).pages: cv_text_2 += page.extract_text()
        if not cv_text_1 or not cv_text_2: return jsonify(
            {"error": "PDF dosyalarından metin okunurken sorun oluştu."}), 500
    except Exception as e:
        return jsonify({"error": f"PDF okuma hatası: {e}"}), 500
    ai_response = compare_cvs_for_job(cv_text_1, cv_text_2, company, position)
    if "hata oluştu" not in ai_response:
        db = SessionLocal()
        try:
            new_analysis = AnalysisResult(
                request_text=f"CV Karşılaştırma:\n- Şirket: {company}\n- Pozisyon: {position}",
                response_text=ai_response, analysis_type='CV Karşılaştırma', user_id=session['user_id'])
            db.add(new_analysis)
            db.commit()
        finally:
            db.close()
    return jsonify({"response": ai_response})


# --- YAPAY ZEKA API ROUTE'LARI ---
@app.route('/get_ai_response', methods=['POST'])
def get_ai_response():
    if 'user_id' not in session: return jsonify({"error": "Lütfen giriş yapın."}), 401
    data = request.get_json()
    text, action_type = data.get('text'), data.get('action_type')
    if not text or not action_type: return jsonify({"error": "Eksik bilgi gönderildi."}), 400

    action_map = {
        'analyze': (get_analysis, 'Analiz'),
        'suggest': (get_suggestion, 'Öneri'),
        'goal_suggest': (get_goal_suggestion, 'Hedef Önerisi'),
        'cv_analyze': (analyze_cv, 'CV Analizi'),
        'cv_suggest': (suggest_cv_improvements, 'CV Önerisi'),
    }

    if action_type in action_map:
        ai_function, db_type = action_map[action_type]
        if action_type == 'cv_suggest':
            company, position = data.get('company', ''), data.get('position', '')
            ai_response = ai_function(text, company, position)
        else:
            ai_response = ai_function(text)
    else:
        return jsonify({"error": "Geçersiz işlem türü."}), 400

    if "hata oluştu" not in ai_response:
        db = SessionLocal()
        try:
            new_analysis = AnalysisResult(request_text=text, response_text=ai_response, analysis_type=db_type,
                                          user_id=session['user_id'])
            db.add(new_analysis)
            db.commit()
        finally:
            db.close()
    return jsonify({"response": ai_response})


@app.route('/get_holistic_analysis', methods=['POST'])
def holistic_analysis():
    if 'user_id' not in session: return jsonify({"error": "Lütfen giriş yapın."}), 401
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == session['user_id']).first()
        if not user: return jsonify({"error": "Kullanıcı bulunamadı."}), 404
        user_profile = {"kariyer_hedefi": user.kariyer_hedefi, "egitim_durumu": user.egitim_durumu.value,
                        "is_deneyimi": user.is_deneyimi}
        diary_entries = [e.content for e in db.query(DiaryEntry).filter(DiaryEntry.user_id == user.id).order_by(
            desc(DiaryEntry.created_at)).limit(5).all()]
        goals = [g.content for g in db.query(Goal).filter(Goal.user_id == user.id).all()]
        latest_cv = db.query(Cv).filter(Cv.user_id == user.id).order_by(desc(Cv.created_at)).first()
        cv_text = latest_cv.extracted_text if latest_cv else ""
        ai_response = get_holistic_analysis(user_profile, diary_entries, goals, cv_text)
        if "hata oluştu" not in ai_response:
            new_analysis = AnalysisResult(request_text="Genel Kariyer Analizi İsteği", response_text=ai_response,
                                          analysis_type='Genel Analiz', user_id=session['user_id'])
            db.add(new_analysis)
            db.commit()
        return jsonify({"response": ai_response})
    finally:
        db.close()


if __name__ == '__main__':
    # Sunucunun bize verdiği portu kullan, eğer yoksa (yerel bilgisayarda) 5000'i kullan
    port = int(os.environ.get("PORT", 5000))
    # host='0.0.0.0' ayarı, uygulamanın dışarıdan gelen bağlantıları kabul etmesini sağlar
    app.run(host='0.0.0.0', port=port, debug=True)