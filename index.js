//index.js
const express = require("express");
const spawn = require("child_process").spawn; 

const app = express();
const port = 5000;

// 정적 파일을 호스팅하기 위해 public 디렉토리를 사용
app.use(express.static("public"));

app.get("/run-script", (req, res) => {
    const net = spawn("python3", ["YOLO3.py"]);
    console.log("launching python script..");
    net.stdout.on("data", function (data) {
        const result = data.toString();
        console.log(result);
        res.send(result);
    });
});

app.listen(port, () => {
    console.log(`Example app listening at http://localhost:${port}`);
});