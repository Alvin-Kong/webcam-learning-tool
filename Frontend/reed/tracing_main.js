//get all selectors 
let canvas = document.getElementById("canvas");
let context = canvas.getContext("2d");
let reSetCanvas = document.getElementById("#clear");
let undo = document.getElementById("#undo");
let allBtn = document.querySelectorAll(".btn");
let colorInput = document.querySelector("#color");
let downloadBtn = document.querySelector(".download");
let backgroundBtn = document.querySelector("#background");

background = ""

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

async function getChoice(choice)
{
  console.log(choice)
   var received_data = await getTemplate(choice)
   var path = received_data.data.template_response.template_results["template"]
   return path
}

async function change_background(choice){
  console.log("choice: ", choice)
  clear_canvas()
  var path = await getChoice(choice)
  // console.log(path)
  string = path.replace('C:','')
  string = string.replaceAll('\\', '/')
  console.log(string)
  url = "url(" + String(string) + ")"
  // console.log(url)
  canvas.style.backgroundImage = url
}


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
};


upload_api_url = 'http://127.0.0.1:5000/upload'
async function fileUpload(filename) {
  let response = await axios.post(api_url, {
    file: filename
  })
  .catch(function(error) {
    console.log(error);
    alert(error);
  });

  return response
}


async function sendFile(filename) {
  let response = await fileUpload(filename)
  return response
}


//download button
// downloadBtn.onclick = function(){
//   // var url = canvas.toDataURL()
//   // console.log(url);
//   const a = document.createElement("a");
//   document.body.appendChild(a);
//   a.href = canvas.toDataURL();
//   // window.open
//   a.download = "canvas-image.png";
//   a.click();
//   sendFile(a.href);
//   document.body.removeChild(a);
// }


// downloadBtn.onclick = function() {
//   let canvasFile = convertCanvasToImage();
//   document.getElementById("uploadForm").file = canvasFile;
//   document.getElementById("uploadForm").submit();
// }


// downloadBtn.onclick = function() {
//   var dataURL = canvas.toDataURL('image/png');
//   var blob = dataURItoBlob2(dataURL);
//   let canvasFile = new File([blob], "canvas-file");
//   document.getElementById("uploadForm").file = canvasFile;
//   document.getElementById("uploadForm").submit();
// }


// downloadBtn.onclick = function() {

//   const a = document.createElement("a");
//   document.body.appendChild(a);
//   a.href = canvas.toDataURL();
//   console.log(a.href);
//   var inputs = document.getElementById("uploadForm").elements;
//   inputs["file"] = a;
//   document.forms["uploadForm"].submit();
//   // a.download = "canvas-image.png"
//   a.click()
//   document.body.removeChild(a);
// }


downloadBtn.onclick = function() {
  var dataURL = canvas.toDataURL();
  var result = sendFile(dataURL)
  console.log(result)
}


// downloadBtn.onclick = function() {
//   var dataURL = canvas.toDataURL('image/png');
//   console.log(dataURL)

//   // var upload = sendFile(dataURL)
//   // console.log(upload)

//   // document.getElementById("uploadForm").File = dataURL
//   // document.getElementById("uploadForm").submit()

//   // var data = new FormData()
//   // var file = dataURLtoFile(dataURL, "canvas-download")
//   // console.log(file.name)
//   // data.append('file', file, file.name)
  

//   var blob = dataURItoBlob2(dataURL);
//   console.log(blob)
//   var fd = new FormData(document.forms[0]);
//   // var xhr = new XMLHttpRequest();
//   // fd.append("canvasImage", blob);
//   fd.append("file", blob, "file");
//   console.log(fd)
//   var newFile = new File([blob], "canvas-download");
//   console.log(newFile)
  
//   // xhr.open('POST', '/', true);
//   // xhr.send(fd)

//   var upload = sendFile(newFile)
//   console.log(upload)

//   // document.getElementById("uploadForm").File = newFile;
//   // document.getElementById("uploadForm").submit();
// }


