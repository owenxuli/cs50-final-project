$(document).ready(function () {
    var board3 = Chessboard('board3', {
        position: 'start',
    
    });
$('#move1Btn').on('click', function () {
board3.move('e2-e4')
})

$('#move2Btn').on('click', function () {
board3.move('d2-d4', 'g8-f6')
})

$('#startPositionBtn').on('click', board3.start)
});