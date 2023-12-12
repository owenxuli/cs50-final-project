$(document).ready(function() {
    // initialize the board with the starting position
    var board1 = Chessboard('board1', {
        position: 'start',
    });

    // this will move the e2 pawn to e4 when the button is clicked
    $('#1move1').on('click', function() {
        board1.move('e2-e4')
    })

    // this will move the c7 pawn to c5 when the button is clicked
    $('#1move2').on('click', function() {
        board1.move('c7-c5')
    })

    // this will move all the pieces to their starting position when the button is clicked
    $('#1startPosition').on('click', board1.start)
});
