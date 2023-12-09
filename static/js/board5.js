$(document).ready(function () {
    var board5 = Chessboard('board5', {
        position: 'start',
    
    });
$('#move1Btn').on('click', function () {
board5.move('e2-e4')
})

$('#move2Btn').on('click', function () {
board5.move('d2-d4', 'g8-f6')
})

$('#startPositionBtn').on('click', board5.start)
});