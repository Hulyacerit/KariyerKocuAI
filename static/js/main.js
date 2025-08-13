document.addEventListener('DOMContentLoaded', function() {

    // --- Genel Modal Kodu ---
    const overlay = document.getElementById('alert-overlay');
    const customAlert = document.getElementById('custom-alert');
    const alertMessage = document.getElementById('alert-message');
    const okButton = document.getElementById('alert-ok-btn');

    function showAlert(message) {
        if (customAlert) {
            alertMessage.textContent = message;
            overlay.style.display = 'block';
            customAlert.style.display = 'block';
        }
    }
    function hideAlert() {
        if (customAlert) {
            overlay.style.display = 'none';
            customAlert.style.display = 'none';
        }
    }

    if (okButton) { okButton.addEventListener('click', hideAlert); }
    if (overlay) { overlay.addEventListener('click', hideAlert); }

    // --- Günlük Sayfası Mantığı ---
    const diaryContent = document.getElementById('diary-content');
    if (diaryContent) {
        // ... (Bu bölüm öncekiyle aynı, değişiklik yok) ...
        const diaryDateInput = document.getElementById('diary-date');
        const selectedDateDisplay = document.getElementById('selected-date-display');
        const diarySuggestButton = document.getElementById('btn-suggest');
        const diaryAnalyzeButton = document.getElementById('btn-analyze');
        const diaryResultBox = document.getElementById('ai-result-box');
        const diaryLoadingSpinner = document.getElementById('loading-spinner');
        const today = new Date().toISOString().split('T')[0];
        diaryDateInput.value = today;
        updateDateDisplay(today);
        diaryDateInput.addEventListener('change', (event) => { updateDateDisplay(event.target.value); });
        function updateDateDisplay(dateString) {
            const date = new Date(dateString);
            const options = { year: 'numeric', month: 'long', day: 'numeric', weekday: 'long' };
            selectedDateDisplay.textContent = date.toLocaleDateString('tr-TR', options) + " Günü";
        }
        diarySuggestButton.addEventListener('click', () => { fetchDiaryAIResponse('suggest'); });
        diaryAnalyzeButton.addEventListener('click', () => { fetchDiaryAIResponse('analyze'); });
        async function fetchDiaryAIResponse(actionType) {
            const text = diaryContent.value;
            if (!text.trim()) { showAlert("Lütfen bir metin girin."); return; }
            diaryLoadingSpinner.style.display = 'block';
            diaryResultBox.innerHTML = '';
            try {
                const response = await fetch('/get_ai_response', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text, action_type: actionType }),
                });
                const data = await response.json();
                if (response.ok) {
                    diaryResultBox.innerHTML = data.response.replace(/\n/g, '<br>').replace(/\*/g, '<b>&bull;</b>');
                } else { showAlert(data.error || 'Bilinmeyen bir hata oluştu.'); }
            } catch (error) { showAlert('Sunucuyla iletişim kurulamadı.'); }
            finally { diaryLoadingSpinner.style.display = 'none'; }
        }
    }

    // --- Hedefler Sayfası Mantığı ---
    const goalForm = document.getElementById('goal-form');
    if (goalForm) {
        // ... (Bu bölüm öncekiyle aynı, değişiklik yok) ...
        const goalIdInput = document.getElementById('goal_id_input');
        const goalContentInput = document.getElementById('goal-content-input');
        const goalStartDateInput = document.getElementById('start_date');
        const goalEndDateInput = document.getElementById('end_date');
        const clearGoalFormBtn = document.getElementById('clear-goal-form-btn');
        const goalResultBox = document.getElementById('goal-ai-result-box');
        const goalLoadingSpinner = document.getElementById('goal-loading-spinner');
        document.querySelectorAll('.btn-goal-suggest').forEach(button => {
            button.addEventListener('click', function() {
                const goalCard = this.closest('.goal-card');
                const goalText = goalCard.dataset.content;
                fetchGoalAIResponse(goalText);
            });
        });
        document.querySelectorAll('.btn-edit-goal').forEach(button => {
            button.addEventListener('click', function() {
                const goalCard = this.closest('.goal-card');
                goalIdInput.value = goalCard.dataset.goalId;
                goalContentInput.value = goalCard.dataset.content;
                goalStartDateInput.value = goalCard.dataset.start;
                goalEndDateInput.value = goalCard.dataset.end;
                goalForm.action = `/update_goal/${goalCard.dataset.goalId}`;
                clearGoalFormBtn.style.display = 'inline-block';
                window.scrollTo(0, 0);
            });
        });
        clearGoalFormBtn.addEventListener('click', function() {
            goalIdInput.value = '';
            goalContentInput.value = '';
            goalStartDateInput.value = '';
            goalEndDateInput.value = '';
            goalForm.action = "/add_goal";
            this.style.display = 'none';
        });
        async function fetchGoalAIResponse(text) {
            if (!text.trim()) { showAlert("Öneri getirilecek bir hedef metni bulunamadı."); return; }
            goalLoadingSpinner.style.display = 'block';
            goalResultBox.innerHTML = '';
            try {
                const response = await fetch('/get_ai_response', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ text: text, action_type: 'goal_suggest' }),
                });
                const data = await response.json();
                if (response.ok) {
                    goalResultBox.innerHTML = data.response.replace(/\n/g, '<br>').replace(/\*/g, '<b>&bull;</b>');
                } else { showAlert(data.error || 'Bilinmeyen bir hata oluştu.'); }
            } catch (error) { showAlert('Sunucuyla iletişim kurulamadı.'); }
            finally { goalLoadingSpinner.style.display = 'none'; }
        }
    }

    // --- CV Sayfası Kodu (İKİ BÖLÜMLÜ YENİ TASARIMA UYGUN) ---
    const singleCvForm = document.getElementById('single-cv-form');
    if (singleCvForm) {
        // Gerekli tüm elementleri yeni ID'lerine göre seçiyoruz
        const singleCvFileInput = document.getElementById('cv_file_single');
        const singleFileChosenText = singleCvFileInput.parentElement.querySelector('.file-chosen-text');

        const cvFileInput1 = document.getElementById('cv_file_1');
        const fileChosenText1 = cvFileInput1.parentElement.querySelector('.file-chosen-text');
        const cvFileInput2 = document.getElementById('cv_file_2');
        const fileChosenText2 = cvFileInput2.parentElement.querySelector('.file-chosen-text');

        const companyInput = document.getElementById('target_company_single');
        const positionInput = document.getElementById('target_position_single');

        const suggestButton = document.getElementById('btn-cv-suggest-single');
        const analyzeButton = document.getElementById('btn-cv-analyze-single');
        const compareButton = document.getElementById('btn-cv-compare');

        const resultBox = document.getElementById('cv-ai-result-box');
        const loadingSpinner = document.getElementById('cv-loading-spinner');

        // ==========================================================
        // EKSİK OLAN DOSYA ADI GÜNCELLEME MANTIĞI BURADA
        // ==========================================================
        singleCvFileInput.addEventListener('change', function() {
            singleFileChosenText.textContent = this.files.length > 0 ? this.files[0].name : 'Dosya seçilmedi';
        });
        cvFileInput1.addEventListener('change', function() {
            fileChosenText1.textContent = this.files.length > 0 ? this.files[0].name : 'Dosya seçilmedi';
        });
        cvFileInput2.addEventListener('change', function() {
            fileChosenText2.textContent = this.files.length > 0 ? this.files[0].name : 'Dosya seçilmedi';
        });
        // ==========================================================

        // Olay dinleyicileri (Butonların çalışma mantığı)
        analyzeButton.addEventListener('click', () => processSingleCvAction('cv_analyze'));
        suggestButton.addEventListener('click', () => processSingleCvAction('cv_suggest'));
        compareButton.addEventListener('click', () => processCvComparison());

        // Tek CV analizi/önerisi için fonksiyon
        async function processSingleCvAction(actionType) {
            if (!singleCvFileInput.files || singleCvFileInput.files.length === 0) {
                showAlert('Lütfen tekli analiz için bir CV dosyası seçin.');
                return;
            }
            loadingSpinner.style.display = 'block';
            resultBox.innerHTML = 'CV metni okunuyor...';
            const formData = new FormData();
            formData.append('cv_file', singleCvFileInput.files[0]);
            try {
                const uploadResponse = await fetch('/upload_cv', { method: 'POST', body: formData });
                const uploadData = await uploadResponse.json();
                if (!uploadResponse.ok) {
                    showAlert(uploadData.error || 'CV yüklenirken bir hata oluştu.');
                    loadingSpinner.style.display = 'none';
                    return;
                }
                const extractedCvText = uploadData.extracted_text;
                resultBox.innerHTML = 'CV metni okundu. Yapay zeka ile iletişime geçiliyor...';
                const aiPayload = {
                    text: extractedCvText,
                    action_type: actionType,
                    company: companyInput.value,
                    position: positionInput.value
                };
                const aiResponse = await fetch('/get_ai_response', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(aiPayload),
                });
                const aiData = await aiResponse.json();
                if (aiResponse.ok) {
                    resultBox.innerHTML = aiData.response.replace(/\n/g, '<br>').replace(/\*/g, '<b>&bull;</b>');
                } else { showAlert(aiData.error || 'Yapay zeka analizi sırasında bir hata oluştu.'); }
            } catch (error) { showAlert('Sunucuyla iletişim kurulamadı.'); }
            finally { loadingSpinner.style.display = 'none'; }
        }

        // İki CV karşılaştırma fonksiyonu
        async function processCvComparison() {
            if (!cvFileInput1.files || cvFileInput1.files.length === 0 || !cvFileInput2.files || cvFileInput2.files.length === 0) {
                showAlert('Lütfen karşılaştırma için iki CV dosyasını da seçin.');
                return;
            }
            loadingSpinner.style.display = 'block';
            resultBox.innerHTML = 'CV\'ler sunucuya yükleniyor ve metinler okunuyor...';

            const formData = new FormData();
            formData.append('cv_file_1', cvFileInput1.files[0]);
            formData.append('cv_file_2', cvFileInput2.files[0]);
            formData.append('target_company', companyInput.value);
            formData.append('target_position', positionInput.value);

            try {
                const response = await fetch('/compare_cvs', {
                    method: 'POST',
                    body: formData,
                });
                const data = await response.json();
                if (response.ok) {
                    resultBox.innerHTML = data.response.replace(/\n/g, '<br>').replace(/\*/g, '<b>&bull;</b>');
                } else { showAlert(data.error || 'Karşılaştırma sırasında bir hata oluştu.'); }
            } catch (error) { showAlert('Sunucuyla iletişim kurulamadı.'); }
            finally { loadingSpinner.style.display = 'none'; }
        }
    }

    // --- Genel Öneriler Sayfası Kodu ---
    const holisticBtn = document.getElementById('btn-holistic-analysis');
    if (holisticBtn) {
        // ... (Bu bölüm öncekiyle aynı, değişiklik yok) ...
        const holisticResultArea = document.getElementById('holistic-result-area');
        const holisticSpinner = document.getElementById('holistic-loading-spinner');
        holisticBtn.addEventListener('click', async function() {
            holisticSpinner.style.display = 'block';
            holisticResultArea.style.display = 'none';
            holisticResultArea.innerHTML = '';
            try {
                const response = await fetch('/get_holistic_analysis', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                });
                const data = await response.json();
                if (response.ok) {
                    holisticResultArea.style.display = 'block';
                    holisticResultArea.innerHTML = data.response.replace(/\n/g, '<br>').replace(/\*\*/g, '').replace(/\*/g, '<b>&bull;</b>');
                } else { showAlert(data.error || 'Bilinmeyen bir hata oluştu.'); }
            } catch (error) { showAlert('Sunucuyla iletişim kurulamadı.'); }
            finally { holisticSpinner.style.display = 'none'; }
        });
    }
});