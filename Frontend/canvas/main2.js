const canvas = document.getElementById("canvas");
const context = canvas.getContext("2d");

// canvas is same as screen height and screen width 
let pageWidth = document.documentElement.clientWidth;
let pageHeight = document.documentElement.clientHeight;
canvas.width = pageWidth;
canvas.height = pageHeight;

// When true, moving the mouse draws on the canvas
// set the current canvas function as the pen state 
let isDrawing = false;
let stop = false;
let startPoint = {x: 300, y: 200};
let nextPoint = {x: undefined, y: undefined};


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
  return apiData
}


// Function to test whether API data can be retrieved
document.addEventListener('keypress', async event => {
  if (event.code === 'KeyN') {
    var data = await getapiData();
    console.log(data)
  }
})


// Main drawing functionality
document.addEventListener('keypress', async event => {
  if (event.code === 'Space') {
    isDrawing = true;
    console.log("Drawing Start")
    var startapiData = await getapiData();
    // console.log(startapiData);
    var startCenter = startapiData.data.results["center"];
    var startX = startapiData.data.results["x"];
    var startY = startapiData.data.results["y"];
    // console.log("start: " + startX + ", " + startY);

    // Main while loop to draw
    while (isDrawing) {
      var nextapiData = await getapiData();
      // console.log(nextapiData);
      var nextCenter = nextapiData.data.results["center"];
      var nextX = nextapiData.data.results["x"];
      var nextY = nextapiData.data.results["y"];
      // console.log("next: " + nextX + ", " + nextY);
      drawLine(startX, startY, nextX, nextY)
      
      // Press 'M' key to stop drawing and exit out of while loop
      document.addEventListener('keypress', event2 => {
        if (event2.code === 'KeyM') {
          isDrawing = false;
          console.log("Drawing Stop")
        }
      });
      
      startX = nextX;
      startY = nextY;
    }
  }
});


// Method to test the retrieval of API data
// document.addEventListener('keyup', event => {
//   if (event.code === 'Space') {
//     // getData().then(value => console.log(value));
//     var apiData = getData();
//     var data = async () => {
//       var result = await apiData;
//       console.log(result)
//       console.log(result.data.results["center"])
//       console.log(result.data.results["x"])
//       console.log(result.data.results["y"])
//     }
//     data();
//   }
// });

// Old drawing methods using mouse
////////////////////////////////////////////////////////////////////////////////////
// canvas.addEventListener("mousedown", (e) => {
//   let x = e.offsetX;
//   let y = e.offsetY;
//   isDrawing = true;
//   startPoint = {x: x, y: y};
// });


// canvas.addEventListener("mousemove", (e) => {
//   if (isDrawing === true) {
//     let x = e.offsetX;
//     let y = e.offsetY;
//     let newPoint = {x: x, y: y};
//     drawLine(startPoint.x, startPoint.y, newPoint.x, newPoint.y);
//     startPoint = newPoint;
//   }
// });


// canvas.addEventListener("mouseup", (e) => {
//   isDrawing = false;
// });
////////////////////////////////////////////////////////////////////////////////////

// Function to create drawing lines
function drawLine(x_start, y_start, x_end, y_end) {
  context.beginPath();
  context.lineWidth = 2;
  context.moveTo(x_start, y_start);
  context.lineTo(x_end, y_end);
  context.stroke();
  context.closePath();
}