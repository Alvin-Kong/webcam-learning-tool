//get all selectors 
let canvas = document.getElementById("canvas");
let context = canvas.getContext("2d");
let reSetCanvas = document.getElementById("#clear");
let undo = document.getElementById("#undo");
let allBtn = document.querySelectorAll(".btn");
let colorInput = document.querySelector("#color");
let downloadBtn = document.querySelector(".download");
let backgroundBtn = document.querySelector("#background");
let templatePath = ''
let cursor = document.getElementById("cursor");
let cursorOn = false;

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


// Function to set the position of the webcam cursor
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


// Function to request template filepath from API
async function getTemplate(choice) {
  console.log(choice)
  let response = await axios.get(api_url, {
    params: {
      getTemplatePath: choice
    }
  })
  .catch(function(error) {
    console.log(error);
    alert(error);
  });
  // console.log(response)
  return response;
}


// Get method to get template filepath
async function getChoice(choice)
{
  console.log(choice)
   var received_data = await getTemplate(choice)
   var path = received_data.data.template_response.template_results["template"]
   return path
}


// Function to change the template shown on the canvas
async function change_background(choice){
  console.log("choice: ", choice)
  clear_canvas()
  var path = await getChoice(choice)
  // console.log(path)
  string = path.replace('C:','')
  string = string.replaceAll('\\', '/')
  templatePath = string
  console.log(string)
  url = "url(" + String(string) + ")"
  // console.log(url)
  canvas.style.backgroundImage = url
  document.getElementById("rating").innerHTML = "";
  document.getElementById("percentage").innerHTML = "";
}


//brush button
var brushBtn = document.querySelector("#brush");
brushBtn.onclick = function () {

  allBtn.forEach(function(item,i){
    item.classList.remove("active")
  })
  brushBtn.classList.add("active");
  board.type = "brush"
};


// Function to send file to backend for processing
async function fileUpload(filename) {
  let response = await axios.post(api_url, {
    postTemplatePath: templatePath,
    file: filename
  })
  .catch(function(error) {
    console.log(error);
    alert(error);
  });
  return response
}


// Function to request 
async function sendFile(filename) {
  let response = await fileUpload(filename)
  return response
}


// download button
function download() {
  const a = document.createElement("a");
  document.body.appendChild(a);
  a.href = canvas.toDataURL();
  // window.open
  a.download = "canvas-image.png";
  a.click();
  document.body.removeChild(a);
}


// Function to initiate file upload to backend when button is clicked
async function upload() {
  var dataURL = canvas.toDataURL();
  var result = await sendFile(dataURL);
  var rating = result.data.tracing_stats_response.rating;
  var percentage = result.data.tracing_stats_response.percentage;
  document.getElementById("rating").innerHTML = "Rating(0 = non-passable, 1 = average, 2 = good): " + rating;
  document.getElementById("percentage").innerHTML = "Percentage: " + percentage + "%";
  console.log(result);
}


// event.offsetX, event.offsetY gives the (x,y) offset from the edge of the canvas
// Add the event listeners for mousedown, mousemove, and mouseup
canvas.addEventListener("mousedown", function (e) {
  board.canDraw = true;

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
  document.getElementById("rating").innerHTML = "";
  document.getElementById("percentage").innerHTML = "";
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
  document.getElementById("rating").innerHTML = "";
  document.getElementById("percentage").innerHTML = "";
}


// Function to get webcam tracking data from local API
const api_url = 'http://127.0.0.1:5000/';
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


// Function to initialize the webcam cursor
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


// Main webcam drawing functionality
document.addEventListener('keypress', async (e) => {
  if ((e).code === 'Enter') {
    board.canDraw = true;
    console.log("Drawing Start")
    var startapiData = await getapiData();
    var startCenter = startapiData.data.tracking_response.tracking_results["center"];
    var startX = startapiData.data.tracking_response.tracking_results["x"];
    var startY = startapiData.data.tracking_response.tracking_results["y"];
    cursorOn = false;

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


// Press 'Space' key to stop drawing
document.addEventListener('keypress', event => {
  if (event.code === 'Space') {
    board.imageData = context.getImageData(0,0,canvas.offsetWidth,canvas.offsetHeight);
    board.canDraw = false;
    cursorOn = false;

    restore_array.push(context.getImageData(0,0,canvas.width,canvas.height));
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