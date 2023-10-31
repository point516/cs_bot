// script.js
const star = document.querySelector('.star');
const statsBlock = document.querySelector('.stats');

star.addEventListener('click', () => {
    if (statsBlock.style.display === 'none') {
        statsBlock.style.display = 'inline-block';
    } else {
        statsBlock.style.display = 'none';
    }
});

const select = document.getElementById('ai-model');
const info = document.getElementById('info');

select.addEventListener('change', function () {
    const selectedOption = select.value;

    if (selectedOption === 'XGBoost') {
        info.innerHTML = "<strong>XGBoost: </strong> Predictions Accuracy: 79.15% <br> <strong>Important Stats:</strong> Map Winrates, 5 VS 4 Conversions, Team Ratings, Event Ratings, Number of Maps Played";
    } else if (selectedOption === 'CatBoost') {
        info.innerHTML = "<strong>LightGBM: </strong> Predictions Accuracy: 74.36% <br> <strong>Important Stats:</strong> Map Winrates, Team Ratings, 5 VS 4 Conversions, Team Rankings";
    } else if (selectedOption === 'LightGBM') {
        info.innerHTML = "<strong>LightGBM: </strong> Predictions Accuracy: 75.33% <br> <strong>Important Stats:</strong> Map Winrates, Team Ratings, 5 VS 4 Conversions, Team Rankings, 4 VS 5 Conversions";
    } else if (selectedOption === 'LogReg') {
        info.innerHTML = "<strong>Logistic Regression: </strong> Predictions Accuracy: 76.05% <br> <strong>Important Stats:</strong> Map Winrates, Team Ratings, Head to Head Matches, Player Ratings, Team Rankings";
    } else if (selectedOption === 'LDA') {
        info.innerHTML = "<strong>Linear Discriminant Analysis: </strong> Predictions Accuracy: 75.77% <br> <strong>Important Stats:</strong> Map Winrates, Team Ratings, 5 VS 4 Conversions, Team Rankings, 4 VS 5 Conversions";
    }

});