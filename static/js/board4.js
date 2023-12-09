$(document).ready(function () {
    var board4 = Chessboard('board4', {
        position: 'start',
    
    });
$('#move1Btn').on('click', function () {
board4.move('e2-e4')
})

$('#move2Btn').on('click', function () {
board4.move('d2-d4', 'g8-f6')
})

$('#startPositionBtn').on('click', board4.start)
});