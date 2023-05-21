window.onscroll = () => {
    scrollFunction();
    checkSection();
};
window.onload = () => {
    keepRatio()
    resizeNav();
    scrollFunction();
    checkSection();
};
window.onresize = () => {
    keepRatio()
    resizeNav();
    checkSection();
};
