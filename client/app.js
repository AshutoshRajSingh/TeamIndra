const express = require("express");
const bodyParser = require("body-parser");
const ejs = require("ejs");
const http = require("http");

const app = express();


app.use(bodyParser.urlencoded({extended:true}));
app.use(express.static("public"));
app.set("view engine","ejs");



var apiData ={};
var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
var labels = []
var states = []


function getData(state){

    const url = "http://localhost:8000/api/states/"+state+"/";

    http.get(url,function(response){
        
       
        response.on("data",function(data){

            apiData = JSON.parse(data);
        });

        
    });

    
  
}


app.get("/",function(req,res){

    res.render("index");

})


app.post("/",function(req,res){


    const state = req.body["state"];
    getData(state);

    // console.log(apiData.data);

    
    
    apiData.data["timestamps"].forEach((date)=>{

        var d = new Date(date*1000);
        var day = d.getDate();
        var month = d.getMonth();
        var year = d.getFullYear();

        date = year + '-' + month + '-' + day;

        labels.push(date);
    });
   
   
    res.render("results",{"state": state,"apiData":apiData,"labels":labels});
})



app.listen(3000,()=>{

    console.log("Server running on port 3000");
})