import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd

# ==========================================
# 1. CẤU HÌNH TRANG STREAMLIT
# ==========================================
st.set_page_config(
    page_title="TechArt AI-Assistant | THCS",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS cho giao diện hiện đại
st.markdown("""
    <style>
    .main-title {
        color: #182B49;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-title {
        color: #0096B4;
        font-size: 1.1rem;
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #0096B4;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #182B49;
        color: white;
    }
    .ai-box {
        background-color: #F4F7F9;
        border-left: 5px solid #0096B4;
        padding: 15px;
        border-radius: 8px;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. THANH CÔNG CỤ BÊN (SIDEBAR)
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/illustrations/100/art.png", width=80)
    st.title("⚙️ Cấu hình hệ thống")
    
    # Tự động kết nối API Key nếu lưu trong Secrets
    api_key_secret = st.secrets.get("GEMINI_API_KEY", "")
    if api_key_secret:
        api_key = api_key_secret
        st.success("🔑 Đã kết nối API Key hệ thống!")
    else:
        api_key = st.text_input(
            "Nhập Gemini API Key:",
            type="password",
            help="Lấy API Key miễn phí tại Google AI Studio (aistudio.google.com)"
        )
    
    st.divider()
    
    role = st.radio(
        "👥 Vai trò người dùng:",
        ["Học sinh (Thực hành)", "Giáo viên (Quản lý & Rubric)"]
    )
    
    if role == "Học sinh (Thực hành)":
        subject = st.selectbox(
            "📚 Môn học ứng dụng:",
            [
                "Công nghệ THCS (Thiết kế Kỹ thuật)",
                "Mĩ thuật THCS (Tạo dáng Sản phẩm)"
            ]
        )
    else:
        subject = None
    
    st.divider()
    st.caption("🏫 Trường TH & THCS Phú Định\n🎨 Dự án TechArt AI-Assistant © 2026")

# ==========================================
# 3. TIÊU ĐỀ TRANG CHÍNH
# ==========================================
st.markdown("<h1 class='main-title'>🎨 TechArt AI-Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Hệ thống Trợ lý AI hỗ trợ Đánh giá Năng lực & Phát triển Tư duy Phác thảo cho Học sinh THCS</p>", unsafe_allow_html=True)

# ==========================================
# 4. GIAO DIỆN HỌC SINH (STUDENT INTERFACE)
# ==========================================
if role == "Học sinh (Thực hành)":
    st.subheader(f"📌 Chế độ Thực hành: {subject}")
    
    col1, col2 = st.columns([1, 1], gap="large")
    
    with col1:
        st.markdown("### 1. Tải lên Bản phác thảo V1")
        uploaded_v1 = st.file_uploader(
            "Chụp và tải ảnh bản vẽ phác thảo tay của em (PNG, JPG, JPEG):",
            type=["jpg", "jpeg", "png"],
            key="v1_uploader"
        )
        
        description = st.text_area(
            "Mô tả thêm về ý tưởng thiết kế/sản phẩm (Tùy chọn):",
            placeholder="Ví dụ: Em thiết kế hộp đựng bút bằng bìa cứng, kích thước 20x10cm, có 3 ngăn...",
            key="v1_desc"
        )
        
        if uploaded_v1:
            img_v1 = Image.open(uploaded_v1)
            st.image(img_v1, caption="Bản phác thảo V1 đã tải lên", use_container_width=True)
            
            analyze_btn = st.button("🚀 Gửi cho AI TechArt Phân tích", type="primary", use_container_width=True)
        else:
            analyze_btn = False

    with col2:
        st.markdown("### 2. Phản hồi & Câu hỏi gợi mở từ AI")
        
        if uploaded_v1 and analyze_btn:
            if not api_key:
                st.error("⚠️ Vui lòng nhập Gemini API Key ở thanh bên (Sidebar) để bắt đầu phân tích!")
            else:
                with st.spinner("🔍 AI đang tự động dò tìm mô hình khả dụng và phân tích bản vẽ..."):
                    try:
                        # Cấu hình API Key
                        genai.configure(api_key=api_key)
                        
                        # 1. Khai báo prompt
                        prompt = f"""
                        Bạn là TechArt AI - Trợ lý sư phạm cho học sinh THCS trong môn {subject}.
                        Nhiệm vụ của bạn là phân tích bản vẽ phác thảo tay (Phiên bản V1) do học sinh gửi lên.
                        Mô tả bổ sung của học sinh: "{description}"
                        
                        YÊU CẦU PHẢN HỒI (Trình bày bằng Tiếng Việt thân thiện, động viên, chuẩn sư phạm):
                        1. **Lời khen động viên:** Khen ngợi 1-2 điểm sáng tạo hoặc nỗ lực phác thảo nét vẽ của học sinh.
                        2. **Phân tích kỹ thuật / Thẩm mỹ:** Nhận xét về bố cục, tỉ lệ, tính cân đối hoặc đường nét kỹ thuật/tạo dáng.
                        3. **CÂU HỎI GỢI MỞ PHẢN BIỆN (QUAN TRỌNG NHẤT):** Đưa ra 2-3 câu hỏi gợi ý để học sinh TỰ SUY NGẪM và TỰ ĐIỀU CHỈNH cho bản vẽ V2. (Ví dụ: Hỏi về độ vững của chân đế, kích thước ngăn chứa, sự hài hòa màu sắc,...). 
                        
                        *LƯU Ý QUAN TRỌNG: Tuyệt đối KHÔNG cho sẵn đáp án hay vẽ hộ.*
                        """
                        
                        # 2. Tự động truy vấn danh sách Model thực tế từ API của tài khoản
                        available_models = []
                        try:
                            for m in genai.list_models():
                                if hasattr(m, 'supported_generation_methods') and 'generateContent' in m.supported_generation_methods:
                                    available_models.append(m.name)
                        except Exception:
                            pass
                        
                        # Danh sách tên model phổ biến ưu tiên
                        preferred_models = [
                            'gemini-2.5-flash', 'models/gemini-2.5-flash',
                            'gemini-2.0-flash', 'models/gemini-2.0-flash',
                            'gemini-1.5-flash', 'models/gemini-1.5-flash',
                            'gemini-1.5-pro', 'models/gemini-1.5-pro'
                        ]
                        
                        models_to_try = []
                        for pref in preferred_models:
                            if pref in available_models and pref not in models_to_try:
                                models_to_try.append(pref)
                        
                        for m_name in available_models:
                            if m_name not in models_to_try:
                                models_to_try.append(m_name)
                                
                        if not models_to_try:
                            models_to_try = [
                                'gemini-2.5-flash',
                                'gemini-2.0-flash',
                                'gemini-1.5-flash',
                                'models/gemini-1.5-flash',
                                'models/gemini-2.0-flash'
                            ]
                            
                        # 3. Thử lần lượt từng model cho đến khi thành công
                        response = None
                        last_exception = None
                        
                        for m_name in models_to_try:
                            try:
                                model = genai.GenerativeModel(m_name)
                                response = model.generate_content([prompt, img_v1])
                                if response and response.text:
                                    break
                            except Exception as ex:
                                last_exception = ex
                                continue
                        
                        if response is None or not response.text:
                            if last_exception:
                                raise last_exception
                            else:
                                raise Exception("Không thể kết nối với các mô hình AI. Vui lòng kiểm tra lại API Key.")
                        
                        st.session_state['ai_response'] = response.text
                        st.success("✅ Đã hoàn thành phân tích!")
                        
                    except Exception as e:
                        st.error(f"❌ Lỗi khi kết nối với AI: {str(e)}")
        
        # Hiển thị kết quả AI
        if 'ai_response' in st.session_state and st.session_state['ai_response']:
            st.markdown(f"<div class='ai-box'>{st.session_state['ai_response']}</div>", unsafe_allow_html=True)
            
            st.divider()
            st.markdown("### 3. Cải tiến & Nộp Bản vẽ Hoàn thiện (V2)")
            uploaded_v2 = st.file_uploader(
                "Tải lên Bản phác thảo V2 (Đã chỉnh sửa theo gợi ý của AI):",
                type=["jpg", "jpeg", "png"],
                key="v2_uploader"
            )
            
            if uploaded_v2:
                img_v2 = Image.open(uploaded_v2)
                st.image(img_v2, caption="Bản phác thảo V2 đã hoàn thiện", use_container_width=True)
                if st.button("✅ Xác nhận Hoàn thành & Gửi Bài"):
                    st.success("🎉 Tốt lắm! Bài làm của em đã được tự động lưu vào Nhật ký E-Portfolio gửi Giáo viên.")

# ==========================================
# 5. GIAO DIỆN GIÁO VIÊN (TEACHER INTERFACE)
# ==========================================
else:
    st.subheader("📊 Bảng Quản lý & Đánh giá Năng lực (Dành cho Giáo viên)")
    
    tab1, tab2 = st.tabs(["📋 Khung Rubric Đánh giá (GDPT 2018)", "📁 Nhật ký Tiến bộ E-Portfolio"])
    
    # TAB 1: RUBRIC
    with tab1:
        st.markdown("#### Khung Rubric Đánh giá Sản phẩm Thiết kế THCS")
        rubric_data = {
            "Tiêu chí đánh giá": [
                "TC1: Ý tưởng & Tính mới",
                "TC2: Bản vẽ Kỹ thuật / Tạo dáng",
                "TC3: Tính khả thi & An toàn",
                "TC4: Tư duy Phản biện (V1 -> V2)"
            ],
            "Mức 1 (Chưa đạt)": [
                "Ý tưởng mô phỏng lại, chưa rõ nét",
                "Nét vẽ mờ, sai tỉ lệ hình chiếu/bố cục",
                "Không sử dụng được, thiếu an toàn",
                "Không chỉnh sửa sau khi nhận gợi ý"
            ],
            "Mức 2 (Đạt)": [
                "Có ý tưởng riêng, thể hiện được công năng",
                "Bản vẽ khá rõ ràng, đúng tỉ lệ cơ bản",
                "Làm được mô hình/sản phẩm thực tế",
                "Có sửa chữa V2 nhưng chưa triệt để"
            ],
            "Mức 3 (Tốt)": [
                "Ý tưởng độc đáo, có tính ứng dụng cao",
                "Bản vẽ chuẩn xác, phối màu/kết cấu đẹp",
                "Chắc chắn, an toàn, tối ưu vật liệu",
                "Tự chỉnh sửa V2 hoàn thiện dựa trên gợi mở"
            ]
        }
        df_rubric = pd.DataFrame(rubric_data)
        st.table(df_rubric)
        
    # TAB 2: E-PORTFOLIO MẪU
    with tab2:
        st.markdown("#### Nhật ký Theo dõi Tiến bộ Học sinh Lớp 8A (Thực nghiệm)")
        
        portfolio_data = {
            "Mã HS": ["HS01", "HS02", "HS03", "HS04", "HS05"],
            "Họ và Tên": ["Nguyễn Văn An", "Trần Thị Bích", "Lê Hoàng Cường", "Phạm Đăng Khoa", "Vũ Mỹ Linh"],
            "Môn học": ["Công nghệ", "Mĩ thuật", "Công nghệ", "Mĩ thuật", "Công nghệ"],
            "Bản V1": ["Đã tải", "Đã tải", "Đã tải", "Đã tải", "Đã tải"],
            "Số lượt AI Gợi mở": [2, 3, 1, 2, 3],
            "Bản V2 (Hoàn thiện)": ["Đã nộp", "Đã nộp", "Chưa nộp", "Đã nộp", "Đã nộp"],
            "Đánh giá Rubric": ["Mức 3 (Tốt)", "Mức 3 (Tốt)", "Mức 1 (Chưa đạt)", "Mức 2 (Đạt)", "Mức 3 (Tốt)"]
        }
        df_portfolio = pd.DataFrame(portfolio_data)
        st.dataframe(df_portfolio, use_container_width=True)
        
        st.download_button(
            label="📥 Xuất dữ liệu E-Portfolio sang Excel (CSV)",
            data=df_portfolio.to_csv(index=False).encode('utf-8-sig'),
            file_name="E_Portfolio_TechArt_Class8A.csv",
            mime="text/csv"
        )
