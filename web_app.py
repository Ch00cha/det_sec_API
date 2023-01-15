import streamlit as st
from api_requests import request_to_det_sec_API

st.title('Детекция паролей в коде')
st.markdown('Проверьте свой репозиторий или файл из репозитория на наличие  **паролей**.')
st.markdown('Вставьте сюда :point_down: _ссылку_ на репозиторий или файл')
url = st.text_input('dd', '', placeholder='URL', label_visibility="hidden")

if st.button('Найти все пароли'):
    with st.spinner('Производится сканирование ваших секретиков...'):
            response = request_to_det_sec_API(url)
            st.markdown('**Результаты:**')
            if response == 'Неверный url, либо репозиторий является приватным':
                st.error('Неверный URL или репозиторий приватный', icon="🚨")
            elif response == 'Превышено количество запросов':
                st.error('Превышено количество запросов', icon="🚨")
            else:
                st.write(response)
                st.success('Дело сделано', icon="✅")
