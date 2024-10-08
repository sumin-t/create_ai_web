import streamlit as st
import openai

# 사이드바에서 API 키 입력 받기
st.sidebar.title("API 설정")
api_key = st.sidebar.text_input("OpenAI API 키를 입력하세요", type="password")

# API 키가 입력되었는지 확인
if api_key:
    # OpenAI API 키 설정
    openai.api_key = api_key

    # Streamlit 페이지 제목 설정
    st.title("DALL-E 3 이미지 생성기")

    # 사용자 입력 받기
    prompt = st.text_input("이미지 생성 프롬프트를 입력하세요", "a white siamese cat")

    # 미래 동물 모습 예측 옵션 추가
    future_animal = st.checkbox("미래 동물 모습 예측")

    # 버튼을 클릭했을 때 이미지 생성
    if st.button("이미지 생성"):
        try:
            # 미래 동물 모습 예측 체크 여부에 따라 프롬프트 수정
            if future_animal:
                prompt = "future version of " + prompt

            # OpenAI API를 사용하여 이미지 생성
            response = openai.Image.create(
                prompt=prompt,
                n=1,
                size="1024x1024"
            )

            # 생성된 이미지 URL 가져오기
            image_url = response['data'][0]['url']

            # 이미지 출력
            st.image(image_url, caption=f"Generated Image: {prompt}")
        except Exception as e:
            st.error(f"이미지 생성 중 오류가 발생했습니다: {e}")
else:
    st.warning("API 키를 사이드바에 입력하세요.")