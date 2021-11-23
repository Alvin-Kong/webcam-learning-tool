/////////////////////////////// old variable initialization ///////////////////////////////
// const canvas = document.getElementById("canvas");
// const context = canvas.getContext("2d");

// canvas is same as screen height and screen width 
// let pageWidth = document.documentElement.clientWidth;
// let pageHeight = document.documentElement.clientHeight;
// canvas.width = pageWidth;
// canvas.height = pageHeight;

// When true, moving the mouse draws on the canvas
// set the current canvas function as the pen state 
// let isDrawing = false;
// let startPoint = {x: 300, y: 200};
// let nextPoint = {x: undefined, y: undefined};
/////////////////////////////// old variable initialization ///////////////////////////////


/////////////////////////////// new variable initialization ///////////////////////////////
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
/////////////////////////////// new variable initialization ///////////////////////////////


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


///////////////////////////////////// mouse drawing /////////////////////////////////////
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
    context.beginPath();
    context.moveTo(x,y);
  }
});


canvas.addEventListener("mousemove", function (e) {
  if (board.canDraw) {
    var strFn = board.type + 'Fn';
    board[strFn](e);
  }
});


canvas.addEventListener("mouseup", function (e) {
  board.imageData = context.getImageData(0,0,canvas.offsetWidth,canvas.offsetHeight);
  board.canDraw = false;

  if(board.type == "brush"){
    context.closePath();
  }
});
///////////////////////////////////// mouse drawing /////////////////////////////////////


//////////////////////////////////////// buttons ////////////////////////////////////////
// brush button
var brushBtn = document.querySelector("#brush");
brushBtn.onclick = function () {
  allBtn.forEach(function(item,i){
    item.classList.remove("active");
  });
  brushBtn.classList.add("active");
  board.type = "brush";
}


// rect button
var rectBtn = document.querySelector("#rect")
rectBtn.onclick = function() {
  allBtn.forEach(function(item,i){
    item.classList.remove("active");
  });
  rectBtn.classList.add("active");
  board.type = "rect";
}


// buttons to set thickness of pen size
var lineDivs = document.querySelectorAll(".line");
lineDivs.forEach(function(item,i) {
  item.onclick = function() {
    lineDivs.forEach(function(a,b){
      a.classList.remove("active");
    })
    item.classList.add('active');
    if(i == 0) {
      board.lineWidth = 2;   
    } else if (i == 1) {
      board.lineWidth = 4;
    } else {
      board.lineWidth = 8;
    }
  }
});


// change pen color
var colorInput = document.querySelector("#color")
colorInput.onchange = function(e){
  board.color = colorInput.value;
}


// clear canvas
reSetCanvas.onclick = function () {
  context.clearRect(0, 0, canvas.width, canvas.height);
};


// erase drawings
eraser.onclick = function () {
  canErase = true;
  eraser.classList.add("active");
  brush.classList.remove("active");
};
//////////////////////////////////////// buttons ////////////////////////////////////////
