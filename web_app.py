import streamlit as st
#import app
import numpy as np
st.title('Детекция секретов в коде')
st.markdown('Проверьте свой репозиторий или файл из репозитория на наличие  **секретов**.')
st.markdown('Вставьте сюда :point_down: _ссылку_ на репозиторий или файл')
url = st.text_input('dd', '', placeholder='URL', label_visibility="hidden")

if st.button('Найти все секреты'):
    with st.spinner('Ждём жоского грязного белья...'):
        try:
            output = app.test1() #url внутри
            st.markdown('Мы тут несколько **секретов** у Вас нашли:')
            st.write(output)
            st.success('Дело сделано', icon='✅')
        except Exception:
            st.error('Неверный URL а репозиторий', icon="🚨")
