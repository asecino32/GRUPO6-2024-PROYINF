document.getElementById('colorButton').addEventListener('click', function() {
    const colors = ['#ff5733', '#33ff57', '#3357ff', '#ff33a1', '#f3ff33'];
    const randomColor = colors[Math.floor(Math.random() * colors.length)];
    document.getElementById('header').style.backgroundColor = randomColor;
});
