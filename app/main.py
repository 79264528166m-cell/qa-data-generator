import streamlit as st
from faker import Faker
import pandas as pd
import random
from datetime import datetime

st.title("🎲 Генератор тестовых данных")
st.markdown("Создавай данные для тестирования в один клик")

# Настройки в боковой панели
with st.sidebar:
    st.header("Настройки")
    count = st.slider("Количество записей", 1, 50, 10)
    language = st.selectbox("Язык", ["Русский", "English"])
    st.markdown("---")
    st.markdown("👆 Выбери параметры и нажми кнопку")

# Выбираем язык
if language == "Русский":
    fake = Faker('ru_RU')
else:
    fake = Faker('en_US')

# Кнопка генерации
if st.button("🚀 Сгенерировать данные", type="primary"):
    with st.spinner("Генерирую..."):
        # Создаем данные
        data = []
        for i in range(count):
            user = {
                "ID": i + 1,
                "ФИО": fake.name(),
                "Email": fake.email(),
                "Телефон": fake.phone_number(),
                "Город": fake.city(),
                "Адрес": fake.address().replace('\n', ', '),
                "Дата рождения": fake.date_of_birth(minimum_age=18, maximum_age=70).strftime("%d.%m.%Y"),
                "Профессия": fake.job(),
                "Компания": fake.company(),
            }
            data.append(user)
        
        # Показываем таблицу
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        
        # Кнопки скачивания
        col1, col2 = st.columns(2)
        with col1:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Скачать CSV",
                csv,
                f"users_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "text/csv"
            )
        with col2:
            st.download_button(
                "📥 Скачать JSON",
                df.to_json(orient='records', force_ascii=False).encode('utf-8'),
                f"users_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                "application/json"
            )
        
        st.success(f"✅ Сгенерировано {count} записей!")