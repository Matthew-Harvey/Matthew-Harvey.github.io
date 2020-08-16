function run() {
    var column = document.getElementById('end');
    var rangelow = document.getElementById('range1').value;
    var rangehigh = document.getElementById('range2').value;
    column.innerHTML = ""
    for (var i=rangelow; i<=rangehigh; i++) {
        if (i % 3 === 0 && i % 5 === 0) {
            column.innerHTML += " fizzbuzz ";
        } else if (i % 3 === 0) {
            column.innerHTML += " fizz ";
        } else if (i % 5 === 0) {
            column.innerHTML += " buzz ";
        } else {
            column.innerHTML += " " + i + " ";
        }
    }
}
function run2() {
    var column2 = document.getElementById('end2');
    var num = document.getElementById('num1').value;
    column2.innerHTML = ""
    if (num % 3 === 0 && num % 5 === 0) {
        column2.innerHTML += " fizzbuzz ";
    } else if (num % 3 === 0) {
        column2.innerHTML += " fizz ";
    } else if (num % 5 === 0) {
        column2.innerHTML += " buzz ";
    } else {
        column2.innerHTML += " " + num + " ";
        }
}