function convertCanvasToImage() {
  let image = new Image();
  image.src = canvas.toDataURL('image/png');
  image.id = "canvas-download"
  return image;
}

function convertCanvasToFile(blob) {
  let file = new File(blob, "canvas-file");
  file.src = canvas.toDataURL();
  file.name = "canvas-download"
  return file;
}


const dataURLtoFile = (dataurl, filename) => {
  const arr = dataurl.split(',')
  const mime = arr[0].match(/:(.*?);/)[1]
  const bstr = atob(arr[1])
  let n = bstr.length
  const u8arr = new Uint8Array(n)
  while (n) {
    u8arr[n - 1] = bstr.charCodeAt(n - 1)
    n -= 1 // to make eslint happy
  }
  return new File([u8arr], filename, { type: mime })
}

function dataURItoBlob(dataURI) {
  // convert base64/URLEncoded data component to raw binary data held in a string
  var byteString;
  if (dataURI.split(',')[0].indexOf('base64') >= 0)
      byteString = atob(dataURI.split(',')[1]);
  else
      byteString = unescape(dataURI.split(',')[1]);

  // separate out the mime component
  var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];

  // write the bytes of the string to a typed array
  var ia = new Uint8Array(byteString.length);
  for (var i = 0; i < byteString.length; i++) {
      ia[i] = byteString.charCodeAt(i);
  }

  return new Blob([ia], {type:mimeString});
}

function dataURItoBlob2(dataURI) {
  // convert base64 to raw binary data held in a string
  // doesn't handle URLEncoded DataURIs - see SO answer #6850276 for code that does this
  var byteString = atob(dataURI.split(',')[1]);

  // separate out the mime component
  var mimeString = dataURI.split(',')[0].split(':')[1].split(';')[0];

  // write the bytes of the string to an ArrayBuffer
  var ab = new ArrayBuffer(byteString.length);
  var ia = new Uint8Array(ab);
  for (var i = 0; i < byteString.length; i++) {
      ia[i] = byteString.charCodeAt(i);
  }

  //Old Code
  //write the ArrayBuffer to a blob, and you're done
  //var bb = new BlobBuilder();
  //bb.append(ab);
  //return bb.getBlob(mimeString);

  //New Code
  return new Blob([ab], {type: mimeString});
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
    let response = await axios.get(api_url, {
      params: {
          getTraceData: false,
          getTemplatePath: false,
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


// Main drawing functionality
document.addEventListener('keypress', async (e) => {
  if ((e).code === 'Enter') {
    board.canDraw = true;
    console.log("Drawing Start")
    var startapiData = await getapiData();
    // console.log(startapiData);
    var startCenter = startapiData.data.tracking_response.tracking_results["center"];
    var startX = startapiData.data.tracking_response.tracking_results["x"];
    var startY = startapiData.data.tracking_response.tracking_results["y"];
    // console.log("start: " + startX + ", " + startY);
    limiter = 0;

    // Main while loop to draw
    while (board.canDraw) {
      var nextapiData = await getapiData();
      // console.log(nextapiData);
      var nextCenter = nextapiData.data.tracking_response.tracking_results["center"];
      var nextX = nextapiData.data.tracking_response.tracking_results["x"];
      var nextY = nextapiData.data.tracking_response.tracking_results["y"];
      // console.log("next: " + nextX + ", " + nextY);
      
      drawLine(startX, startY, nextX, nextY)

      // Press 'M' key to stop drawing and exit out of while loop
      document.addEventListener('keypress', event => {
        if (event.code === 'Space') {
          board.imageData = context.getImageData(0,0,canvas.offsetWidth,canvas.offsetHeight);
          board.canDraw = false;

          restore_array.push(context.getImageData(0,0,canvas.width,canvas.height));
          limiter += 1;
          if (limiter == 1) {
            index += 1;
            console.log("index" + index)
            // console.log(restore_array);
            console.log("Drawing Stop")
          }
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
