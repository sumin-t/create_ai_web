import streamlit as st
import google.generativeai as genai

# 사이드바에서 API 키 입력 받기
st.sidebar.title("API 설정")
api_key = st.sidebar.text_input("Google Gemini API 키를 입력하세요", type="password")

# API 키가 입력되었는지 확인
if api_key:
    # API 키 설정
    genai.configure(api_key=api_key)

    # Streamlit 페이지 제목 설정
    st.title("원영적사고 생성기")

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

    # 사용자 입력 받기
    user_input = st.text_area("당신의 슬픈기분을 입력해 보세요.", 
                              "예: 나는 체육대회에서 우승하기 위해 방과후에도 남아서 연습했으나 꼴지를 하였어요.")

    if st.button("원영적사고 생성"):
        # 인공지능 모델을 사용하여 상장 생성
        response = model.generate_content([
            "중고등학생에게 부정적인 사고를 긍정적인 사고로 바꾸어주는 역할을 합니다. 예를 들어 출력물은 갑자기 비가 와서 추워. 그렇지만 운치있는 빗소리를 들을 수 있다니 완전 럭키비키잖아. 이모티콘을 꼭 첨부해주고 럭키비잖아로 끝나게 해주세요.",
            f"input: {user_input}",
        ])

        # 결과 출력
        st.subheader("원영적사고 생성")
        st.write(response.text)
else:
    st.warning("API 키를 사이드바에 입력하세요.")
