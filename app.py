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
            
To know how exactly it generates them, go to [Github](https://github.com/abdbbdii/markdown-badge-generator).
            
To know how the API works, go to [shields.io](https://shields.io/).''')
with st.container(border=True):
    st.markdown("### Add elements")

    label = st.text_input("Label", placeholder="Label", value="Label")
    if not label:
        st.error("Label cannot be empty.")
    message = st.text_input("Message", placeholder="Message")
    link = Link(label=label,message=message, color="ffffff")

    logoInc=st.checkbox("Include a logo?")
    if logoInc:
        logo = st.selectbox("Logo", icons)
        link.config('logo', logo)
    else:
        logo = st.selectbox("Logo", icons, disabled=True)


with st.container(border=True):
    st.markdown("### Customize badge")
    if logoInc:
        icon = icons.get(link.get("logo"))
        color = st.color_picker("Badge Color", value="#"+icon.__dict__["hex"])[1:]
        logoColor = st.color_picker("Logo Color", value="#ffffff")[1:]
        if st.button("Logo color"):
            icon = icons.get(link.get("logo"))
            logoColor = icon.__dict__["hex"]
        link.config('logoColor', logoColor)
    else:
        color = st.color_picker("Badge Color", value="#ffffff")[1:]
        logoColor = st.color_picker("Logo Color", disabled=True)
        st.button("Logo color", disabled=True)
    link.config('color', color)
    
    
    link.config("style", st.selectbox("Style", ("flat", "flat-square", "plastic", "for-the-badge", "social")))
    md=f"![{link.get('label')}]({link})"
    if (link.get("label")):
        st.markdown(md)
        st.code(md, "None")


st.write("Made with ❤️ by abd")
