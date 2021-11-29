//get all selectors 
let canvas = document.getElementById("canvas");
let context = canvas.getContext("2d");
let reSetCanvas = document.getElementById("#clear");
let undo = document.getElementById("#undo");
let allBtn = document.querySelectorAll(".btn");
let colorInput = document.querySelector("#color");
let downloadBtn = document.querySelector(".download");


canvas.style.backgroundImage = "url('/Users/reedbower/PycharmProjects/webcam-learning-tool/Backend/Tracing/Original/8.png')"

function change_background(){
    base_image = new Image();
    base_image.src = '/Users/reedbower/PycharmProjects/webcam-learning-tool/Backend/Tracing/Original/8.png';
    base_image.onload = function(){
        context.drawImage(background,0,0);
    }
  }

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
  lineWidth:10,
  imageData:null,
  color:"#FF0000",

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

};



//brush button
var brushBtn = document.querySelector("#brush");
brushBtn.onclick = function () {

  allBtn.forEach(function(item,i){
    item.classList.remove("active")
  })
  brushBtn.classList.add("active");
  board.type = "brush"
  change_background();
};


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
}

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


///////////////////////////////////// webcam drawing /////////////////////////////////////
// Function to get data from local API
const api_url = 'http://127.0.0.1:5000/';
async function getData() {
    let response = await axios.get(api_url)
    .catch(function(error) {
        console.log(error);
        alert(error);
    });
    return response;
}


// Helper Function to translate a Promise response from API to JSON data
async function getapiData() {
  var apiData = await getData();
  return apiData;
}


// Function to test whether API data can be retrieved
// Press N to get sample API data   
document.addEventListener('keypress', async event => {
  if (event.code === 'KeyN') {
    var data = await getapiData();
    console.log(data);
  }
})


// Main drawing functionality
document.addEventListener('keypress', async (e) => {
  if ((e).code === 'Enter') {
    board.canDraw = true;
    console.log("Drawing Start")
    var startapiData = await getapiData();
    // console.log(startapiData);
    var startCenter = startapiData.data.results["center"];
    var startX = startapiData.data.results["x"];
    var startY = startapiData.data.results["y"];
    // console.log("start: " + startX + ", " + startY);

    // Main while loop to draw
    while (board.canDraw) {
      var nextapiData = await getapiData();
      // console.log(nextapiData);
      var nextCenter = nextapiData.data.results["center"];
      var nextX = nextapiData.data.results["x"];
      var nextY = nextapiData.data.results["y"];
      // console.log("next: " + nextX + ", " + nextY);
      
      drawLine(startX, startY, nextX, nextY)

      // Press 'M' key to stop drawing and exit out of while loop
      document.addEventListener('keypress', event => {
        if (event.code === 'Space') {
          board.imageData = context.getImageData(0,0,canvas.offsetWidth,canvas.offsetHeight);
          board.canDraw = false;
          console.log("Drawing Stop")
        }
      });

      startX = nextX;
      startY = nextY;
    }
  }
});

//make_base('/Users/reedbower/PycharmProjects/webcam-learning-tool/Backend/Tracing/Original/8.png');
//make_base();

// HTML
// style = "background-image: url('/Users/reedbower/PycharmProjects/webcam-learning-tool/Backend/Tracing/Original/8.png');"


// Function to create drawing lines
function drawLine(x_start, y_start, x_end, y_end) {
  context.beginPath();
  context.moveTo(x_start, y_start);
  context.lineTo(x_end, y_end);
  context.strokeStyle = board.color;
  context.lineWidth = board.lineWidth;
  context.lineCap = "round"; //Set line end style
  context.lineJoin = "round"; //Set line intersection style
  context.stroke();
  context.closePath();
}
///////////////////////////////////// webcam drawing /////////////////////////////////////


// //request and response of center point
// function getCenter() {
//   const express = require("express");
//   const { spawn } = require("child_process");
//   const app = express();
//   const port = 5000;

//   app.get("/", (req, res) => {
//     var dataset = [];
//     const python = spawn("python", ["../Backend/get_center.py"]);
//     python.stdout.on("data", function (data) {
//       console.log("Pipe data from python scrupt ...");
//       dataset.push(data);
//     });

//     python.on("close", (code) => {
//       console.log(`child process close all stdio with code ${code}`);
//       res.send(dataset.join(""));
//     });
//   });

//   app.listen(port, () => console.log(`Example app listening on port ${port}!`));
// }
