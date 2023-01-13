import streamlit as st
import subprocess
import time
#import "... .py"
import pandas as pd
import numpy as np
st.title('Детекция секретов в коде')
st.markdown('Проверьте свой репозиторий на наличие  **секретов**.')
st.markdown('Вставьте сюда :point_down: _ссылку_ на репозиторий')
url = st.text_input('dd', '', placeholder='URL', label_visibility="hidden")
if st.button('Найти все секреты'):
    with st.spinner('Ждём жоского грязного белья...'):
            subprocess.call("D:/2nd proj/simple_streamlit_app/app.py", shell=True) #Для проверки работоспособности можно импортнуть сам .py файл и вызвать его
    st.success('Дело сделано', icon='✅')

    #добавить бокс для вывода после выполнения проги (наверное тоже по нажатию кнопки)