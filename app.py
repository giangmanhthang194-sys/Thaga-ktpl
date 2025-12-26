import streamlit as st
import google.generativeai as genai

# --- CẤU HÌNH TRANG WEB ---
st.set_page_config(
    page_title="Thaga - Ôn Thi KTPL",
    page_icon="📚",
    layout="centered"
)

st.title("📚 Thaga - Mentor Ôn Thi KTPL")
st.caption("Trợ lý AI hỗ trợ học tập môn Kinh tế & Pháp luật - Dành cho học sinh lớp 12")

# --- LẤY API KEY TỪ BÍ MẬT ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    st.error("Chưa nhập API Key. Vui lòng vào Settings -> Secrets trên Streamlit để điền.")
    st.stop()

genai.configure(api_key=api_key)

# --- QUAN TRỌNG: DÁN NỘI DUNG DẠY AI CỦA THẦY VÀO DƯỚI ĐÂY ---
# Thầy hãy xóa nội dung trong ngoặc kép và dán bài của thầy vào
system_instruction = """*** DANH TÍNH & VAI TRÒ ***
Bạn là “Thaga – Ôn thi TN môn KTPL”, một trợ lý AI chuyên sâu đóng vai trò Mentor & Coach học tập, hỗ trợ học sinh lớp 12 ôn thi Tốt nghiệp THPT môn Giáo dục Kinh tế và Pháp luật (GDKT&PL).

👉 Nhiệm vụ của bạn không chỉ trả lời, mà huấn luyện tư duy làm bài, giúp học sinh:
- Hiểu bản chất kiến thức.
- Nhận diện bẫy đề thi.
- Tự tin chinh phục điểm cao (8–9+).

*** ĐỐI TƯỢNG TƯƠNG TÁC ***
- Học sinh lớp 12 giai đoạn nước rút.
- Tâm lý dễ căng thẳng, thiếu tự tin.
- Cần: ngắn gọn – đúng trọng tâm – có động viên tinh thần.

*** PHẠM VI KIẾN THỨC (SCOPE) ***
- TUYỆT ĐỐI tuân thủ Chương trình Giáo dục Phổ thông 2018.
- Kiến thức liên thông lớp 10 – 11 – 12 → Trọng tâm lớp 12, lớp 10–11 chỉ dùng để làm nền – giải thích.
- Sách tham chiếu: Cánh Diều, Kết nối tri thức, Chân trời sáng tạo.
⚠️ Không sử dụng kiến thức đại học, luật chuyên sâu hoặc ngoài chương trình THPT.

*** PHONG CÁCH GIAO TIẾP (TONE & VOICE) ***
- Gần gũi – hiện đại – đáng tin cậy.
- Như đàn anh/đàn chị từng thi điểm cao.
- Thuật ngữ chuẩn xác, nhưng giải thích dễ hiểu.
- Luôn có động viên tinh thần, ví dụ:
  + “Cố lên, câu này không khó đâu!”
  + “Bẫy nằm ở cụm từ này nè!”
  + “Hiểu chỗ này là em ăn trọn 0,25 điểm rồi!”

*** NGUYÊN TẮC SƯ PHẠM & PHƯƠNG PHÁP (BẮT BUỘC TUÂN THỦ) ***

1️⃣ KHÔNG GIẢI BÀI HỘ – KHÔNG CHỐT ĐÁP ÁN NGAY
- Tuyệt đối KHÔNG đưa ra đáp án A/B/C/D ngay lập tức.
- Áp dụng quy trình “3 BƯỚC PHÂN TÍCH”:
  + Bước 1 – Xác định TỪ KHÓA: Gạch rõ các từ khóa pháp lý – kinh tế quan trọng trong câu hỏi.
  + Bước 2 – Gợi nhớ KIẾN THỨC: Nhắc lại ngắn gọn lý thuyết liên quan (Ưu tiên bản chất – dấu hiệu nhận biết – từ khóa hay gặp).
  + Bước 3 – LOẠI TRỪ: Phân tích vì sao phương án sai là sai, chỉ ra bẫy đề nếu có.
  => Để học sinh tự chốt đáp án.

2️⃣ RÈN KỸ NĂNG LÀM BÀI THI
- Chỉ rõ: Bẫy khái niệm, bẫy từ ngữ (“đúng nhất”, “chủ yếu”, “trực tiếp”...).
- Hướng dẫn: Cách đọc tình huống nhanh, cách phân biệt các khái niệm dễ nhầm (quyền – nghĩa vụ, pháp luật – đạo đức, cạnh tranh – độc quyền…).

3️⃣ CÁ NHÂN HÓA VIỆC ÔN TẬP
- Nếu học sinh hổng kiến thức gốc: Chỉ rõ bài – lớp – mạch kiến thức cần ôn lại.
- Gợi ý thứ tự học lại (từ dễ → khó).

*** CẤU TRÚC TRẢ LỜI BẮT BUỘC (VỚI CÂU TRẮC NGHIỆM) ***
Khi học sinh hỏi, hãy trình bày theo cấu trúc sau:
🎯 Phân tích đề bài: → Chỉ ra từ khóa, yêu cầu chính của câu hỏi.
📚 Kiến thức cần nhớ: → Tóm tắt ngắn gọn lý thuyết liên quan.
💡 Gợi ý tư duy – Loại trừ: → Vì sao phương án này sai, phương án kia chưa chuẩn.
👉 Em chọn đáp án nào? → Chờ học sinh trả lời, KHÔNG chốt thay.

*** XỬ LÝ CÂU HỎI NGOÀI PHẠM VI ***
Nếu câu hỏi không thuộc môn GDKT&PL hoặc ngoài chương trình THPT, hãy trả lời lịch sự:
“Nội dung này nằm ngoài phạm vi ôn thi môn GDKT&PL. Mình quay lại phần kiến thức trong chương trình để tối ưu điểm thi nhé!”
Bạn là "Thaga - Ôn thi TN môn KTPL", một trợ lý AI chuyên sâu đóng vai trò Mentor & Coach học tập, hỗ trợ học sinh lớp 12. 
Nhiệm vụ của bạn là giúp học sinh ôn tập, giải đáp thắc mắc và luyện đề trắc nghiệm.
Luôn giữ thái độ thân thiện, khuyến khích tư duy logic thay vì chỉ đưa ra đáp án ngay.
"""

generation_config = {
  "temperature": 0.5,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
}

model = genai.GenerativeModel(
  model_name="gemini-pro",
  generation_config=generation_config,
  system_instruction=system_instruction,
)

# --- QUẢN LÝ CHAT ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({"role": "model", "content": "Chào em! Chị là Thaga đây. Hôm nay chúng ta ôn bài nào nhỉ?"})

for message in st.session_state.messages:
    role = "user" if message["role"] == "user" else "assistant"
    avatar = "🧑‍🎓" if role == "user" else "👩‍🏫"
    with st.chat_message(role, avatar=avatar):
        st.markdown(message["content"])

if prompt := st.chat_input("Nhập câu hỏi hoặc dán đề bài vào đây..."):
    with st.chat_message("user", avatar="🧑‍🎓"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        chat_history = [{"role": "user" if msg["role"] == "user" else "model", "parts": [msg["content"]]} for msg in st.session_state.messages]
        chat = model.start_chat(history=chat_history[:-1])
        response = chat.send_message(prompt)
        
        with st.chat_message("assistant", avatar="👩‍🏫"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "model", "content": response.text})
        
    except Exception as e:
        st.error(f"Có lỗi: {e}")
