$(document).ready(function () {
    var board1 = Chessboard('board1', {
        position: 'start',
    });
$('#1move1').on('click', function () {
board1.move('e2-e4')
})

$('#1move2').on('click', function () {
board1.move('c7-c5')
})

$('#1startPosition').on('click', board1.start)
});