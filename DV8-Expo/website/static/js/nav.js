const defaultTitle = "DV8 Game Expo <span>2023</span>";
let prevTitle;

window.onscroll = () => {
    scrollFunction();
    checkSection();
};
window.onload = () => { scrollFunction() };

function scrollFunction() {
    let nav = document.querySelector("nav");
    // let scrollHeight = window.innerHeight - nav.offsetHeight;
    let scrollHeight = 0;

    if (document.body.scrollTop > scrollHeight ||
        document.documentElement.scrollTop > scrollHeight) {
        nav.classList.add("scrolled");
    } else {
        nav.classList.remove("scrolled");
    }
}

function checkSection() {
    // Get the nav and sections
    let navTitle = document.querySelector("nav > h1");
    let sections = document.querySelectorAll("section");

    // If we're at the top of the page, set the title to the default
    if (window.pageYOffset < sections[0].offsetTop) {
        // If we're already on the default title, don't do anything as it'll break the animation
        if (prevTitle === defaultTitle) return;

        navTitle.innerHTML = defaultTitle;
        navTitle.style.animation = "title-change 0.2s ease-in-out";
        prevTitle = defaultTitle;

        // Remove the animation after it's done, so we can animate again
        setTimeout(() => { navTitle.style.animation = ""; }, 200);
    }

    // While at this point we may not need to check for the sections
    // There aren't many sections, so it's not a big deal
    sections.forEach((section) => {
        // Get the position of the section
        let top = section.offsetTop;
        let bottom = section.offsetTop + section.offsetHeight;

        // If the section is on the screen is:
        // 1. The top of the section is above the top of the screen
        // 2. The bottom of the section is below the bottom of the screen
        if (window.pageYOffset >= top && window.pageYOffset < bottom) {
            // If we're already on the section, don't do anything as it'll break the animation
            if (prevTitle === section.id) return;

            navTitle.innerHTML = section.id;
            navTitle.style.animation = "title-change 0.2s ease-in-out";
            prevTitle = section.id;

            // Remove the animation after it's done, so we can animate again
            setTimeout(() => { navTitle.style.animation = ""; }, 200);
        }
    });
}
