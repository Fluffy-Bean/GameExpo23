function keepRatio() {
    let games = document.querySelectorAll(".game-box");
    games.forEach((game) => {
        game.style.height = (game.offsetWidth * 1.5) + "px";
    });
}
