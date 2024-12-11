const cage = document.getElementById('cage');
let playerHead,
  playerLoc,
  squarePos,
  dir,
  lose = false,
  scores = 0,
  gameScore = document.getElementById('score'),
  square = document.getElementById('square'),
  player = document.querySelector('.snakeBody'),
  divEl = document.createElement('div'),
  reset = document.getElementById('reset'),
  die = document.getElementById('dead'),
  size = 4,
  i,
  c = 98 / size,
  deBounce = true;

const timeout = value => {
  setTimeout(() => {
    ++i;
    moreSnake();
    player.style.top = playerHead[1] + '%';
    player.style.left = playerHead[0] + '%';
    player.style.height = size + '%';
    player.style.width = size + '%';
    deBounce = true;
    if (lose === false) timeout(value);
  }, 100)
}
//Directions the snake moves
const move = (event) => {
  if (deBounce) {
    if ((event.key === 'ArrowRight' || event.key === 'd') && dir !== 'left') {
      dir = 'right';
      lose = false;
      deBounce = false;
      i === 0 ? timeout(playerHead[0]) : i = 0;
        event.preventDefault();
    } else if ((event.key === 'ArrowLeft' || event.key === 'a') && dir !== 'right') {
      dir = 'left';
      lose = false;
      deBounce = false;
      i === 0 ? timeout(playerHead[0]) : i = 0;
        event.preventDefault();
    } else if ((event.key === 'ArrowUp' || event.key === 'w') && dir !== 'down') {
      dir = 'up';
      lose = false;
      deBounce = false;
      i === 0 ? timeout(playerHead[1]) : i = 0;
        event.preventDefault();
    } else if ((event.key === 'ArrowDown' || event.key === 's') && dir !== 'up') {
      dir = 'down';
      lose = false;
      deBounce = false;
      i === 0 ? timeout(playerHead[1]) : i = 0;
        event.preventDefault();
    }
  }
}
gameStart = () => {
  lose = false;
  i = 0;
  playerLoc = [];
  scores = 0;
  gameScore.textContent = `Score: ${scores}`;
  //Creates a div for snake and selects it, styles it
  cage.appendChild(divEl);
  divEl.className = 'snakeBody';
  let squareEl = document.createElement('div');
  cage.appendChild(squareEl);
  squareEl.setAttribute('id', 'square');
  square = document.getElementById('square');
  player = document.querySelector('.snakeBody');
  playerHead = [size, size];
  playerLoc.push(Array.from(playerHead));
  player.style.height = size + '%';
  player.style.width = size + '%';

  player.style.left = playerHead[0] + '%';
  player.style.top = playerHead[1] + '%';
  squarePos = [[(Math.floor(Math.random() * c)) * size, (Math.floor(Math.random() * c)) * size]];
  square.style.height = size + '%';
  square.style.width = size + '%';

  square.style.left = squarePos[0][0] + '%';
  square.style.top = squarePos[0][1] + '%';
  window.addEventListener('keydown', move);
}

gameOver = () => {
  lose = true;
  dir = null;
  while (cage.firstChild) {
      cage.firstChild.remove();
    }
  die.className = 'die';
  die.textContent = `YOU ARE DEAD SCORE: ${scores} Click Anywhere To Replay`;
  window.removeEventListener('keydown', move);
  window.addEventListener('click', dead = () => {
    die.classList.remove('die');
    removeEventListener('click', dead);
    gameStart();
  })
}

gameStart();
//Function that grows snake
const moreSnake = () => {
  if ((player.style.left === square.style.left) && (player.style.top === square.style.top)) {
    gameScore.textContent = `Score: ${++scores}`;
    //updates squares random position
    squarePos = [[(Math.floor(Math.random() * c)) * size, (Math.floor(Math.random() * c)) * size]];
    while (checkArray(squarePos[0], playerLoc)) squarePos = [[(Math.floor(Math.random() * c)) * size, (Math.floor(Math.random() * c)) * size]];
    square.style.left = squarePos[0][0] + '%';
    square.style.top = squarePos[0][1] + '%';
    playerLoc.unshift(Array.from(playerHead));
    // creates a div element and appends it to the cage. Gives it the class snakeBody
    cage.append(divEl);
    divEl.className = 'snakeBody';
  } else {
    // Takes the already existing div and moves it to the end
    // It will then update the current player and updates div
    cage.append(player);
    player = document.querySelector('.snakeBody');
    divEl = document.createElement('div');
    if (dir === 'right') playerHead[0] += size;
    if (dir === 'left') playerHead[0] -= size;
    if (dir === 'up') playerHead[1] -= size;
    if (dir === 'down') playerHead[1] += size;
    playerLoc.unshift(Array.from(playerHead));
    playerLoc.pop();
    if (checkArray(playerLoc[0], playerLoc.slice(1)) ||
      playerHead[0] < 0 ||
      playerHead[1] < 0 ||
      playerHead[0] > 96 ||
      playerHead[1] > 96) gameOver();
  }
}

checkArray = (a, arr) => {
  for (const element of arr) {
    if (a[0] === element[0] && a[1] === element[1]) {
      return true;
    }
  }
  return false;
}

reset.addEventListener ("click", gameOver);
