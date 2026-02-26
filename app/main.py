import streamlit as st
from faker import Faker
import pandas as pd
import random
from datetime import datetime
import time

# Настройка страницы
st.set_page_config(
    page_title="QA Data Generator",
    page_icon="🎲",
    layout="wide"
)

st.title("🎲 QA Data Generator")
st.markdown("Инструмент для генерации тестовых данных (для QA-инженеров)")

# Инициализация session state для сохранения настроек
if 'count' not in st.session_state:
    st.session_state.count = 10
if 'language' not in st.session_state:
    st.session_state.language = "Русский"

# Настройки в боковой панели
with st.sidebar:
    st.header("⚙️ Настройки")
    
    count = st.slider("Количество записей", 1, 50, st.session_state.count)
    language = st.selectbox("Язык", ["Русский", "English"], 
                           index=0 if st.session_state.language == "Русский" else 1)
    
    st.markdown("---")
    st.header("📋 Выбери поля для генерации")
    
    # Создаём колонки для чекбоксов
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.checkbox("ФИО", value=True)
        email = st.checkbox("Email", value=True)
        phone = st.checkbox("Телефон", value=True)
        city = st.checkbox("Город", value=True)
        address = st.checkbox("Адрес", value=False)
        birth = st.checkbox("Дата рождения", value=False)
    
    with col2:
        job = st.checkbox("Профессия", value=False)
        company = st.checkbox("Компания", value=False)
        inn = st.checkbox("ИНН", value=False)
        passport = st.checkbox("Паспорт", value=False)
        card = st.checkbox("Банковская карта", value=False)
        ip = st.checkbox("IP адрес", value=False)
    
    st.markdown("---")
    
    # Кнопка случайных настроек
    if st.button("🎲 Случайные настройки"):
        st.session_state.count = random.randint(5, 50)
        st.session_state.language = random.choice(["Русский", "English"])
        st.rerun()
    
    # Кнопка генерации (теперь здесь)
    generate_btn = st.button("🚀 Сгенерировать данные", type="primary", use_container_width=True)

# Выбираем язык
if language == "Русский":
    fake = Faker('ru_RU')
else:
    fake = Faker('en_US')

# Основная логика генерации
if generate_btn:
    with st.spinner("Генерирую данные..."):
        
        # Прогресс-бар
        progress_bar = st.progress(0)
        
        # Создаем данные
        data = []
        for i in range(count):
            user = {}
            
            # Добавляем только выбранные поля
            user["ID"] = i + 1
            
            if name:
                user["ФИО"] = fake.name()
            if email:
                user["Email"] = fake.email()
            if phone:
                user["Телефон"] = fake.phone_number()
            if city:
                user["Город"] = fake.city()
            if address:
                user["Адрес"] = fake.address().replace('\n', ', ')
            if birth:
                user["Дата рождения"] = fake.date_of_birth(minimum_age=18, maximum_age=70).strftime("%d.%m.%Y")
            if job:
                user["Профессия"] = fake.job()
            if company:
                user["Компания"] = fake.company()
            if inn:
                # ИНН (10 цифр для юрлиц)
                user["ИНН"] = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            if passport:
                # Паспорт: серия и номер
                user["Паспорт"] = f"{random.randint(1000, 9999)} {random.randint(100000, 999999)}"
            if card:
                user["Номер карты"] = fake.credit_card_number()
                user["CVV"] = fake.credit_card_security_code()
            if ip:
                user["IP адрес"] = fake.ipv4()
            
            data.append(user)
            
            # Обновляем прогресс
            progress_bar.progress((i + 1) / count)
            time.sleep(0.01)  # небольшая задержка, чтобы прогресс был виден
        
        # Убираем прогресс-бар
        progress_bar.empty()
        
        # Показываем результаты
        st.success(f"✅ Сгенерировано {count} записей!")
        
        # Таблица с данными
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        
        # Кнопки скачивания
        col1, col2, col3 = st.columns(3)
        
        with col1:
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📥 Скачать CSV",
                csv,
                f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                "text/csv",
                use_container_width=True
            )
        
        with col2:
            st.download_button(
                "📥 Скачать JSON",
                df.to_json(orient='records', force_ascii=False).encode('utf-8'),
                f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                "application/json",
                use_container_width=True
            )
        
        with col3:
            # Статистика в отдельной кнопке
            with st.expander("📊 Статистика"):
                st.write(f"**Всего записей:** {len(df)}")
                st.write(f"**Всего полей:** {len(df.columns)}")
                st.write(f"**Поля:** {', '.join(df.columns)}")
                
                # Небольшая статистика по текстовым полям
                for col in df.columns:
                    if df[col].dtype == 'object':
                        unique_count = df[col].nunique()
                        st.write(f"**{col}:** {unique_count} уникальных значений")

else:
    # Информация до генерации
    st.info("👈 Выбери настройки в боковой панели и нажми кнопку генерации")
    
    # Показываем пример того, что будет
    with st.expander("👀 Предпросмотр (пример данных)"):
        st.write("**Будут сгенерированы следующие поля:**")
        selected_fields = []
        if name: selected_fields.append("ФИО")
        if email: selected_fields.append("Email")
        if phone: selected_fields.append("Телефон")
        if city: selected_fields.append("Город")
        if address: selected_fields.append("Адрес")
        if birth: selected_fields.append("Дата рождения")
        if job: selected_fields.append("Профессия")
        if company: selected_fields.append("Компания")
        if inn: selected_fields.append("ИНН")
        if passport: selected_fields.append("Паспорт")
        if card: selected_fields.append("Номер карты, CVV")
        if ip: selected_fields.append("IP адрес")
        
        if selected_fields:
            st.write("📋 " + ", ".join(selected_fields))
        else:
            st.warning("⚠️ Ни одно поле не выбрано! Выбери хотя бы одно поле в настройках.")
        
        st.write(f"**Количество записей:** {count}")
        st.write(f"**Язык:** {language}")

# Подвал
st.markdown("---")
st.markdown("🔗 [Проект на GitHub](https://github.com/твой-никнейм/qa-data-generator)")