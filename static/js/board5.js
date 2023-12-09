$(document).ready(function () {
    var board5 = Chessboard('board5', {
        position: 'start',
    
    });
$('#5move1').on('click', function () {
board5.move('d2-d4')
})

$('#5move2').on('click', function () {
board5.move('d7-d5')
})

$('#5move3').on('click', function () {
    board5.move('c2-c4')
})

$('#5startPosition').on('click', board5.start)
});