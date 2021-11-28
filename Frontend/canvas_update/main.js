//get all selectors 
let canvas = document.getElementById("canvas");
let context = canvas.getContext("2d");
let reSetCanvas = document.getElementById("#clear");
let undo = document.getElementById("#undo");
let allBtn = document.querySelectorAll(".btn");
let colorInput = document.querySelector("#color");
let downloadBtn = document.querySelector(".download");


// record  x and y coordinates point of brush
var x = 0;
var y = 0;

//define array to store record of drawing
let restore_array = [];
let index = -1;

//drawing board function
var board = {
  type: "none",
  canDraw: false,
  canUndo: false,
  beginX:0,
  beginY:0,
  lineWidth:2,
  imageData:null,
  color:"#000",

  //brush function start
  brushFn:function(e){
    x = e.pageX - canvas.offsetLeft;
    y = e.pageY - canvas.offsetTop;
    context.lineTo(x,y)
    context.strokeStyle = board.color;
    context.lineWidth = board.lineWidth;
    context.lineCap = "round"; //Set line end style
    context.lineJoin = "round"; //Set line intersection style
    context.stroke()
  },
  //brush function end

  //rectangle function start
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
  },
  //rectangle function end

  //arc function start
  arcFn:function(e){
    x = e.pageX - canvas.offsetLeft;
    y = e.pageY - canvas.offsetTop;
    context.clearRect(0,0,canvas.offsetWidth,canvas.offsetHeight)
    if(board.imageData!=null){
      context.putImageData(board.imageData,0,0,0,0,canvas.offsetWidth,canvas.offsetHeight)
    }
    context.beginPath()
    var radius = 2000; // set default radius to start with
    var radiusX = Math.min(x-board.beginX, radius); // set horizontal radius to be atleast as wide as width of div
    var radiusY = Math.min(y-board.beginY, radius); // set vertical radius to be atleast as high as height of div
    radius = Math.min(radiusX, radiusY); // now set the radius of the circle equal to the minimum of the two values so that it is a perfect circle
    context.arc(x,y,radius,0, 2 * Math.PI,false);
    context.strokeStyle = board.color;
    context.stroke()
    context.closePath()
  }
  //arc function end 
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

//arc button
var arcBtn = document.querySelector("#arc")
arcBtn.onclick = function(){

  allBtn.forEach(function(item,i){
    item.classList.remove("active")
  })
  arcBtn.classList.add("active");
  board.type = "arc"
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

//color panel
colorInput.onchange = function(e){
board.color = colorInput.value;
}

//download button
downloadBtn.onclick = function(){
  var url = canvas.toDataURL()
  console.log(url);
  const a = document.createElement("a");
  document.body.appendChild(a);
  a.href = canvas.toDataURL();
  a.download = "canvas-image.png";
  a.click();
  document.body.removeChild(a);
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

  if(board.type == "arc"){
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

  if(e.type == 'mouseup'){
  restore_array.push(context.getImageData(0,0,canvas.width,canvas.height));
  index+=1;
  console.log(restore_array);
  } 
});

//clear canvas function
function clear_canvas() {
  context.clearRect(0, 0, canvas.width, canvas.height);
  restore_array = [];
  index = -1;
};

//undo drawings function
function undo_last(){
  if(index <= 0){
    clear_canvas();
  }else{
    index -= 1;
    restore_array.pop();
    context.putImageData(restore_array[index],0,0);
  }
}




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
