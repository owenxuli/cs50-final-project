$(document).ready(function() {
    var board4 = Chessboard('board4', {
        position: 'start',

    });

    $('#4move1').on('click', function() {
        board4.move('e2-e4')
    })

    $('#4move2').on('click', function() {
        board4.move('c7-c6')
    })

    $('#4startPosition').on('click', board4.start)
});
