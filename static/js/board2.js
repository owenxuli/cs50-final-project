$(document).ready(function () {
    var board2 = Chessboard('board2', {
        position: 'start',
    
    });
$('#2move1').on('click', function () {
    board2.move('e2-e4')
})

$('#2move2').on('click', function () {
    board2.move('e7-e5')
})

$('#2move3').on('click', function () {
    board2.move('g1-f3')
})

$('#2move4').on('click', function () {
    board2.move('b8-c6')
})

$('#2move5').on('click', function () {
    board2.move('f1-b5')
})

$('#2startPosition').on('click', board2.start)
});