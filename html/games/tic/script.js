let grid = ['', '', '', '', '', '', '', '', '']
let turn = Math.round(Math.random())
const syms = ['X', 'O']
do {
  syms[0] = prompt('Player 1 Symbol:', 'X') || 'X'
} while (syms[0].length > 10)
do {
  syms[1] = prompt('Player 2 Symbol:', 'O') || 'O'
} while (syms[1].length > 10)
const arr = Array.from(document.getElementById('board').children)
const output = document.getElementById('turn')
const score = document.getElementById('score')
const cookie = document.cookie ? document.cookie.split('=') : null
let scores = cookie || [0, 0, 0]
if (scores === cookie) {
  scores = cookie[1].split('')
  console.log(scores)
}

output.textContent = `It's Player ${syms[turn]}'s turn.`
document.getElementById('reset').addEventListener('click', reset)
gameStart()
score.textContent = `Player ${syms[0]}: ${scores[0]} Player ${syms[1]}: ${scores[1]} Ties: ${scores[2]}`
function gameStart () {
  for (const i of arr) {
    i.textContent = ''
    i.addEventListener('click', play)
    i.addEventListener('keydown', play)
  }
}
function play (event) {
  const index = arr.indexOf(event.target)
  if (event.key === 'Enter' || !event.key) {
    grid[index] = syms[turn]
    event.target.textContent = syms[turn]
    if (winCheck(index)[0]) {
      output.textContent = `Player ${syms[turn]} wins!`
      for (const element of arr) {
        element.removeEventListener('click', play)
        element.removeEventListener('keydown', play)
      }
      turn === 0 ? ++scores[0] : ++scores[1]
      for (const square of winCheck(index)[1]) {
        arr[square].classList.add('win')
      }
    } else if (grid.filter(n => n !== '').length === 9) {
      output.textContent = "It's a tie!"
      ++scores[2]
    } else {
      turn = turn === 1 ? 0 : 1
      output.textContent = `It's Player ${syms[turn]}'s turn.`
    }
    event.target.removeEventListener('click', play)
    event.target.removeEventListener('keydown', play)
    score.textContent = `Player ${syms[0]}: ${scores[0]} Player ${syms[1]}: ${scores[1]} Ties: ${scores[2]}`
    document.cookie = `score=${scores.join('')}; expires=Fri, 31 Dec 9999 23:59:59 GMT`
    console.log(document.cookie)
  }
}

function winCheck (index) {
  if (index === 0) {
    if ((grid[0] === grid[1] && grid[0] === grid[2])) return [true, [0, 1, 2]]
    if ((grid[0] === grid[3] && grid[0] === grid[6])) return [true, [0, 3, 6]]
    if ((grid[0] === grid[4] && grid[0] === grid[8])) return [true, [0, 4, 8]]
  }
  if (index === 1) {
    if ((grid[1] === grid[2] && grid[1] === grid[0])) return [true, [1, 2, 0]]
    if ((grid[1] === grid[4] && grid[1] === grid[7])) return [true, [1, 4, 7]]
  }
  if (index === 2) {
    if ((grid[2] === grid[1] && grid[2] === grid[0])) return [true, [2, 1, 0]]
    if ((grid[2] === grid[5] && grid[2] === grid[8])) return [true, [2, 5, 8]]
    if ((grid[2] === grid[4] && grid[2] === grid[6])) return [true, [2, 4, 6]]
  }
  if (index === 3) {
    if ((grid[3] === grid[4] && grid[3] === grid[5])) return [true, [3, 4, 5]]
    if ((grid[3] === grid[0] && grid[3] === grid[6])) return [true, [3, 0, 6]]
  }
  if (index === 4) {
    if ((grid[4] === grid[3] && grid[4] === grid[5])) return [true, [4, 3, 5]]
    if ((grid[4] === grid[1] && grid[4] === grid[7])) return [true, [4, 1, 7]]
    if ((grid[4] === grid[0] && grid[4] === grid[8])) return [true, [4, 0, 8]]
    if ((grid[4] === grid[6] && grid[4] === grid[2])) return [true, [4, 6, 2]]
  }
  if (index === 5) {
    if ((grid[5] === grid[2] && grid[5] === grid[8])) return [true, [5, 2, 8]]
    if ((grid[5] === grid[4] && grid[5] === grid[3])) return [true, [5, 4, 3]]
  }
  if (index === 6) {
    if ((grid[6] === grid[3] && grid[6] === grid[0])) return [true, [6, 3, 0]]
    if ((grid[6] === grid[7] && grid[6] === grid[8])) return [true, [6, 7, 8]]
    if ((grid[6] === grid[4] && grid[6] === grid[2])) return [true, [6, 4, 2]]
  }
  if (index === 7) {
    if ((grid[7] === grid[6] && grid[7] === grid[8])) return [true, [7, 6, 8]]
    if ((grid[7] === grid[4] && grid[7] === grid[1])) return [true, [7, 4, 1]]
  }
  if (index === 8) {
    if ((grid[8] === grid[5] && grid[8] === grid[2])) return [true, [8, 5, 2]]
    if ((grid[8] === grid[7] && grid[8] === grid[6])) return [true, [8, 7, 6]]
    if ((grid[8] === grid[4] && grid[8] === grid[0])) return [true, [8, 4, 0]]
  }
  return false
}

function reset () {
  gameStart()
  grid = ['', '', '', '', '', '', '', '', '']
  turn = turn === 1 ? 0 : 1
  output.textContent = `It's Player ${syms[turn]}'s turn.`
  for (const div of Array.from(document.getElementsByClassName('win'))) {
    div.classList.remove('win')
  }
}
