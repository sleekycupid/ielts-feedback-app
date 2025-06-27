import streamlit as st
import language_tool_python

# Function to detect generalizations
def detect_generalizations(essay):
    generalizations = []
    words_to_check = ["all", "always", "everyone", "never", "nobody", "everybody", "everything", "nothing"]
    for word in words_to_check:
        if word in essay.lower():
            generalizations.append(f"⚠️ Try to avoid using absolute term: '{word}'")
    return generalizations

# Streamlit UI
st.title("IELTS Essay Feedback App ✍️")
essay = st.text_area("📄 Paste your IELTS essay below:")

if essay:
    st.subheader("🧠 Feedback:")

    # Generalization warnings
    generalization_flags = detect_generalizations(essay)
    if generalization_flags:
        st.write("🚨 **Generalization Warnings:**")
        for warning in generalization_flags:
            st.write(f"- {warning}")
    else:
        st.write("✅ No generalization issues found.")

    # Grammar checking
    try:
        tool = language_tool_python.LanguageTool('en-US')
        st.write("✅ LanguageTool is running")

        matches = tool.check(essay)

        if matches:
            st.write("🔍 **Detailed Grammar Feedback:**")
            for match in matches[:5]:  # Limit to first 5 issues
                start = match.offset
                end = start + match.errorLength
                error_part = essay[start:end]
                suggestion = match.replacements[0] if match.replacements else "No suggestion"

                st.markdown(f"""
                ---
                🔸 **Issue:** {match.message}  
                ❌ **Problem:** `{error_part}`  
                ✅ **Suggestion:** `{suggestion}`  
                📍 **Position:** character {start} to {end}
                """)
        else:
            st.write("✅ No grammar issues found.")
    except Exception as e:
        st.error(f"❌ Error with LanguageTool: {e}")


