import streamlit as st
from api_requests import request_to_det_sec_API

st.title('Детекция секретов в коде')
st.markdown('Проверьте свой репозиторий или файл из репозитория на наличие  **секретов**.')
st.markdown('Вставьте сюда :point_down: _ссылку_ на репозиторий или файл')
url = st.text_input('dd', '', placeholder='URL', label_visibility="hidden")

if st.button('Найти все секреты'):
    with st.spinner('Ждём жоского грязного белья...'):
        try:
            response = request_to_det_sec_API(url)
            st.markdown('Мы тут несколько **секретов** у Вас нашли:')
            st.write(response)
            st.success('Дело сделано', icon="✅")
        except KeyError:
            st.error('Неверный URL или репозиторий приватный', icon="🚨")
