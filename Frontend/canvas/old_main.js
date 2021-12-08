//get all selectors 
let canvas = document.getElementById("canvas");
let context = canvas.getContext("2d");
let reSetCanvas = document.getElementById("#clear");
let undo = document.getElementById("#undo");
let allBtn = document.querySelectorAll(".btn");
let colorInput = document.querySelector("#color");
let downloadBtn = document.querySelector(".download");
let cursor = document.getElementById("cursor");
let cursorOn = false;
const api_url = 'http://127.0.0.1:5000/';


// record  x and y coordinates point of brush
var x = 0;
var y = 0;

//define array to store record of drawing
let restore_array = [];
let index = -1;
let limiter = 0;

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
  board.imageData = context.getImageData(0,0,canvas.offsetWidth,canvas.offsetHeight);
};

//undo drawings function
function undo_last(){
  if(index <= 0){
    clear_canvas();
  }else{
    index -= 1;
    restore_array.pop();
    context.putImageData(restore_array[index],0,0);
    board.imageData = context.getImageData(0,0,canvas.offsetWidth,canvas.offsetHeight);
  }
}


// set webcam canvas cursor
function set_cursor(x, y) {
  var left = x - 8;
  var top = y - 8;

  if (left < 3) {
      left = 3;
  }
  if (left > 787) {
      left = 787;
  }
  if (top < 1) {
      top = 1;
  }
  if (top > 585) {
      top = 585;
  }
  cursor.style.left = left + "px";
  cursor.style.top = top + "px";
}


// Function to get data from local API
async function getData() {
    let response = await axios.get(api_url, {
      params: {
        isOff: false,
      }
  })
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


document.addEventListener('keypress', async event => {
  if (event.code === 'KeyM') {
    cursorOn = true;
    while(cursorOn) {
      var data = await getapiData();
      var x = data.data.tracking_response.tracking_results["x"];
      var y = data.data.tracking_response.tracking_results["y"];
      set_cursor(x, y);
    }
  }
})


// Main drawing functionality
document.addEventListener('keypress', async (e) => {
  if ((e).code === 'Enter') {
    board.canDraw = true;
    console.log("Drawing Start")
    var startapiData = await getapiData();
    var startCenter = startapiData.data.tracking_response.tracking_results["center"];
    var startX = startapiData.data.tracking_response.tracking_results["x"];
    var startY = startapiData.data.tracking_response.tracking_results["y"];

    // Main while loop to draw
    while (board.canDraw) {
      var nextapiData = await getapiData();
      var nextCenter = nextapiData.data.tracking_response.tracking_results["center"];
      var nextX = nextapiData.data.tracking_response.tracking_results["x"];
      var nextY = nextapiData.data.tracking_response.tracking_results["y"];
      set_cursor(nextX, nextY);      
      drawLine(startX, startY, nextX, nextY)
      startX = nextX;
      startY = nextY;
    }
  }
});


// Press 'Space' key to stop drawing and exit out of while loop
document.addEventListener('keypress', event => {
  if (event.code === 'Space') {
    board.imageData = context.getImageData(0,0,canvas.offsetWidth,canvas.offsetHeight);
    board.canDraw = false;
    cursorOn = false;
    restore_array.push(context.getImageData(0,0,canvas.width,canvas.height));
    index+=1;
    console.log("Drawing Stop")
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