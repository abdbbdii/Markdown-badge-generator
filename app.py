import streamlit as st
from simpleicons.all import icons


class Link:
    BASE_URL = "https://img.shields.io/badge/"

    def __init__(self, label, color, message=None) -> None:
        self.label = label.strip().replace(" ", "_").replace('-','--')
        self.message = message.strip().replace(" ", "_").replace('-','--')
        self.color = color
        self.parameters = {}

    def config(self, key, value):
        self.parameters[key] = value
    
    def get(self, string):
        value = self.parameters.get(string, None)
        if value is not None:
            return value
        elif string == "label":
            return self.label
        elif string == "message":
            return self.message
        elif string == "color":
            return self.color

    def __str__(self):
        link_parts = [self.BASE_URL, f"{self.label}-{self.message}-{self.color}" if self.message else f"{self.label}-{self.color}"]
        if self.parameters:
            link_parts.append("?")
            link_parts.extend([f"{key}={value}&" for key, value in self.parameters.items() if value is not None])
        return "".join(link_parts).rstrip("&")
st.markdown('''# Badge Generator
This web app creates personalized badges for your upcoming project by generating HTML and Markdown code. It utilizes the shields.io API for crafting these badges.
To know how the API works, go to [Github](https://github.com/abdbbdii/markdown-badge-generator).
To know how exactly it generates them, go to [shields.io](https://img.shields.io/badge/).''')
with st.container(border=True):
    st.markdown("### Add elements")
    label = st.text_input("Label", placeholder="Label", value="Label")
    if not label:
        st.error("Label cannot be empty.")
    message = st.text_input("Message", placeholder="Message")
    color = st.color_picker("Choose text background color", value="#ffffff")[1:]
        
    link = Link(label=label,message=message, color=color)

    link.config("style", st.selectbox("Style", ("flat", "flat-square", "plastic", "for-the-badge", "social")))

with st.container(border=True):
    st.markdown("### Customize badge")
    if st.checkbox("Include a logo?"):
        logo = st.selectbox("Logo", icons)
        link.config('logo', logo)
        logoColor = st.color_picker("Choose logo color", value="#000000" if link.get("logoColor") is None else "#"+link.get("logoColor"))[1:]
        if st.button("Same as text"):
            logoColor = link.get("color")
        if st.button("Logo color"):
            icon = icons.get(link.get("logo"))
            logoColor = icon.__dict__["hex"]
        link.config('logoColor', logoColor)
    else:
        logo = st.text_input("Logo", disabled=True)
        logoColor = st.color_picker("Choose logo color", disabled=True)
        st.button("Same as text", disabled=True)
        st.button("Logo color", disabled=True)
    md=f"![{link.get('label')}]({link})"
    if (link.get("label")):
        st.markdown(md)
        st.code(md, "None")
