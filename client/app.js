const express = require("express");
const bodyParser = require("body-parser");
const ejs = require("ejs");
const https = require("https");

const app = express();


app.use(bodyParser.urlencoded({extended:true}));
app.use(express.static("public"));
app.set("view engine","ejs");



var apiData ={};

function getData(state){

    const url1 = "";

    https.get(url,function(response){
        
       
        response.on("data",function(data){

            apiData = JSON.parse(data);
        });

        
    });

    const url2="";
}
app.get("/",function(req,res){

    res.render("index");

})


app.post("/",function(req,res){


    const state = req.body["state"];
    // getData(state);
    res.render("results",{"state": state});
})



app.listen(3000,()=>{

    console.log("Server running on port 3000");
})