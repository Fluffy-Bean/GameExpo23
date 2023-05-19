const defaultTitle = "DV8 Game Expo <span>2023</span>";
let navSpacing = (3 * 16); // The amount of pixels to offset the section by
let prevElement = null;

window.onscroll = () => {
    scrollFunction();
    checkSection();
};
window.onload = () => {
    resizeNav();
    scrollFunction();
    checkSection();
};
window.onresize = () => {
    resizeNav();
    checkSection();
}

function resizeNav() {
    if (window.innerWidth > 600) {
        navSpacing = (3 * 16);
    } else {
        navSpacing = (6 * 16);
    }
}

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
    let navTitle = document.querySelector(".title > p");
    let sections = document.querySelectorAll("section");

    // If we're at the top of the page, set the title to the default
    if ((window.pageYOffset + navSpacing) < sections[0].offsetTop) {
        // If we're already on the default title, don't do anything as it'll break the animation
        if (prevElement === null) return;

        navTitle.innerHTML = defaultTitle;
        navTitle.style.animation = "title-change 0.2s ease-in-out";
        prevElement = null;

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
        if ((window.pageYOffset + navSpacing) >= top && window.pageYOffset < (bottom - navSpacing)) {
            // If we're already on the section, don't do anything as it'll break the animation
            if (prevElement === section) return;

            navTitle.innerHTML = section.id.split("_").join(" ");
            navTitle.style.animation = "title-change 0.2s ease-in-out";
            prevElement = section;

            // Remove the animation after it's done, so we can animate again
            setTimeout(() => { navTitle.style.animation = ""; }, 200);
        }
    });
}


document.querySelectorAll("nav > ul > li > a").forEach((element) => {
    element.onclick = () => {
        let anchor = location.hash.split("#")[1].toString();
        let element = document.getElementById(anchor);

        if (element === null) {
            window.scrollTo({ top: 0, behavior: "smooth" });
        } else {
            window.scrollTo({top: (element.offsetTop + navSpacing), behavior: "smooth"});
        }
    }
});
