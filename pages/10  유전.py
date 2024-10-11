import streamlit as st
from openai import OpenAI
import requests
from io import BytesIO
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# 가이드를 사이드바에서 입력 받기
st.sidebar.title("API 설정")
api_key = st.sidebar.text_input("OpenAI API 키를 입력하세요", type="password")

# Streamlit 페이지 제목 설정
st.title("가상의 부모 만들기")
st.header("사용자 자기소개")

# 사용자 입력 받기
name = st.text_input("이름을 이니셜로 입력하세요. 예) J.Y.S.")
gender = st.radio("성별:", ('남자', '여자'))

# 유전자 관련 형질 입력 받기
eye_type = st.radio("눈 형질 (우성/열성):", ('쌍꺼풀', '외꺼풀'))
earlobe_type = st.radio("귀 형질 (우성/열성):", ('분리형', '부착형'))
forehead_type = st.radio("이마선 형질 (우성/열성):", ('V자형', 'M자형'))
hair_type = st.radio("머리카락 형질 (우성/열성):", ('곱슬형', '직모형'))
dimples = st.radio("보조개:", ('있다', '없다'))

generate_button = st.button("가상의 부모 생성")

# API 키가 입력되었는지 확인
if api_key:
    # OpenAI 클라이언트 초기화
    client = OpenAI(api_key=api_key)

    if generate_button and all([name, gender, eye_type, earlobe_type, forehead_type, hair_type, dimples]):
        # 이미지 생성 프롬프트
        prompt = f"성인의 현실적인 얼굴 사진으로, 성별: {gender}, 눈 형질: {eye_type}, 귀 형질: {earlobe_type}, 이마선: {forehead_type}, 머리카락 형질: {hair_type}, 보조개: {dimples}을 포함한 증명사진 디자인. 카드 하단에 '{name}'이라는 이름이 크게 표시됩니다."

        with st.spinner("가상의 부모를 생성중입니다. 잠시만 기다려주세요..."):
            try:
                # OpenAI API를 사용하여 이미지 생성
                response = client.images.generate(
                    model="dall-e-3",
                    prompt=prompt,
                    size="1024x1792",
                    quality="standard",
                    n=1,
                )

                # 생성된 이미지 URL 가져오기
                image_url = response.data[0].url

                # 이미지 출력
                st.image(image_url, caption=f"{name}의 가상의 부모")

                # 쌍꺼풀 여부 확인 체크박스
                double_eyelid_check = st.checkbox("생성된 이미지에서 쌍꺼풀이 잘 표현되었나요?")

                if double_eyelid_check:
                    st.success("쌍꺼풀이 잘 표현되었습니다!")
                else:
                    st.info("쌍꺼풀이 잘 표현되지 않았습니다. 다시 시도해보세요.")

                # 만족도 평가 및 이유 입력
                satisfaction_score = st.slider("생성된 이미지에 대한 만족도를 평가해주세요 (0-5점):", 0, 5, 3)
                feedback_reason = st.text_area("만족도에 대한 이유를 입력해주세요:")

                # 이메일로 이유 전송 버튼
                if st.button("이유 이메일로 보내기"):
                    try:
                        # 이메일 설정
                        sender_email = "your_email@example.com"  # 발신자 이메일 주소 입력
                        receiver_email = "dunghu@hanmail.net"
                        password = "your_email_password"  # 발신자 이메일 비밀번호 입력

                        # 이메일 내용 구성
                        msg = MIMEMultipart()
                        msg['From'] = sender_email
                        msg['To'] = receiver_email
                        msg['Subject'] = f"{name}의 타로 카드 이미지 평가 결과"

                        body = f"만족도 점수: {satisfaction_score}\n이유: {feedback_reason}"
                        msg.attach(MIMEText(body, 'plain'))

                        # SMTP 서버 설정 및 이메일 전송
                        server = smtplib.SMTP('smtp.example.com', 587)  # SMTP 서버와 포트 설정
                        server.starttls()
                        server.login(sender_email, password)
                        server.sendmail(sender_email, receiver_email, msg.as_string())
                        server.quit()

                        st.success("이유가 이메일로 성공적으로 전송되었습니다!")
                    except Exception as e:
                        st.error("이메일 전송 중 오류가 발생했습니다: " + str(e))

                # 이미지 다운로드 준비
                response = requests.get(image_url)
                image_bytes = BytesIO(response.content)

                # 이미지 다운로드 버튼
                st.download_button(label="이미지 다운로드",
                                   data=image_bytes,
                                   file_name=f"{name}_tarot_card.jpg",
                                   mime="image/jpeg")
            except Exception as e:
                st.error("현재 사용 중인 키로 오류가 발생했습니다. 안전 시스템에 의해 요청이 거부되었을 수 있습니다. 요청 내용을 수정하여 다시 시도해주세요.")
    else:
        st.warning("모든 필드를 채워주세요!")
else:
    st.error("API 키가 입력되지 않았습니다. API 키를 입력한 후 다시 시도하세요.")
