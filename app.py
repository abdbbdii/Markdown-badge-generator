import streamlit as st
from simpleicons.all import icons


class Link:
    BASE_URL = "https://img.shields.io/badge/"

    def __init__(self, label, color, message=None) -> None:
        self.label = ((label.strip().replace("_", "__")).replace(" ", "%20")).replace("-", "--")
        self.message = ((message.strip().replace("_", "__")).replace(" ", "%20")).replace("-", "--")
        self.color = color
        self.parameters = {}

    def config(self, key, value):
        self.parameters[key] = value

    def get(self, string):
        return self.parameters.get(string, getattr(self, string, None))

    def __str__(self):
        link_parts = [self.BASE_URL, f"{self.label}-{self.message}-{self.color}" if self.message else f"{self.label}-{self.color}"]
        if self.parameters:
            link_parts.append("?")
            link_parts.extend([f"{key}={value}&" for key, value in self.parameters.items() if value is not None])
        return "".join(link_parts).rstrip("&")


st.set_page_config(
    "Markdown Badge Generator",
    "./markdown-badge-generator.ico",
    "centered",
    menu_items={
        "Get help": None,
        "About": "Streamline app to gennerate a markdowncode for customized badge",
        "Report a bug": None,
    },
)
st.header("Badge Generator", divider="red")
st.markdown(
    """This web app creates personalized badges for your upcoming project by generating HTML and Markdown code. It utilizes the shields.io API for crafting these badges.
            
To know how exactly it generates them, go to [github.com/abdxdev/markdown-badge-generator](https://github.com/abdxdev/markdown-badge-generator).
            
To know how the API works, go to [shields.io/badges](https://shields.io/badges)."""
)
with st.container(border=True):
    st.markdown("### Add elements")
    columnsl = st.columns(2)
    label = columnsl[0].text_input("Label", placeholder="Label", value="Label")
    if not label:
        st.error("Label cannot be empty.")
    message = columnsl[1].text_input("Message", placeholder="Message")
    link = Link(label=label, message=message, color="ffffff")

    logoInc = st.checkbox("Include a logo?")
    if logoInc:
        logo = st.selectbox("Logo", icons)
        link.config("logo", logo)
    else:
        logo = st.selectbox("Logo", icons, disabled=True)


with st.container(border=True):
    st.markdown("### Customize badge")
    link.config("style", st.selectbox("Style", ("flat", "flat-square", "plastic", "for-the-badge", "social")))
    columns1 = st.columns(5)
    columns2 = st.columns(5)
    if logoInc:
        icon = icons.get(link.get("logo"))
        link.config("color", columns1[0].color_picker("Badge Color", value="#" + icon.__dict__["hex"] if link.get("color") is None else "#" + link.get("color"))[1:])
        if columns1[4].button("Get logo color", key="btn1"):
            link.config("color", icon.__dict__["hex"])
        logoColor = columns2[0].color_picker("Logo Color", value="#" + icon.__dict__["hex"])[1:]
        link.config("logoColor", logoColor)
        if columns2[4].button("Get logo color", key="btn2"):
            link.config("logoColor", icon.__dict__["hex"])
    else:
        link.config("color", columns1[0].color_picker("Badge Color", value="#ffffff")[1:])
        columns1[4].button("Get logo color", disabled=True, key="btn1")
        columns2[0].color_picker("Logo Color", value="#ffffff", disabled=True)
        columns2[4].button("Get logo color", disabled=True, key="btn2")


with st.container(border=True):
    text = ((link.get("label").replace("__", "_")).replace("%20", " ")).replace("--", "-")
    md = f"![{text}]({link})"
    if link.get("label"):
        st.markdown(md)
        st.code(md, "None")


st.write("Made with ❤️ by abd")
