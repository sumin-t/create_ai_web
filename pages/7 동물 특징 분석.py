import streamlit as st
import google.generativeai as genai
import tempfile

# 사이드바에서 API 키 입력 받기
st.sidebar.title("API 설정")
api_key = st.sidebar.text_input("Google Gemini API 키를 입력하세요", type="password")

# API 키가 입력되었는지 확인
if api_key:
    # API 키 설정
    genai.configure(api_key=api_key)

    # Streamlit 페이지 제목 설정
    st.title("인공지능 이미지 분석기")

    # 생성 설정
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    # 모델 초기화
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )

    # 이미지 업로드 기능 추가
    uploaded_file = st.file_uploader("이미지를 업로드하세요", type=["jpg", "jpeg", "png"])

    def upload_to_gemini(file_data, mime_type=None):
        """Uploads the given file to Gemini and returns the file object."""
        # 임시 파일로 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            temp_file.write(file_data)
            temp_file_path = temp_file.name
        
        # 업로드
        file = genai.upload_file(temp_file_path, mime_type=mime_type)
        
        return file

    if uploaded_file is not None:
        # 파일 데이터를 임시 파일로 저장하고 업로드 및 분석
        uploaded_gemini_file = upload_to_gemini(uploaded_file.getvalue(), mime_type=uploaded_file.type)

        # 대화 세션 시작 및 메시지 전송
        chat_session = model.start_chat(
            history=[
                {
                    "role": "user",
                    "parts": [
                        uploaded_gemini_file,
                        "이 동물의 특징을 분석해 주세요. 동물의 특징 3가지를 분석하여 설명하고, 서식지를 2가지 이상 설명해주세요. 미래의 변화한 생태계에서 이 사진 속 동물이 어떤 모습으로 진화될지 진화된 모습의 특징 2가지 설명해주세요.",
                    ],
                },
            ]
        )

        # 결과 출력
        response = chat_session.send_message("이미지 분석 결과를 알려주세요.")
        st.subheader("이미지 분석 결과")
        st.write(response.text)
else:
    st.warning("API 키를 사이드바에 입력하세요.")
