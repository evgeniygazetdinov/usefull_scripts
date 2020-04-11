//first implement js calculator


window.onload = function(e){
    let first_window = document.querySelector('input[name=one]');
    let second_window = document.querySelector('input[name=second]');
    let plus = document.querySelector('button.plus');
    res = document.querySelector('span.result');
    plus.addEventListener('click',function(e){
        result= parseInt(first_window.value)+parseInt(second_window.value)
        res.innerText = result;
    });
}
