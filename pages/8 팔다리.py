import streamlit as st
from openai import OpenAI

# 사이드바에서 API 키 입력 받기
st.sidebar.title("API 설정")
api_key = st.sidebar.text_input("OpenAI API 키를 입력하세요", type="password")

# API 키가 입력되었는지 확인
if api_key:
    # OpenAI 클라이언트 초기화
    client = OpenAI(api_key=api_key)

    # Streamlit 페이지 제목 설정
    st.title("DALL-E 3 이미지 생성기")

    # 사용자 입력 받기
    prompt = st.text_input("귀여운 이미지 생성 프론트를 입력하세요", "a white siamese cat")

    # 물건에 팔다리를 추가하는 옵션 체크박스
    add_limbs = st.checkbox("물건에 팔다리를 추가하기")

    # 버튼을 클릭했을 때 이미지 생성
    if st.button("이미지 생성"):
        # 프롬프트에 팔다리 추가 옵션 반영
        if add_limbs:
            prompt += ", with limbs"

        # OpenAI API를 사용하여 이미지 생성
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )

        # 생성된 이미지 URL 가져오기
        image_url = response.data[0].url

        # 이미지 출력
        st.image(image_url, caption=f"Generated Image: {prompt}")
else:
    st.warning("API 키를 사이드바에 입력하세요.")