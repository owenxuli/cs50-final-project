$(document).ready(function () {
    var board3 = Chessboard('board3', {
        position: 'start',
    
    });
    
$('#3move1').on('click', function () {
    board3.move('e2-e4')
})

$('#3move2').on('click', function () {
    board3.move('e7-e5')
})

$('#3move3').on('click', function () {
    board3.move('g1-f3')
})

$('#3move4').on('click', function () {
    board3.move('b8-c6')
})

$('#3move5').on('click', function () {
    board3.move('f1-c4')
})

$('#3startPosition').on('click', board3.start)
});