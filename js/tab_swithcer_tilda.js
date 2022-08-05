 setTimeout(function() {
var allElements = ['rec475856757', 'rec475856759', 'rec475856761', 'rec475856763', 'rec475856765'];
  var choosenTab = 0;
  function extractButtons(elementsWithButtons){
    for(let i=0;i<elementsWithButtons.length;i++){
      oneButton = elementsWithButtons[i].firstElementChild;
      oneButton.addEventListener ("click", function(e) {
          e.preventDefault();
          choosenTab = i;
          console.log(choosenTab);
          //нужно закрыть все а оставить открыть только нажатый
          for(x=0;x<allElements.length;x++){
            if (x === choosenTab){
                  let myElem = document.getElementById(allElements[x])
                  if (document.getElementById(allElements[x]).classList.contains('hidden')){
                    document.getElementById(allElements[x]).classList.remove('hidden');
                  }
                  else{
                      continue;
                  }
            }
            else{
              var d = document.getElementById(allElements[x]);
              d.classList.add('hidden');
            }
          }
        

        });
    }
  }

  let allHeaders = document.getElementsByClassName('t976__list-item')
  extractButtons(allHeaders);
  }, 1000);
