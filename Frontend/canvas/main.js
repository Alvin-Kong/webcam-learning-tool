let canvas = document.getElementById("canvas");
let context = canvas.getContext("2d");
let reSetCanvas = document.getElementById("clear");
let eraser = document.getElementById("eraser");
let allBtn = document.querySelectorAll(".btn");

// When true, canvas starts drawing
let canDraw = false;
let canErase = false;
// record last point of brush
var x = 0;
var y = 0;


var board = {
  type: "none",
  canDraw: false,
  canErase: false,
  beginX:0,
  beginY:0,
  lineWidth:2,
  imageData:null,
  color:"#000",
  //brush begin
  brushFn:function(e){
    x = e.pageX - canvas.offsetLeft;
    y = e.pageY - canvas.offsetTop;
    context.lineTo(x,y)
    context.strokeStyle = board.color;
    context.lineWidth = board.lineWidth;
    context.lineCap = "round"; //Set line end style
    context.lineJoin = "round"; //Set line intersection style
    context.stroke()
      // drawLine(context, x, y, e.offsetX, e.offsetY);
      // x = e.offsetX;
      // y = e.offsetY;
    
  },
  //brush end

  //rectangle start 
  rectFn:function(e){
    x = e.pageX - canvas.offsetLeft;
    y = e.pageY - canvas.offsetTop;
    context.clearRect(0,0,canvas.offsetWidth,canvas.offsetHeight)
    if(board.imageData!=null){
      context.putImageData(board.imageData,0,0,0,0,canvas.offsetWidth,canvas.offsetHeight)
    }
    context.beginPath()
    context.rect(board.beginX,board.beginY,x-board.beginX,y-board.beginY);
    context.strokeStyle = board.color;
    context.stroke()
    context.closePath()
  }
  //rectangle end

  
};

//brush button
var brushBtn = document.querySelector("#brush");
brushBtn.onclick = function () {

  allBtn.forEach(function(item,i){
    item.classList.remove("active")
  })
  brushBtn.classList.add("active");
  board.type = "brush"
};

//rect button
var rectBtn = document.querySelector("#rect")
rectBtn.onclick = function(){

  allBtn.forEach(function(item,i){
    item.classList.remove("active")
  })
  rectBtn.classList.add("active");
  board.type = "rect"
}

//buttons to set thin, thick, normal 
var lineDivs = document.querySelectorAll(".line")
lineDivs.forEach(function(item,i){
  item.onclick = function(){
    lineDivs.forEach(function(a,b){
      a.classList.remove("active")
    })
    item.classList.add('active')
    if(i == 0){
      board.lineWidth = 2;   
    }else if (i == 1){
      board.lineWidth = 4;
    }else{
      board.lineWidth = 8;
    }
  }
})

var colorInput = document.querySelector("#color")
colorInput.onchange = function(e){
board.color = colorInput.value;
}

// event.offsetX, event.offsetY gives the (x,y) offset from the edge of the canvas
// Add the event listeners for mousedown, mousemove, and mouseup
canvas.addEventListener("mousedown", function (e) {
  board.canDraw = true;
  // x = e.offsetX;
  // y = e.offsetY;
  if(board.type == "rect"){
    x = e.pageX - canvas.offsetLeft;
    y = e.pageY - canvas.offsetTop;
    board.beginX = x;
    board.beginY = y;
  }

  if(board.type == "brush"){
    x = e.pageX - canvas.offsetLeft;
    y = e.pageY - canvas.offsetTop;
    board.beginX = x;
    board.beginY = y;
    context.beginPath()
    context.moveTo(x,y)
  }

});

canvas.addEventListener("mousemove", function (e) {
  if (board.canDraw) {
    var strFn = board.type + 'Fn'
    board[strFn](e)
  }
});

canvas.addEventListener("mouseup", function (e) {
  board.imageData = context.getImageData(0,0,canvas.offsetWidth,canvas.offsetHeight)
  board.canDraw = false;

  if(board.type == "brush"){
    context.closePath();
  }
});


//clear canvas
reSetCanvas.onclick = function () {
  context.clearRect(0, 0, canvas.width, canvas.height);
};

//erase drawings
eraser.onclick = function () {
  canErase = true;
  eraser.classList.add("active");
  brush.classList.remove("active");
};






//request and response of center point
function getCenter() {
  const express = require("express");
  const { spawn } = require("child_process");
  const app = express();
  const port = 5000;

  app.get("/", (req, res) => {
    var dataset = [];
    const python = spawn("python", ["../Backend/get_center.py"]);
    python.stdout.on("data", function (data) {
      console.log("Pipe data from python scrupt ...");
      dataset.push(data);
    });

    python.on("close", (code) => {
      console.log(`child process close all stdio with code ${code}`);
      res.send(dataset.join(""));
    });
  });

  app.listen(port, () => console.log(`Example app listening on port ${port}!`));
}
