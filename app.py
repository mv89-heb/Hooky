import streamlit as st
import google.generativeai as genai

# הגדרות תצוגת הדף
st.set_page_config(page_title="מכונת הפוסטים", page_icon="🚀", layout="centered")

st.title("מכונת הפוסטים הויראליים 🚀")
st.write("הופכים כל טקסט ארוך ל-5 פוסטים שמושכים לקוחות ברשתות החברתיות.")
st.markdown("---")

# 1. ניהול הזיכרון של האפליקציה (כאן תיקנתי את הבאג)
if 'credits' not in st.session_state:
    st.session_state['credits'] = 1 
if 'generated_posts' not in st.session_state:
    st.session_state['generated_posts'] = "" # כאן נשמור את התוצאה כדי שלא תיעלם

st.sidebar.title("החשבון שלך")
st.sidebar.write(f"קרדיטים נותרים: **{st.session_state['credits']}**")

if st.session_state['credits'] <= 0:
    st.sidebar.warning("נגמרו לך הקרדיטים!")
    stripe_link = "https://buy.stripe.com/test_link_example" 
    st.sidebar.markdown(f"[**לרכישת מנוי חודשי ללא הגבלה לחץ כאן**]({stripe_link})")

# 2. ממשק המשתמש
api_key = st.sidebar.text_input("הכנס מפתח API של Gemini (למפתחים):", type="password")
article_text = st.text_area("הדבק כאן את המאמר או הטקסט שלך:", height=200, placeholder="הטקסט הולך כאן...")

# 3. יצירת הפוסטים
if st.button("ייצר לי פוסטים", type="primary"):
    if st.session_state['credits'] <= 0:
        st.error("עליך לשדרג את החשבון כדי להמשיך לייצר פוסטים.")
    elif not api_key:
        st.error("אנא הכנס מפתח API בסרגל הצד.")
    elif not article_text:
        st.error("אנא הדבק טקסט כלשהו כדי שנתחיל.")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-pro') 
            
            prompt = f"""
            אתה קופירייטר מומחה לשיווק ויראלי. נתח את הטקסט הבא:
            {article_text}
            
            המשימה:
            צור 5 פוסטים ויראליים.
            - פוסט 1: סיפורי.
            - פוסט 2: מדריך פרקטי.
            - פוסט 3: דעה מעוררת מחלוקת/שונה מהמקובל.
            - פוסט 4: רשימת תועלות.
            - פוסט 5: טיזר קצר לסקרנות.
            
            הקפד על:
            1. שורת פתיחה שעוצרת גלילה.
            2. משפטים קצרים ומרווחים.
            3. אימוג'ים ו-3 האשטאגים.
            4. הנעה ברורה לפעולה בסוף.
            """
            
            with st.spinner('מנתח את הטקסט ומייצר קסמים...'):
                response = model.generate_content(prompt)
                
                # שומרים את התוצאה בזיכרון לפני שמרעננים את הדף!
                st.session_state['generated_posts'] = response.text
                st.session_state['credits'] -= 1
                st.rerun() 
                
        except Exception as e:
            st.error(f"התרחשה שגיאה בחיבור ל-API: {e}")

# 4. הצגת התוצאה (נשארת על המסך גם אחרי הרענון)
if st.session_state['generated_posts']:
    st.success("הפוסטים שלך מוכנים! העתק אותם מכאן:")
    st.write(st.session_state['generated_posts'])