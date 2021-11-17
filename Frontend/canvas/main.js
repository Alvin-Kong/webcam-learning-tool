const canvas = document.getElementById("canvas");
const context = canvas.getContext("2d");


whole();

// canvas is same as screen height and screen width 
function whole() {
    let pageWidth = document.documentElement.clientWidth;
    let pageHeight = document.documentElement.clientHeight;
    canvas.width = pageWidth;
    canvas.height = pageHeight;
}

      // When true, moving the mouse draws on the canvas
      // set the current canvas function as the pen state 
      let isDrawing = false;
      let startPoint = {x: undefined, y: undefined};

   
      canvas.addEventListener("mousedown", (e) => {
        let x = e.offsetX;
        let y = e.offsetY;
        isDrawing = true;
        startPoint = {x: x, y: y};
      });

      canvas.addEventListener("mousemove", (e) => {
        if (isDrawing === true) {
        let x = e.offsetX;
        let y = e.offsetY;
        let newPoint = {x: x, y: y};
        drawLine(startPoint.x, startPoint.y, newPoint.x, newPoint.y);
        startPoint = newPoint;
        }
      });

      canvas.addEventListener("mouseup", (e) => {
        isDrawing = false;
      });

      function drawLine(x_start, y_start, x_end,y_end) {
        context.beginPath();
        context.lineWidth = 2;
        context.moveTo(x_start, y_start);
        context.lineTo(x_end, y_end);
        context.stroke();
        context.closePath();
      }
