// in target create one one cell /atfer from cell composite row //after from row table



function addCell(tr, val) {
    var td = document.createElement('td');

    td.innerHTML = val;
    td.style.border ='1px solid black'
    tr.appendChild(td)
  }


  function addRow(tbl, val_1, val_2, val_3) {
    var tr = document.createElement('tr');

    addCell(tr, val_1);
    addCell(tr, val_2);
    addCell(tr, val_3);
    tr.style.border ='1px solid black'
 
    tbl.appendChild(tr)
  }

  function main(width,heigth) {
    let body = document.getElementsByTagName('body')[0];
    let tbl = document.createElement('tbl');
    tbl.style.width = width;
    tbl.style.heigth = heigth;
    addRow(tbl, 'foo', 'bar', 'baz');
    addRow(tbl, 'one', 'two', 'three');
    addRow(tbl, 'one', 'two', 'three');
    body.append(tbl)
  }


  main(500,400);
